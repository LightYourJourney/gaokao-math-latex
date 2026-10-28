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
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季北京理_试题.md"
FIGURES = ROOT / "2004/2004_数学真题_春季北京理_图表清单.md"
PARABOLA_FIGURE = PROJECT / "2004_春季北京理科/figures/gaokao_2004_beijing_spring_science_q18_parabola.tex"
SOURCE_ID = "src-f845cde09dfedfcb590e7b0f5726822c767def9cd70ddf732102917e34c5fe12"
SOURCE_SHA256 = "7e4af53fb7548e19fb987d562b4172fba170102503b556e27fbadf2b9a97ac3d"


class BeijingSpring2004ScienceTranscriptionTests(unittest.TestCase):
    def test_draft_is_complete_traceable_and_preserves_high_risk_source_content(self):
        self.assertTrue(TRANSCRIPT.is_file(), "2004 Beijing spring science transcription is missing")
        self.assertTrue(FIGURES.is_file(), "source figure inventory is missing")
        self.assertTrue(PARABOLA_FIGURE.is_file(), "Q18 vector diagram is missing")

        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        figures = FIGURES.read_text(encoding="utf-8")
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(item for item in manifest["sources"] if item["source_id"] == SOURCE_ID)

        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], "春季高考/2004/2004春季北京理.pdf")
        self.assertEqual(source["paper_id"], "gk-2004-spring-beijing-science")
        self.assertEqual(source["paper_relation"], "canonical")
        paper = next(item for item in manifest["papers"] if item["paper_id"] == source["paper_id"])
        self.assertIn(SOURCE_ID, paper["source_ids"])
        for figure in paper["figure_files"]:
            figure_path = PROJECT / figure["path"]
            self.assertTrue(figure_path.is_file())
            self.assertIn(figure["path"], figures)
            links = re.findall(r"\]\(([^)]+)\)", transcript)
            self.assertIn(figure_path.resolve(), [(TRANSCRIPT.parent / link).resolve() for link in links])
        self.assertIn(SOURCE_ID, transcript)
        self.assertIn(SOURCE_SHA256, transcript)
        self.assertIn("paper_id: gk-2004-spring-beijing-science", transcript)
        self.assertIn("official_answer: null", transcript)

        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 21)))
        multiple_choice_prompts = re.findall(r"^\*\*(\d+)．(.*?)\n", transcript, re.M)
        self.assertEqual(len(multiple_choice_prompts), 20)
        for number, prompt in multiple_choice_prompts[:10]:
            with self.subTest(question=number):
                self.assertFalse(prompt.endswith("）。"), "source has no full stop after the answer blank")
        self.assertEqual(transcript.count("## 一、选择题"), 1)
        self.assertEqual(transcript.count("## 二、填空题"), 1)
        self.assertEqual(transcript.count("## 三、解答题"), 1)
        self.assertEqual(transcript.count("$") % 2, 0)

        for expected in (
            r"y=\tan\dfrac{x}{2}",
            r"\dfrac{2}{3}<m<1",
            r"\rho=-2\sqrt2\cos\theta",
            r"\sin(\theta+\pi)<0",
            r"\dfrac{c}{a}-\dfrac{d}{b}",
            r"a^{\sqrt{2x-1}}<a^{x-2}",
            r"A(2,8)",
            r"2N+1",
        ):
            self.assertIn(expected, transcript)
        self.assertIn("实际出厂单价不能低于 $51$ 元", transcript)
        self.assertIn("$1000$ 个", transcript)
        self.assertIn("\u4e24\u540d\u72ec\u7acb\u76f2\u6838\u5df2\u5b8c\u6210", transcript)
        self.assertNotIn("![", transcript)
        self.assertNotRegex(transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")
        self.assertIn("reconstructed from the stated constraints", PARABOLA_FIGURE.read_text(encoding="utf-8"))
        for question in (17, 18, 20):
            self.assertIn(f"| {question} |", figures)
        self.assertIn("出版物/版次/来源链及官方身份未核", transcript)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and Poppler are required")
    def test_q18_vector_and_q20_table_compile_and_render(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2004-beijing-science-", dir=work_root) as temp:
            build_dir = Path(temp)
            figure_doc = (
                "\\documentclass{article}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{amsmath,tikz}\n"
                "\\pagestyle{empty}\n\\begin{document}\n"
                "\\input{" + PARABOLA_FIGURE.as_posix() + "}\n"
                "\\end{document}\n"
            )
            (build_dir / "figure.tex").write_text(figure_doc, encoding="utf-8")
            result = subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                cwd=build_dir, check=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            self.assertTrue((build_dir / "figure.pdf").is_file())
            self.assertNotRegex(result.stdout, r"(?i)(?:LaTeX Warning|Package .* Warning|Overfull|Underfull|undefined|Missing character|! )")
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "120", str(build_dir / "figure.pdf"), str(build_dir / "figure")],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            self.assertGreater((build_dir / "figure.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2004_BEIJING_SCIENCE_FIGURES") == "1":
                review_dir = PROJECT / ".work/review-2004-beijing-science"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(build_dir / "figure.png", review_dir / "q18.png")

            transcript = TRANSCRIPT.read_text(encoding="utf-8")
            table = transcript.split(r"\begin{array", 1)[1].split(r"\end{array}", 1)[0]
            table_doc = (
                "\\documentclass{article}\n\\usepackage{amsmath}\n"
                "\\pagestyle{empty}\n\\begin{document}\n\\[\\begin{array" + table + "\\end{array}\\]\n\\end{document}\n"
            )
            (build_dir / "table.tex").write_text(table_doc, encoding="utf-8")
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "table.tex"],
                cwd=build_dir, check=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            info = subprocess.run(["pdfinfo", str(build_dir / "table.pdf")], check=True, capture_output=True, text=True)
            self.assertRegex(info.stdout, r"Pages:\s+1")
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "120", str(build_dir / "table.pdf"), str(build_dir / "table")],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            self.assertGreater((build_dir / "table.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2004_BEIJING_SCIENCE_FIGURES") == "1":
                shutil.copy2(build_dir / "table.png", review_dir / "q20.png")


if __name__ == "__main__":
    unittest.main()
