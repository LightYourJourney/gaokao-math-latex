import json
import re
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "2000/2000_数学真题_春季上海_试题.md"
LATEX_ROOT = ROOT / "math-gaokao-latex"
FIGURES = LATEX_ROOT / "2000_春季上海卷/figures"
EXPECTED = {
    8: "gaokao_2000_shanghai_spring_q08_geometry.tex",
    17: "gaokao_2000_shanghai_spring_q17_even_function.tex",
    22: "gaokao_2000_shanghai_spring_q22_ellipse.tex",
}


class ShanghaiSpring2000FigureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paper = PAPER.read_text(encoding="utf-8")
        manifest = json.loads((LATEX_ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        cls.record = next(paper for paper in manifest["papers"] if paper["paper_id"] == "gk-2000-spring-shanghai")

    def test_each_source_figure_is_linked_from_its_question(self):
        for question, filename in EXPECTED.items():
            with self.subTest(question=question):
                heading = re.search(
                    rf"^\*\*{question}．.*?(?=^\*\*\d+．|\Z)",
                    self.paper,
                    re.M | re.S,
                )
                self.assertIsNotNone(heading, f"missing question {question}")
                links = re.findall(r"\[图稿（TikZ 源）\]\(([^)]+)\)", heading.group())
                self.assertEqual(len(links), 1)
                figure = FIGURES / filename
                # Markdown links are relative to the Markdown file; manifest figures
                # are relative to the LaTeX corpus root.
                self.assertEqual((PAPER.parent / links[0]).resolve(), figure.resolve())
                registered = [entry for entry in self.record["figure_files"]
                              if (LATEX_ROOT / entry["path"]).resolve() == figure.resolve()]
                self.assertEqual(len(registered), 1)
                self.assertEqual(registered[0]["expected_occurrences"], 2)
                self.assertTrue(figure.is_file())

    def test_figure_sources_are_vector_tikz_without_embedded_rasters(self):
        for filename in EXPECTED.values():
            with self.subTest(filename=filename):
                source = (FIGURES / filename).read_text(encoding="utf-8")
                self.assertEqual(source.count(r"\begin{tikzpicture}"), 1)
                self.assertEqual(source.count(r"\end{tikzpicture}"), 1)
                self.assertNotIn(r"\includegraphics", source)

    def test_geometry_diagram_keeps_only_given_relations_and_labels(self):
        source = (FIGURES / EXPECTED[8]).read_text(encoding="utf-8")
        for label in ("A", "B", "C", "D", "E"):
            self.assertRegex(source, rf"node(?:\[[^]]*\])?\s*\{{\${label}\$\}}")
        self.assertIn("right angle", source.lower())
        self.assertIn("midpoint", source.lower())
        self.assertIn("perpendicular", source.lower())

    def test_even_function_plot_has_exact_piecewise_landmarks(self):
        source = (FIGURES / EXPECTED[17]).read_text(encoding="utf-8")
        for point in ((-2, 0), (-1, 1), (0, 2), (1, 1), (2, 0)):
            with self.subTest(point=point):
                self.assertIn(f"({point[0]},{point[1]})", source.replace(" ", ""))

    def test_ellipse_diagram_preserves_equation_and_named_relationships(self):
        source = (FIGURES / EXPECTED[22]).read_text(encoding="utf-8")
        for label in ("A", "F", "O", "T", "Q"):
            self.assertRegex(source, rf"node(?:\[[^]]*\])?\s*\{{\${label}(?:\([^}}]*\))?\$\}}")
        self.assertIn("\\frac{(y+1)^2}{16}+\\frac{(x-1)^2}{12}=1", source)
        self.assertIn("图不按比例", source)

    @unittest.skipUnless(shutil.which("latexmk"), "latexmk is required for the vector-figure smoke build")
    def test_all_three_figures_compile_and_render_as_pdf_pages(self):
        work_root = ROOT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2000-shanghai-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            inputs = "\n\\newpage\n".join(
                r"\input{" + str(FIGURES / filename) + "}"
                for filename in EXPECTED.values()
            )
            (build_dir / "figures.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1.5cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                + inputs
                + "\n\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                [
                    "latexmk",
                    "-xelatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "figures.tex",
                ],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figures.pdf"
            self.assertTrue(pdf.is_file())
            rendered_prefix = build_dir / "figure"
            subprocess.run(
                ["pdftoppm", "-png", "-r", "120", str(pdf), str(rendered_prefix)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pages = sorted(build_dir.glob("figure-*.png"))
            self.assertEqual(len(pages), 3)
            self.assertTrue(all(page.stat().st_size > 1000 for page in pages))
            if os.environ.get("KEEP_2000_SHANGHAI_FIGURE_REVIEW") == "1":
                review_dir = work_root / "review-2000-shanghai-figures"
                review_dir.mkdir(exist_ok=True)
                for page in pages:
                    shutil.copy2(page, review_dir / page.name)


if __name__ == "__main__":
    unittest.main()
