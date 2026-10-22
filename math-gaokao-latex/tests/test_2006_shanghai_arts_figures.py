"""Source-bound vector-figure checks for the 2006 Shanghai arts paper."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER_SOURCE = ROOT / "2006/2006_数学真题_上海文_试题.md"
FIGURES = {
    12: ROOT / "math-gaokao-latex/2006_上海卷_文科/figures/f2006_shanghai_arts_q12_distance_coordinates.tex",
    13: ROOT / "math-gaokao-latex/2006_上海卷_文科/figures/f2006_shanghai_arts_q13_parallelogram.tex",
    18: ROOT / "math-gaokao-latex/2006_上海卷_文科/figures/f2006_shanghai_arts_q18_bearing.tex",
    19: ROOT / "math-gaokao-latex/2006_上海卷_文科/figures/f2006_shanghai_arts_q19_triangular_prism.tex",
}
FIGURE_LINK_PREFIX = "../math-gaokao-latex/2006_上海卷_文科/figures/"


class ShanghaiArts2006FigureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = PAPER_SOURCE.read_text(encoding="utf-8")

    def test_each_source_figure_is_linked_from_its_question(self):
        for number, path in FIGURES.items():
            with self.subTest(question=number):
                section = re.search(
                    rf"(?ms)^\*\*{number}．\*\*.*?(?=^\*\*{number + 1}．\*\*|\Z)",
                    self.transcript,
                )
                self.assertIsNotNone(section, f"Q{number} block is missing")
                self.assertIn(f"]({FIGURE_LINK_PREFIX}{path.name})", section.group(0))
                self.assertTrue(path.is_file(), f"Q{number} TikZ source is missing: {path}")
                source = path.read_text(encoding="utf-8")
                self.assertIn(r"\begin{tikzpicture}", source)
                self.assertIn(r"\end{tikzpicture}", source)
                self.assertNotIn(r"\includegraphics", source)
        self.assertNotIn("![](", self.transcript)

    def test_q12_q13_and_q18_preserve_source_visible_markers(self):
        sources = {number: path.read_text(encoding="utf-8") for number, path in FIGURES.items()}
        q12 = sources[12]
        for marker in (r"$l_1$", r"$l_2$", r"$O$", r"$M(p,q)$"):
            with self.subTest(question=12, marker=marker):
                self.assertIn(marker, q12)
        self.assertIn(r"\draw[dashed] (M)--(P);", q12)
        self.assertIn(r"\draw[dashed] (M)--(Q);", q12)
        self.assertRegex(q12, r"\\draw\[thin\]\s*\(P\)--")
        self.assertRegex(q12, r"\\draw\[thin\]\s*\(Q\)--")

        q13 = sources[13]
        for edge in ("(A)--(B)", "(B)--(C)", "(C)--(D)", "(D)--(A)"):
            with self.subTest(question=13, edge=edge):
                self.assertIn(edge, q13)
        for label in ("A", "B", "C", "D"):
            self.assertIn(f"{{${label}$}}", q13)

        q18 = sources[18]
        self.assertIn("{北}", q18)
        self.assertIn(r"\draw[->]", q18)
        self.assertGreaterEqual(q18.count(r"\draw[dashed]"), 2)
        for measurement in ("20", "10", r"30^\circ"):
            self.assertIn(measurement, q18)

    def test_q19_preserves_prism_edges_and_hidden_segments(self):
        q19 = FIGURES[19].read_text(encoding="utf-8")
        for label in ("A", "A_1", "B", "B_1", "C", "C_1"):
            with self.subTest(label=label):
                self.assertIn(f"${label}$", q19)
        for edge in ("(A)--(A1)", "(C)--(C1)", "(A)--(C)", "(A1)--(B1)", "(B1)--(C1)", "(A1)--(C1)", "(A1)--(C)"):
            with self.subTest(solid_edge=edge):
                self.assertIn(edge, q19)
        for edge in ("(A)--(B)", "(B)--(C)", "(B)--(B1)", "(A1)--(B)"):
            with self.subTest(hidden_edge=edge):
                self.assertRegex(q19, rf"\\draw\[dashed\][^\n]*{re.escape(edge)}")

    @unittest.skipUnless(shutil.which("latexmk"), "latexmk is required to compile TikZ figures")
    def test_all_four_figures_compile_without_layout_warnings(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        for number, path in FIGURES.items():
            with self.subTest(question=number), tempfile.TemporaryDirectory(
                prefix=f"2006-shanghai-arts-q{number}-", dir=work_root
            ) as temp:
                build_dir = Path(temp)
                document = (
                    r"\documentclass[fontset=fandol]{ctexart}" + "\n"
                    r"\usepackage{tikz}" + "\n"
                    r"\pagestyle{empty}" + "\n"
                    r"\begin{document}" + "\n"
                    r"\input{" + path.as_posix() + "}" + "\n"
                    r"\end{document}" + "\n"
                )
                (build_dir / "figure.tex").write_text(document, encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
