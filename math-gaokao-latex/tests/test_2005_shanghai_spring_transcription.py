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
TRANSCRIPT = ROOT / "2005/2005_数学真题_春季上海_试题.md"
FIGURES = ROOT / "2005/2005_数学真题_春季上海_图表清单.md"
SOURCE_ID = "src-2cd71e4caf6708c2589791bd24ba1b55d6d80d2c08b764a325587c7a991d8c83"
SOURCE_SHA256 = "67d4850cc310a4c089729daf7ff1b8fa3bdacaaaf6b227918669bd0972fb56b5"
FIGURE_PATHS = {
    19: ROOT / "2005/figures/gaokao_2005_shanghai_spring_q19_pyramid.tex",
    21: ROOT / "2005/figures/gaokao_2005_shanghai_spring_q21_function.tex",
    22: ROOT / "2005/figures/gaokao_2005_shanghai_spring_q22_ellipse.tex",
}


class ShanghaiSpring2005TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription draft must exist")
        self.assertTrue(FIGURES.is_file(), "the source-figure inventory must exist")
        self.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        self.figures = FIGURES.read_text(encoding="utf-8")

    def test_fixed_source_fingerprint_is_traceable_and_not_formally_bound(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], "春季高考/2005/2005春季上海.pdf")
        self.assertIsNone(source["paper_id"])
        self.assertIn(SOURCE_ID, self.transcript)
        self.assertIn(SOURCE_SHA256, self.transcript)
        self.assertIn("原卷印刷页码 217–218", self.transcript)
        self.assertIn("paper_id 未绑定", self.transcript)

    def test_all_22_questions_and_source_sections_are_present(self):
        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("## 一、填空题"), 1)
        self.assertEqual(self.transcript.count("## 二、选择题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertEqual(self.transcript.count("$") % 2, 0)

    def test_high_risk_math_and_wording_match_the_fixed_source(self):
        normalized = self.transcript.replace(r"\dfrac", r"\frac")
        for source_detail in (
            r"\lg x^2-\lg(x+2)=0",
            r"\frac{n+2}{1+2+\cdots+n}",
            r"\cos\alpha=\frac35",
            r"f(x)=-x^2",
            r"x\in(-\infty,-2]",
            r"\overrightarrow{BA}\cdot\overrightarrow{BC}",
            r"9x^2-16y^2=1",
            r"(x+2)^n=x^n+\cdots+ax^3+bx^2+cx+2^n",
            r"3\cos 2\pi x=3^x",
            r"y=\sin x+\arcsin x",
            r"f(x)=2^x+\log_2 x",
            r"m\parallel n",
            r"\frac{a}{\cos A}=\frac{b}{\cos B}=\frac{c}{\cos C}",
            r"b^2-4ac<0",
            r"\frac{z}{2-i}",
            r"x^2+2x\sec\alpha+1=0",
            r"72\sqrt3",
            r"1200\text{ 万平方米}",
            r"f(2)=2+\frac{\sqrt2}{2}",
            r"\frac{x^2}{a^2}+\frac{y^2}{b^2}=1\ (a>b>0)",
        ):
            self.assertIn(source_detail, normalized)
        self.assertIn(r"a_n=0.1n", self.transcript)
        self.assertIn(r"\tan\alpha", self.transcript)
        self.assertIn("较小的根", self.transcript)
        self.assertIn("未生成答案或解析", self.transcript)

    def test_every_source_figure_has_a_vector_source_and_no_raster_embedding(self):
        self.assertIn("第 19 题", self.figures)
        self.assertIn("第 21 题", self.figures)
        self.assertIn("第 22 题", self.figures)
        for question, path in FIGURE_PATHS.items():
            relative_path = path.relative_to(ROOT / "2005")
            self.assertIn(str(relative_path), self.transcript)
            self.assertIn(str(relative_path), self.figures)
            self.assertTrue(path.is_file(), f"missing vector figure for Q{question}")
            source = path.read_text(encoding="utf-8")
            self.assertIn(r"\begin{tikzpicture}", source)
            self.assertNotIn(r"\includegraphics", source)
        pyramid = FIGURE_PATHS[19].read_text(encoding="utf-8")
        self.assertIn(r"\draw[dashed] (A)--(C) (P)--(O);", pyramid)
        self.assertIn(r"\draw (A)--(B)--(C) (P)--(A) (P)--(B) (P)--(C);", pyramid)

        function_figure = FIGURE_PATHS[21].read_text(encoding="utf-8")
        coordinates = {
            name: (float(x), float(y))
            for name, x, y in re.findall(
                r"\\coordinate \((\w+)\) at \((-?[0-9.]+),(-?[0-9.]+)\);",
                function_figure,
            )
        }
        px, py = coordinates["P"]
        nx, ny = coordinates["N"]
        mx, my = coordinates["M"]
        self.assertEqual(nx, 0)
        self.assertAlmostEqual(py, ny)
        self.assertAlmostEqual(mx, my)
        self.assertAlmostEqual(px + py, mx + my)

        ellipse = FIGURE_PATHS[22].read_text(encoding="utf-8")
        self.assertNotIn(r"\node", ellipse)
        self.assertNotIn(r"\coordinate", ellipse)
        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and Poppler are required")
    def test_vector_figures_compile_and_render_together(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2005-shanghai-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            inputs = "\n".join(r"\input{" + str(path) + "}" for path in FIGURE_PATHS.values())
            (build_dir / "figures.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                + inputs
                + "\n\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figures.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figures.pdf"
            self.assertTrue(pdf.is_file())
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "140", str(pdf), str(build_dir / "figures")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            self.assertGreater((build_dir / "figures.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2005_SHANGHAI_FIGURE_REVIEW") == "1":
                review_dir = PROJECT / ".work/review-2005-shanghai-spring"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(build_dir / "figures.png", review_dir / "figures.png")


if __name__ == "__main__":
    unittest.main()
