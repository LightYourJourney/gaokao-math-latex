"""Page OCR candidates keep source binding and never claim question assignment."""

import copy
import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
if importlib.util.find_spec("ocr_candidate_ir") is not None:
    from ocr_candidate_ir import OcrCandidateError, convert_run
else:
    OcrCandidateError = None
    convert_run = None


class OcrCandidateIrTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        runs = [json.loads(line) for line in (ROOT / "benchmarks/ocr-runs.jsonl").read_text(encoding="utf-8").splitlines()]
        cls.mineru = runs[1]

    def require_converter(self):
        self.assertIsNotNone(convert_run, "OCR 页候选 IR 转换模块尚不存在")
        return convert_run

    def test_real_mineru_run_remains_unassigned_and_source_bound(self):
        convert = self.require_converter()
        candidate = convert(self.mineru, self.manifest)

        self.assertEqual(candidate["source_id"], "src-afb8c527efcbf4f06deb050f6d4d636069bbd1d2d5c0bd2d2ca8d42b15d7649e")
        self.assertEqual(candidate["pdf_sha256"], "fdfb4e9e88d4405f8a99380d6f2197f3269e061ef9b2c4f7ed7066a56a1e88c2")
        self.assertEqual(candidate["source_page"], 5)
        self.assertEqual(candidate["engine"], "MinerU local managed basic / ONNX")
        self.assertEqual(candidate["candidate_text"], self.mineru["output"])
        self.assertIsNone(candidate["question_id"])
        self.assertEqual(candidate["assignment_status"], "unassigned-page-level")
        self.assertEqual(candidate["review_status"], "needs-review")
        self.assertEqual(candidate["prior_review_status"], "pending_human_review")
        self.assertEqual(candidate["candidate_text_sha256"], hashlib.sha256(self.mineru["output"].encode("utf-8")).hexdigest())
        self.assertEqual(candidate["cost_evidence"]["elapsed_seconds"], 32.37)
        self.assertEqual(candidate["cost_evidence"]["peak_rss_bytes"], 65241088)

    def test_native_ocr_pdf_result_preserves_page_bbox_and_cache_cost(self):
        run = {
            "source_id": "src-afb8c527efcbf4f06deb050f6d4d636069bbd1d2d5c0bd2d2ca8d42b15d7649e",
            "pdf_sha256": "fdfb4e9e88d4405f8a99380d6f2197f3269e061ef9b2c4f7ed7066a56a1e88c2",
            "engine": "tesseract",
            "engine_version": "5.5.3",
            "output": "unverified OCR text",
            "cache_hit": True,
            "render_cache_hit": True,
            "elapsed_seconds": 0.01,
            "metadata": {
                "source_page": 5,
                "source_sha256": "fdfb4e9e88d4405f8a99380d6f2197f3269e061ef9b2c4f7ed7066a56a1e88c2",
                "task": "page_text",
                "render_dpi": 180,
                "bbox_px": [0, 0, 1200, 1800],
                "bbox_coordinate_space": "rendered_page_px_top_left",
                "image_sha256": "1" * 64,
                "review_status": "needs-review",
            },
        }
        candidate = self.require_converter()(run, self.manifest)
        self.assertEqual(candidate["source_bbox"], [0, 0, 1200, 1800])
        self.assertEqual(candidate["bbox_coordinate_space"], "rendered_page_px_top_left")
        self.assertEqual(candidate["cost_evidence"]["cache_hit"], True)
        self.assertEqual(candidate["cost_evidence"]["render_cache_hit"], True)
        self.assertEqual(candidate["cost_evidence"]["elapsed_seconds"], 0.01)

    def test_converter_rejects_unbound_source_identity(self):
        run = copy.deepcopy(self.mineru)
        run["metadata"].pop("source_id")
        with self.assertRaisesRegex(OcrCandidateError, "source_id 缺失"):
            self.require_converter()(run, self.manifest)

    def test_converter_rejects_sha_mismatch_and_out_of_range_page(self):
        run = copy.deepcopy(self.mineru)
        run["metadata"]["source_sha256"] = "0" * 64
        with self.assertRaisesRegex(OcrCandidateError, "SHA-256 与 manifest 不一致"):
            self.require_converter()(run, self.manifest)

        run = copy.deepcopy(self.mineru)
        run["metadata"]["source_page"] = 8
        with self.assertRaisesRegex(OcrCandidateError, "页码超出来源页数"):
            self.require_converter()(run, self.manifest)

    def test_converter_rejects_conflicting_identity_and_recorded_output_hash(self):
        cases = []
        run = copy.deepcopy(self.mineru)
        run["source_id"] = "other-source"
        cases.append((run, "source_id 字段冲突"))
        run = copy.deepcopy(self.mineru)
        run["pdf_sha256"] = "0" * 64
        cases.append((run, "PDF SHA-256 字段冲突"))
        run = copy.deepcopy(self.mineru)
        run["source_page"] = 6
        cases.append((run, "页码字段冲突"))
        run = copy.deepcopy(self.mineru)
        run["output"] += " modified"
        cases.append((run, "OCR 输出 SHA-256 不匹配"))
        for run, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(OcrCandidateError, message):
                self.require_converter()(run, self.manifest)


if __name__ == "__main__":
    unittest.main()
