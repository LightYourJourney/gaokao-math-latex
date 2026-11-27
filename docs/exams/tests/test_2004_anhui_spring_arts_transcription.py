import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季安徽文_试题.md"
FIGURES = ROOT / "2004/2004_数学真题_春季安徽文_图表清单.md"
FIGURE = PROJECT / "2004_安徽春季卷_文科/figures/gaokao_2004_anhui_spring_arts_q20_prism.tex"
SOURCE_ID = "src-9c46c959fc97e9d53c91e510403e97f1810d192e5049962539d9d4b54331c35d"
SOURCE_SHA256 = "17f32ff6f385dfd59d80f5bccfa548dd9b7f8d20e697ce4a66b4de185b95d7a8"


class AnhuiSpring2004ArtsTranscriptionTests(unittest.TestCase):
    def test_transcription_is_complete_traceable_and_preserves_source_math(self):
        self.assertTrue(TRANSCRIPT.is_file(), "2004 Anhui spring arts transcription is missing")
        self.assertTrue(FIGURES.is_file(), "source figure inventory is missing")
        self.assertTrue(FIGURE.is_file(), "Q20 vector figure is missing")

        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        figures = FIGURES.read_text(encoding="utf-8")
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(item for item in manifest["sources"] if item["source_id"] == SOURCE_ID)

        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], "春季高考/2004/2004春季安徽文.pdf")
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["paper_id"], "gk-2004-spring-anhui-arts")
        self.assertEqual(source["paper_relation"], "canonical")
        self.assertIn(SOURCE_ID, transcript)
        self.assertIn(SOURCE_SHA256, transcript)
        self.assertIn("paper_id=gk-2004-spring-anhui-arts", transcript)
        self.assertIn("当前 paper ID 为 `gk-2004-spring-anhui-arts`", transcript)
        self.assertNotIn("`paper_id=", transcript)
        body = transcript.split("## 数学试卷", 1)[1]
        self.assertIsNone(re.search(r"`[^`\n]*_[^`\n]*`", body), "TeX body contains inline code with unescaped underscores")
        self.assertNotIn("paper_id 未绑定", transcript)
        self.assertIn("official_answer: null", transcript)

        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        for section in ("一、选择题", "二、填空题", "三、解答题"):
            self.assertEqual(transcript.count(f"## {section}"), 1)
        self.assertEqual(transcript.count("$") % 2, 0)

        for source_sensitive_text in (
            r"\sqrt{2}\cos\left(\dfrac{\pi}{4}-\alpha\right)",
            r"\left(x+\frac{1}{x}-2\right)^n",
            r"\log_a^{2}x<2\log_ax",
            r"A_1B=\frac{\sqrt{6}}{2}a",
            r"Q=8300-170p-p^2",
            r"y=x^2+4x+\frac{7}{2}",
        ):
            self.assertIn(source_sensitive_text, transcript)
        self.assertNotIn(r"\log_{2a}", transcript)

        self.assertIn("| 20 |", figures)
        self.assertIn(FIGURE.name, transcript)
        self.assertIn("不按比例", figures)
        self.assertIn(r"\draw[densely dashed] (A) -- (C);", FIGURE.read_text(encoding="utf-8"))
        self.assertNotIn("![", transcript)
        self.assertNotRegex(transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")

    def test_q20_figure_is_a_vector_redraw_with_source_topology(self):
        self.assertTrue(FIGURE.is_file(), "Q20 vector figure is missing")
        figure = FIGURE.read_text(encoding="utf-8")
        self.assertIn(r"\begin{tikzpicture}", figure)
        self.assertIn(r"\end{tikzpicture}", figure)
        self.assertIn(r"\draw[densely dashed] (A) -- (C);", figure)
        for label in ("A", "B", "C", "A_1", "B_1", "C_1"):
            self.assertIn(f"${label}$", figure)
        self.assertIn("not to scale", figure)
        self.assertNotIn(r"\includegraphics", figure)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and Poppler are required")
    def test_q20_figure_compiles_and_renders(self):
        self.assertTrue(FIGURE.is_file(), "Q20 vector figure is missing")
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2004-anhui-q20-", dir=work_root) as temp:
            build_dir = Path(temp)
            shutil.copy2(FIGURE, build_dir / "figure_body.tex")
            (build_dir / "figure.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                "\\input{figure_body.tex}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            self.assertTrue((build_dir / "figure.pdf").is_file())
            self.assertNotRegex(
                result.stdout,
                r"(?i)(?:LaTeX Warning|Package .* Warning|Overfull|Underfull|undefined|Missing character|! )",
            )
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "150", str(build_dir / "figure.pdf"), str(build_dir / "figure")],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            rendered = build_dir / "figure.png"
            self.assertGreater(rendered.stat().st_size, 1000)
            if os.environ.get("KEEP_2004_ANHUI_FIGURE") == "1":
                review_dir = PROJECT / ".work/review-2004-anhui-arts"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(rendered, review_dir / "q20-prism.png")


if __name__ == "__main__":
    unittest.main()
