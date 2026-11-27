"""1990 上海卷第 26 题矢量图应保留原图点线拓扑且能编译。"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = ROOT / "1990/1990_数学真题_上海_试题.md"
FIGURE = PROJECT / "1990_上海卷/figures/gaokao_1990_shanghai_q26_planes.tex"
LINK = "../math-gaokao-latex/1990_上海卷/figures/gaokao_1990_shanghai_q26_planes.tex"


class Shanghai1990FigureTests(unittest.TestCase):
    def test_question_26_links_to_its_vector_figure(self):
        text = PAPER.read_text(encoding="utf-8")
        q26 = text.split("**26．**", 1)[1].split("**27．**", 1)[0]
        self.assertIn(f"]({LINK})", q26)
        self.assertTrue(FIGURE.is_file())

    def test_figure_preserves_plane_intersection_points_and_segments(self):
        self.assertTrue(FIGURE.is_file(), "missing source-vector figure")
        source = FIGURE.read_text(encoding="utf-8")
        for point in ("M", "N", "C", "A", "B", r"\alpha", r"\beta"):
            self.assertIn(point, source)
        for segment in ("(M)--(N)", "(A)--(C)", "(C)--(B)", "(A)--(B)"):
            self.assertIn(segment, source)
        self.assertNotIn(r"\includegraphics", source)
        self.assertIn("不按比例", source)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and pdftoppm are required")
    def test_figure_compiles_and_renders_one_nonempty_page(self):
        self.assertTrue(FIGURE.is_file(), "missing source-vector figure")
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="1990-shanghai-q26-", dir=work_root) as temp:
            build_dir = Path(temp)
            (build_dir / "figure.tex").write_text(
                r"\documentclass{article}" + "\n" +
                r"\usepackage[margin=1.5cm]{geometry}" + "\n" +
                r"\usepackage{tikz}" + "\n" +
                r"\pagestyle{empty}\begin{document}" + "\n" +
                r"\input{" + str(FIGURE) + "}\n" +
                r"\end{document}" + "\n",
                encoding="utf-8",
            )
            try:
                subprocess.run(
                    ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                    cwd=build_dir, check=True, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, timeout=120,
                )
            except subprocess.CalledProcessError as exc:
                self.fail(f"latexmk rejected the real figure source:\n{exc.stdout[-4000:]}")
            subprocess.run(
                ["pdftoppm", "-png", "-r", "150", "figure.pdf", "figure"],
                cwd=build_dir, check=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            pages = list(build_dir.glob("figure-*.png"))
            self.assertEqual(len(pages), 1)
            self.assertGreater(pages[0].stat().st_size, 1000)
            if os.environ.get("KEEP_1990_SHANGHAI_Q26_FIGURE") == "1":
                review_dir = PROJECT / ".work/review-1990-shanghai-q26"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(pages[0], review_dir / "figure-1.png")


if __name__ == "__main__":
    unittest.main()
