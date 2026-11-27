#!/usr/bin/env python3
"""Run the original Xiaomi checkpoint locally; invoked in its isolated environment."""
import argparse
import json
import os
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('--model-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--task', choices=['document', 'text', 'formula'], default='document')
    parser.add_argument('--device', choices=['mps', 'cpu'], default='mps')
    parser.add_argument('--max-tokens', type=int, default=4096)
    args = parser.parse_args()
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    import torch
    from transformers import AutoModelForImageTextToText, AutoProcessor
    from PIL import Image
    if args.device == 'mps' and not torch.backends.mps.is_available():
        raise RuntimeError('MPS unavailable; explicitly select --device cpu')
    prompts = {
        'document': 'Extract all information from the main body of the document image and represent it in markdown format, ignoring headers and footers. Tables should be expressed in OTSL format, formulas in the document should be represented using LATEX format, and the parsing should be organized according to the reading order.',
        'text': 'Extract the text in the image.',
        'formula': 'Identify the formula in the image and represent it using LATEX format.',
    }
    started = time.monotonic()
    processor = AutoProcessor.from_pretrained(args.model_dir, local_files_only=True)
    model = AutoModelForImageTextToText.from_pretrained(
        args.model_dir, local_files_only=True,
        dtype=torch.float32 if args.device == 'cpu' else torch.float16,
    ).to(args.device).eval()
    loaded = time.monotonic()
    image = Image.open(args.image).convert('RGB')
    image.thumbnail((2048, 2048))
    messages = [{'role': 'user', 'content': [
        {'type': 'image', 'image': image},
        {'type': 'text', 'text': prompts[args.task]},
    ]}]
    inputs = processor.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, enable_thinking=False,
        return_dict=True, return_tensors='pt',
    ).to(args.device)
    with torch.inference_mode():
        generated = model.generate(**inputs, max_new_tokens=args.max_tokens, do_sample=False)
    tokens = generated[0, inputs['input_ids'].shape[1]:]
    eos = model.generation_config.eos_token_id
    eos = [eos] if isinstance(eos, int) else (eos or [])
    if len(tokens) >= args.max_tokens and int(tokens[-1]) not in eos:
        raise RuntimeError('Truncated generation; increase --max-tokens or use a smaller crop')
    output = processor.decode(tokens, skip_special_tokens=True)
    if not output.strip():
        raise RuntimeError('Empty model output')
    result = {'output': output, 'device': args.device,
              'model_load_seconds': round(loaded-started, 6),
              'inference_seconds': round(time.monotonic()-loaded, 6),
              'generated_tokens': len(tokens), 'truncated': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    main()
