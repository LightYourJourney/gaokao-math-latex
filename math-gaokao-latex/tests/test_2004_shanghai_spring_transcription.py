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
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季上海_试题.md"
FIGURES = ROOT / "2004/2004_数学真题_春季上海_图表清单.md"
Q11_FIGURE = ROOT / "2004/figures/gaokao_2004_shanghai_spring_q11_pascal.tex"
Q6_FIGURE = ROOT / "2004/figures/gaokao_2004_shanghai_spring_q06_pyramid.tex"
SOURCE_ID = "src-eda3090af4489c2848005279f9f1f65a561d4fa54daf91ccd574cfbff213be4f"
SOURCE_SHA256 = "e09d135e7814d1d5dd658ac51829a170edae1267b408f30a4edfa44d2312ca8a"


class ShanghaiSpring2004TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        cls.figures = FIGURES.read_text(encoding="utf-8")
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def test_fixed_source_identity_matches_manifest_and_stays_unbound(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], "春季高考/2004/2004春季上海.pdf")
        self.assertIsNone(source["paper_id"])
        self.assertIn(SOURCE_ID, self.transcript)
        self.assertIn(SOURCE_SHA256, self.transcript)
        self.assertIn("paper_id 未绑定", self.transcript)

    def test_question_numbers_sections_and_math_delimiters_are_complete(self):
        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("## 一、填空题"), 1)
        self.assertEqual(self.transcript.count("## 二、选择题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertEqual(self.transcript.count("$") % 2, 0)

    def test_source_wording_and_high_risk_formulas_are_preserved(self):
        for expected in (
            r"f(x)=\log_3\left(\dfrac{4}{x}+2\right)",
            r"(\sqrt{a_n},\sqrt{a_{n-1}})",
            r"4(x+3)^2+9y^2=36",
            r"\overrightarrow{AB}-\overrightarrow{AC}=\overrightarrow{BC}",
            r"\dfrac{2x+1}{x+2}<0",
            r"10^{f(n)}\cdot\left(\dfrac{4}{5}\right)^{g(n)}<4",
            r"\dfrac{x^2}{a^2}-y^2=1",
        ):
            self.assertIn(expected, self.transcript)
        self.assertIn("实数 $p$ 满足不等式", self.transcript)
        self.assertIn("未将 $x$ 擅改为 $p$", self.transcript)

    def test_all_source_figures_are_registered_without_raster_embedding(self):
        for question in ("第 6 题", "第 8 题", "第 11 题", "第 20 题"):
            self.assertIn(question, self.figures)
            self.assertIn(question, self.transcript)
        self.assertIn("1,3,7,13,21", self.figures)
        self.assertIn("第 0 行", self.figures)
        self.assertIn("1,5,10,10,5,1", self.figures)
        self.assertIn("$AB$ 为实线", self.figures)
        self.assertIn("$AC$ 与 $AE$ 为虚线", self.figures)
        self.assertTrue(Q11_FIGURE.is_file())
        self.assertTrue(Q6_FIGURE.is_file())
        self.assertIn("figures/gaokao_2004_shanghai_spring_q06_pyramid.tex", self.transcript)
        self.assertIn("figures/gaokao_2004_shanghai_spring_q11_pascal.tex", self.transcript)
        q11_source = Q11_FIGURE.read_text(encoding="utf-8")
        self.assertEqual(q11_source.count(r"\cdots"), 4)
        self.assertNotIn(r"\vdots", q11_source)
        self.assertIn("第 \\r 行", q11_source)
        self.assertIn(r"\foreach \r in {0,...,5}", q11_source)
        self.assertNotIn(r"\includegraphics", q11_source)
        q6_source = Q6_FIGURE.read_text(encoding="utf-8")
        self.assertIn(r"\draw[dashed] (A)--(C) (A)--(E);", q6_source)
        self.assertIn(r"\draw (A)--(B)--(C);", q6_source)
        self.assertNotIn(r"\includegraphics", q6_source)
        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")

    @unittest.skipUnless(shutil.which("latexmk"), "latexmk is required for the vector-figure smoke build")
    def test_pascal_triangle_figure_compiles_and_renders(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2004-shanghai-q11-", dir=work_root) as temp:
            build_dir = Path(temp)
            (build_dir / "figure.tex").write_text(
                "\\documentclass{ctexart}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                "\\input{" + str(Q11_FIGURE) + "}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figure.pdf"
            self.assertTrue(pdf.is_file())
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "120", str(pdf), str(build_dir / "figure")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            self.assertGreater((build_dir / "figure.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2004_SHANGHAI_Q11_REVIEW") == "1":
                review_dir = PROJECT / ".work/review-2004-shanghai-q11"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(build_dir / "figure.png", review_dir / "q11-pascal.png")

    @unittest.skipUnless(shutil.which("latexmk"), "latexmk is required for the vector-figure smoke build")
    def test_pyramid_figure_compiles_and_renders(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2004-shanghai-q06-", dir=work_root) as temp:
            build_dir = Path(temp)
            (build_dir / "figure.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                "\\input{" + str(Q6_FIGURE) + "}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figure.pdf"
            self.assertTrue(pdf.is_file())
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "120", str(pdf), str(build_dir / "figure")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            self.assertGreater((build_dir / "figure.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2004_SHANGHAI_Q06_REVIEW") == "1":
                review_dir = PROJECT / ".work/review-2004-shanghai-q06"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(build_dir / "figure.png", review_dir / "q06-pyramid.png")


if __name__ == "__main__":
    unittest.main()
