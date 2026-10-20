"""Vector figure guards for the 1999 Shanghai science draft."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = PROJECT / "1999_上海卷_理科"
QUESTIONS = PAPER / "题面转录草稿.md"
FIGURES = {
    20: PAPER / "figures/1999_shanghai_science_q20_pyramid.tex",
    21: PAPER / "figures/1999_shanghai_science_q21_canal.tex",
}


class Shanghai1999ScienceFigureTests(unittest.TestCase):
    def test_question_links_resolve_to_local_tex_only(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        for number, figure in FIGURES.items():
            with self.subTest(question=number):
                expected = f"](figures/{figure.name})"
                self.assertTrue(expected in questions, f"Q{number} is missing its local TeX figure link")
                self.assertTrue(figure.is_file())
        self.assertNotRegex(questions, r"!\[[^]]*\]\([^)]*\.(?:png|jpe?g)\)")

    @unittest.skipUnless(all(path.is_file() for path in FIGURES.values()), "figure sources are not implemented yet")
    def test_q20_pyramid_topology_and_q21_channel_profile_are_recorded(self):
        q20 = FIGURES[20].read_text(encoding="utf-8")
        q21 = FIGURES[21].read_text(encoding="utf-8")
        for label in ("$P$", "$A$", "$B$", "$C$", "$D$", "$E$"):
            with self.subTest(q20_label=label):
                self.assertIn(label, q20)
        for segment in (r"(P)--(A)", r"(P)--(B)", r"(P)--(C)", r"(P)--(D)", r"(A)--(E)"):
            with self.subTest(q20_segment=segment):
                self.assertIn(segment, q20)
        self.assertIn(r"(A) .. controls", q21)
        self.assertIn(r"(O) .. controls", q21)
        self.assertIn(r"\draw[hidden edge] (A)--(B);", q21)
        for label in ("$A$", "$B$", "$O$"):
            with self.subTest(q21_label=label):
                self.assertIn(label, q21)
        for source in (q20, q21):
            self.assertIn("不按比例", source)
            self.assertNotIn(r"\includegraphics", source)
            self.assertNotRegex(source, r"\.(?:png|jpe?g)")

    @unittest.skipUnless(all(path.is_file() for path in FIGURES.values()) and shutil.which("latexmk") and shutil.which("pdftoppm"), "figure sources and latexmk/pdftoppm are required")
    def test_both_vector_sources_compile_and_render(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        for number, figure in FIGURES.items():
            with self.subTest(question=number):
                with tempfile.TemporaryDirectory(
                    prefix=f"1999-shanghai-science-q{number}-",
                    dir=work_root,
                ) as temp:
                    build_dir = Path(temp)
                    (build_dir / "figure.tex").write_text(
                        "\n".join((
                            r"\documentclass[tikz,border=4mm]{standalone}",
                            r"\usepackage{ctex}",
                            r"\usepackage{tikz}",
                            r"\begin{document}",
                            r"\input{" + str(figure) + "}",
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
                        self.fail(f"latexmk rejected Q{number} vector source:\n{exc.stdout[-4000:]}")
                    subprocess.run(
                        ["pdftoppm", "-png", "-r", "150", "figure.pdf", "figure"],
                        cwd=build_dir, check=True, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True, timeout=120,
                    )
                    pages = sorted(build_dir.glob("figure-*.png"))
                    self.assertEqual(len(pages), 1)
                    self.assertGreater(pages[0].stat().st_size, 2000)
                    if os.environ.get("KEEP_1999_SHANGHAI_SCIENCE_FIGURES") == "1":
                        shutil.copy2(pages[0], PROJECT / f".work/review-1999-shanghai-science-q{number}.png")


if __name__ == "__main__":
    unittest.main()
