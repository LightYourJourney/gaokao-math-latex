import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季北京文_试题.md"
INVENTORY = ROOT / "2004/2004_数学真题_春季北京文_图表清单.md"
FIGURES = {
    17: ROOT / "2004/figures/gaokao_2004_beijing_spring_arts_q17_pyramid.tex",
    18: ROOT / "2004/figures/gaokao_2004_beijing_spring_arts_q18_orbit.tex",
}


class BeijingSpring2004ArtsFigureTests(unittest.TestCase):
    def test_source_figures_are_vector_linked_and_preserve_required_labels(self):
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        inventory = INVENTORY.read_text(encoding="utf-8")
        missing = [str(path) for path in FIGURES.values() if not path.is_file()]
        self.assertFalse(missing, f"TikZ source files are missing: {missing}")

        for question, path in FIGURES.items():
            with self.subTest(question=question):
                self.assertTrue(path.is_file(), f"Q{question} TikZ source is missing")
                relative = path.relative_to(ROOT / "2004").as_posix()
                self.assertIn(relative, transcript)
                self.assertIn(f"| {question} |", inventory)
                self.assertIn(relative, inventory)
                source = path.read_text(encoding="utf-8")
                self.assertIn(r"\begin{tikzpicture}", source)
                self.assertIn(r"\end{tikzpicture}", source)
                self.assertNotIn(r"\includegraphics", source)

        q17 = FIGURES[17].read_text(encoding="utf-8")
        for edge in ("(A)--(B)", "(B)--(C)", "(S)--(A)", "(S)--(B)", "(S)--(C)"):
            self.assertIn(edge, q17)
        for edge in ("(A)--(D)", "(D)--(C)", "(S)--(D)"):
            self.assertIn(edge, q17)
        for label in ("A", "B", "C", "D", "S"):
            self.assertIn(f"({label})", q17)

        q18 = FIGURES[18].read_text(encoding="utf-8")
        for label in ("O", "F_1", "F_2", "A", "B"):
            self.assertIn(label, q18)
        self.assertIn("not to scale", q18)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and Poppler are required")
    def test_vector_figures_compile_and_render_without_warnings(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        for question, figure in FIGURES.items():
            with self.subTest(question=question), tempfile.TemporaryDirectory(prefix=f"2004-beijing-q{question}-", dir=work_root) as temp:
                build_dir = Path(temp)
                tex = build_dir / "figure.tex"
                tex.write_text(
                    "\\documentclass{article}\n"
                    "\\usepackage[margin=1cm]{geometry}\n"
                    "\\usepackage{tikz}\n"
                    "\\pagestyle{empty}\n"
                    "\\begin{document}\n"
                    "\\input{" + figure.as_posix() + "}\n"
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
                if os.environ.get("KEEP_2004_BEIJING_ARTS_FIGURES") == "1":
                    review_dir = PROJECT / ".work/review-2004-beijing-arts"
                    review_dir.mkdir(exist_ok=True)
                    shutil.copy2(rendered, review_dir / f"q{question}.png")


if __name__ == "__main__":
    unittest.main()
