"""1998 上海文科原卷插图必须是可追溯、可编译的矢量图。"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = PROJECT / "1998_上海卷_文科"
QUESTIONS = PAPER / "题面转录草稿.md"
FIGURES = {
    "q06": ("f1998_shanghai_arts_q06_flowchart.tex", "第6题工序流程图"),
    "q19": ("f1998_shanghai_arts_q19_prism.tex", "第19题直四棱柱图"),
    "q20": ("f1998_shanghai_arts_q20_parabola.tex", "第20题抛物线与直线图"),
}


class Shanghai1998ArtsFigureTests(unittest.TestCase):
    def test_question_transcription_links_every_source_vector_figure(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        for name, (filename, label) in FIGURES.items():
            with self.subTest(figure=name):
                self.assertTrue(f"](figures/{filename})" in text, f"missing question link: {filename}")
                self.assertTrue(label in text, f"missing source-page label: {label}")
                self.assertTrue((PAPER / "figures" / filename).is_file(), f"missing figure source: {filename}")

    def test_diagrams_retain_source_labels_without_raster_inclusion(self):
        expected = {
            "q06": ("{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "a", "b", "c", "d", "e", "f", "g", "m", "n", "p"),
            "q19": ("$A$", "$B$", "$C$", "$D$", "$A_1$", "$B_1$", "$C_1$", "$D_1$", "$O$", "$O_1$", "$E$"),
            "q20": ("$x$", "$y$", "$O$", "$D$", "$E$", "$P$", "$Q$", "$y^2=4(x-1)$"),
        }
        for name, (filename, _) in FIGURES.items():
            with self.subTest(figure=name):
                path = PAPER / "figures" / filename
                if not path.is_file():
                    self.fail(f"missing figure source: {filename}")
                    continue
                source = path.read_text(encoding="utf-8")
                for label in expected[name]:
                    self.assertIn(label, source)
                self.assertNotIn(r"\includegraphics", source)
                self.assertIn("不按比例", source)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and pdftoppm are required")
    def test_all_three_figures_compile_and_render_as_nonempty_pages(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="1998-shanghai-arts-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            body = (r"\clearpage" + "\n").join(
                r"\input{" + str(PAPER / "figures" / FIGURES[key][0]) + "}" for key in FIGURES
            )
            (build_dir / "figures.tex").write_text(
                "\n".join((
                    r"\documentclass{article}",
                    r"\usepackage[margin=1.5cm]{geometry}",
                    r"\usepackage{tikz}",
                    r"\pagestyle{empty}",
                    r"\begin{document}", body, r"\end{document}",
                )) + "\n",
                encoding="utf-8",
            )
            try:
                subprocess.run(
                    ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figures.tex"],
                    cwd=build_dir, check=True, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, timeout=120,
                )
            except subprocess.CalledProcessError as exc:
                self.fail(f"latexmk rejected one of the source-vector figures:\n{exc.stdout[-4000:]}")
            subprocess.run(
                ["pdftoppm", "-png", "-r", "150", "figures.pdf", "figures"],
                cwd=build_dir, check=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            pages = sorted(build_dir.glob("figures-*.png"))
            self.assertEqual(len(pages), 3)
            self.assertTrue(all(page.stat().st_size > 2000 for page in pages))
            if os.environ.get("KEEP_1998_SHANGHAI_ARTS_FIGURES") == "1":
                for index, page in enumerate(pages, 1):
                    shutil.copy2(page, PROJECT / f".work/review-1998-shanghai-arts-figures-{index}.png")


if __name__ == "__main__":
    unittest.main()
