import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季安徽理_试题.md"
FIGURES = ROOT / "2004/2004_数学真题_春季安徽理_图表清单.md"
FIGURE = PROJECT / "2004_安徽春季卷_理科/figures/gaokao_2004_anhui_spring_science_q20_prism.tex"
SOURCE_ID = "src-7c00191d50c17971e6f514bf6066e92693aa2b71f0ff05a054e2abe22acb5075"
SOURCE_SHA256 = "51038ba6ecdfbb8c5c7edc417f871eda5a5a5c03cc5af510da08131ec0dbb151"


class AnhuiSpring2004ScienceTranscriptionTests(unittest.TestCase):
    def test_transcription_preserves_all_questions_and_high_risk_source_math(self):
        self.assertTrue(TRANSCRIPT.is_file(), "2004 Anhui spring science transcription is missing")
        self.assertTrue(FIGURES.is_file(), "Q20 figure inventory is missing")
        self.assertTrue(FIGURE.is_file(), "Q20 vector figure is missing")

        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        figures = FIGURES.read_text(encoding="utf-8")
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(item for item in manifest["sources"] if item["source_id"] == SOURCE_ID)

        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], "春季高考/2004/2004春季安徽理.pdf")
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        self.assertIn(SOURCE_ID, transcript)
        self.assertIn(SOURCE_SHA256, transcript)
        self.assertIn("paper_id 未绑定", transcript)
        self.assertIn("official_answer: null", transcript)

        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        for section in ("一、选择题", "二、填空题", "三、解答题"):
            self.assertEqual(transcript.count(f"## {section}"), 1)
        choice_section = transcript.split("## 二、填空题", 1)[0]
        self.assertEqual(len(re.findall(r"（[A-D]）", choice_section)), 48)
        self.assertEqual(transcript.count("$") % 2, 0)

        for source_sensitive_text in (
            r"\dfrac{5(4+i)^2}{i(2+i)}",
            r"5(1-38i)",
            r"\dfrac{(n-2)^2(2+3n)^3}{(1-n)^5}",
            r"f(\sin x)=2-\cos 2x",
            r"\sin^4x+\cos^4x",
            r"\left(x+\dfrac{1}{x}-2\right)^n",
            r"\log_a^3 x<3\log_a x",
            r"B_n=\dfrac{1}{4}(b_n+1)^2",
            r"A_1B=\dfrac{\sqrt{6}}{2}a",
            r"y=x^2+4x+\dfrac{2}{7}",
        ):
            self.assertIn(source_sensitive_text, transcript)
        self.assertIn("\n**18．** 已知正项数列", transcript)
        self.assertIn("\n**21．** 已知盒中有 $10$ 个灯泡", transcript)

        self.assertIn("| 20 |", figures)
        self.assertIn(FIGURE.name, transcript)
        self.assertIn("不按比例", figures)
        self.assertNotIn("![", transcript)
        self.assertNotRegex(transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")

    def test_q20_vector_figure_retains_prism_and_question_line_topology(self):
        self.assertTrue(FIGURE.is_file(), "Q20 vector figure is missing")
        figure = FIGURE.read_text(encoding="utf-8")
        self.assertIn(r"\begin{tikzpicture}", figure)
        self.assertIn(r"\end{tikzpicture}", figure)
        self.assertIn(r"\draw[densely dashed, line width=0.55pt] (A) -- (C);", figure)
        for label in ("A", "B", "C", "A_1", "B_1", "C_1"):
            self.assertIn(f"${label}$", figure)
        drawn_segments = {
            frozenset((start, end))
            for start, end in re.findall(
                r"\\draw\[[^\]]+\]\s*\(([^)]+)\)\s*--\s*\(([^)]+)\);",
                figure,
            )
        }
        self.assertEqual(
            drawn_segments,
            {
                frozenset(("A", "C")),
                frozenset(("A", "B")),
                frozenset(("B", "C")),
                frozenset(("A", "A_1")),
                frozenset(("B", "B_1")),
                frozenset(("C", "C_1")),
                frozenset(("A_1", "B_1")),
                frozenset(("B_1", "C_1")),
                frozenset(("A_1", "C_1")),
                frozenset(("A_1", "B")),
                frozenset(("A", "B_1")),
                frozenset(("B", "C_1")),
                frozenset(("A_1", "C")),
                frozenset(("B_1", "C")),
            },
        )
        self.assertIn("not to scale", figure)
        self.assertNotIn(r"\includegraphics", figure)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and Poppler are required")
    def test_q20_vector_figure_compiles_and_renders(self):
        self.assertTrue(FIGURE.is_file(), "Q20 vector figure is missing")
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2004-anhui-science-q20-", dir=work_root) as temp:
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
            if os.environ.get("KEEP_2004_ANHUI_SCIENCE_FIGURE") == "1":
                review_dir = PROJECT / ".work/review-2004-anhui-science"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(rendered, review_dir / "q20-prism.png")


if __name__ == "__main__":
    unittest.main()
