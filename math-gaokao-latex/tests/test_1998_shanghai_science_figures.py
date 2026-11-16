"""Vector-source and build guards for the 1998 Shanghai science Q19 figure."""
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = PROJECT / "1998_上海卷_理科"
QUESTIONS = PAPER / "题面转录草稿.md"
FIGURE = PAPER / "figures/1998_shanghai_science_q19_prism.tex"


class Shanghai1998ScienceFigureTests(unittest.TestCase):
    def test_q19_links_to_a_local_vector_figure(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        self.assertIn("](figures/1998_shanghai_science_q19_prism.tex)", questions)
        self.assertIn("第19题直四棱柱图（按原卷拓扑矢量重绘，不按比例）", questions)
        self.assertTrue(FIGURE.is_file())

    def test_figure_contains_prism_labels_and_source_relations(self):
        source = FIGURE.read_text(encoding="utf-8")
        for label in ("$A$", "$B$", "$C$", "$D$", "$A_1$", "$B_1$", "$C_1$", "$D_1$", "$O$", "$O_1$", "$E$"):
            with self.subTest(label=label):
                self.assertIn(label, source)
        for segment in (
            "(A)--(B)--(C)",
            "(C1)--(B1)--(A1)",
            "(A)--(A1)",
            "(B)--(B1)",
            "(C)--(C1)",
            "(D)--(D1)",
            "(O)--(O1)",
            "(A)--(C)",
            "(B)--(D)",
            "(A)--(E)--(O1)",
        ):
            with self.subTest(segment=segment):
                self.assertIn(segment, source)
        self.assertIn("不按比例", source)
        self.assertNotIn(r"\includegraphics", source)
        self.assertNotRegex(source, r"\.(?:png|jpe?g)")

    def test_coordinate_axes_follow_the_positive_rays_in_the_question(self):
        source = FIGURE.read_text(encoding="utf-8")
        coordinates = {
            name: (float(x), float(y))
            for name, x, y in re.findall(
                r"\\coordinate \((\w+)\)\s+at \(([-\d.]+),([-\d.]+)\);", source
            )
        }
        for endpoint, target in (("xAxisEnd", "A"), ("yAxisEnd", "B"), ("zAxisEnd", "O1")):
            with self.subTest(axis=endpoint):
                if endpoint == "zAxisEnd":
                    self.assertIn("(O) -- (O1)", source)
                    self.assertIn(f"(O1) -- ({endpoint})", source)
                else:
                    self.assertIn(f"(O) -- ({endpoint})", source)
                direction = tuple(coordinates[target][i] - coordinates["O"][i] for i in (0, 1))
                axis = tuple(coordinates[endpoint][i] - coordinates["O"][i] for i in (0, 1))
                cross = direction[0] * axis[1] - direction[1] * axis[0]
                dot = direction[0] * axis[0] + direction[1] * axis[1]
                self.assertAlmostEqual(cross, 0.0, places=6)
                self.assertGreater(dot, 0.0)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and pdftoppm are required")
    def test_q19_vector_source_compiles_and_renders(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="1998-shanghai-science-figure-", dir=work_root) as temp:
            build_dir = Path(temp)
            (build_dir / "figure.tex").write_text(
                "\n".join((
                    r"\documentclass{article}",
                    r"\usepackage[margin=1.5cm]{geometry}",
                    r"\usepackage{tikz}",
                    r"\pagestyle{empty}",
                    r"\begin{document}",
                    r"\input{" + str(FIGURE) + "}",
                    r"\end{document}",
                )) + "\n",
                encoding="utf-8",
            )
            try:
                subprocess.run(
                    ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                    cwd=build_dir, check=True, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, timeout=120,
                )
            except subprocess.CalledProcessError as exc:
                self.fail(f"latexmk rejected the Q19 vector source:\n{exc.stdout[-4000:]}")
            subprocess.run(
                ["pdftoppm", "-png", "-r", "150", "figure.pdf", "figure"],
                cwd=build_dir, check=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            pages = sorted(build_dir.glob("figure-*.png"))
            self.assertEqual(len(pages), 1)
            self.assertGreater(pages[0].stat().st_size, 2000)
            if os.environ.get("KEEP_1998_SHANGHAI_SCIENCE_FIGURE") == "1":
                shutil.copy2(pages[0], PROJECT / ".work/review-1998-shanghai-science-q19.png")


if __name__ == "__main__":
    unittest.main()
