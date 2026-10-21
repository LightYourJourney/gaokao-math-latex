import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = ROOT / "1990/1990_数学真题_全国文_试题.md"
FIGURE_DIR = PROJECT / "1990_全国卷_文科/figures"
SOURCE_ID = "src-4d319a8fc41be0c0fa7ce90615870abbabe5c3670150609e3cb0c37944091866"
SOURCE_SHA256 = "89b85ba17cf8bbd3dcce6b88fd6b819e218b7d4dca2f043692ad10b2961aa029"


class NationalArts1990TranscriptionTests(unittest.TestCase):
    def test_question_draft_pins_fixed_source_and_has_all_26_questions_in_order(self):
        self.assertTrue(PAPER.is_file(), f"missing question draft: {PAPER}")
        text = PAPER.read_text(encoding="utf-8")
        self.assertIn(SOURCE_ID, text)
        self.assertIn(SOURCE_SHA256, text)
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．\*\*", text, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 27)))
        self.assertIn("PDF 不含答案页", text)
        self.assertNotIn("官方答案", text[text.index("## 试题"):])
        self.assertIn("固定源图未标示哪一部分对应 $V_1$ 或 $V_2$", text)

    def test_linked_figures_exist_as_vector_tex_without_committed_rasters(self):
        self.assertTrue(PAPER.is_file(), f"missing question draft: {PAPER}")
        text = PAPER.read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)]+\.tex)\)", text)
        self.assertEqual(len(links), 4)
        self.assertEqual({Path(link).name for link in links}, {
            "f1990_national_arts_q06_sine.tex",
            "f1990_national_arts_q14_tetrahedron.tex",
            "f1990_national_arts_q20_prism.tex",
            "f1990_national_arts_q23_pyramid.tex",
        })
        for link in links:
            target = (PAPER.parent / link).resolve()
            with self.subTest(figure=target.name):
                self.assertTrue(target.is_file(), f"broken figure link: {link}")
                self.assertEqual(target.suffix, ".tex")
                self.assertIn(r"\begin{tikzpicture}", target.read_text(encoding="utf-8"))
        raster_files = [
            path for path in FIGURE_DIR.rglob("*")
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
        ]
        self.assertEqual(raster_files, [])

    def test_prism_occluded_edges_and_cut_plane_segments_are_dashed(self):
        figure = FIGURE_DIR / "f1990_national_arts_q20_prism.tex"
        self.assertTrue(figure.is_file(), f"missing source-vector figure: {figure}")
        source = figure.read_text(encoding="utf-8")
        draw_commands = re.findall(r"\\draw(?:\[([^]]*)\])?\s*([^;]+);", source)

        def styles_of(segment):
            left, right = re.findall(r"\(([^)]+)\)", segment)
            edge = frozenset((left, right))
            matches = []
            for style, path in draw_commands:
                points = re.findall(r"\(([^)]+)\)", path)
                edges = {frozenset(pair) for pair in zip(points, points[1:])}
                if edge in edges:
                    matches.append(style)
            self.assertTrue(matches, f"no draw command found for {segment}")
            return matches

        for segment in ("(A)--(C)", "(C)--(Cone)", "(C)--(B)", "(Cone)--(F)", "(F)--(E)"):
            with self.subTest(segment=segment):
                self.assertTrue(any("dashed" in style for style in styles_of(segment)))
        self.assertTrue(all("dashed" not in style for style in styles_of("(E)--(Bone)")))
        self.assertTrue(all("dashed" not in style for style in styles_of("(Bone)--(Cone)")))

    @unittest.skipUnless(shutil.which("xelatex") and shutil.which("pdftoppm"), "XeLaTeX and Poppler are required")
    def test_all_four_vector_figures_compile_and_render(self):
        links = sorted(FIGURE_DIR.glob("*.tex"))
        self.assertEqual(len(links), 4)
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="1990-national-arts-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            body = [
                r"\documentclass{article}",
                r"\usepackage[margin=2cm]{geometry}",
                r"\usepackage{amsmath}",
                r"\usepackage{tikz}",
                r"\pagestyle{empty}",
                r"\begin{document}",
            ]
            for index, figure in enumerate(links):
                body.append(r"\noindent\input{" + str(figure) + "}")
                if index != len(links) - 1:
                    body.append(r"\clearpage")
            body.append(r"\end{document}")
            (build_dir / "figures.tex").write_text("\n".join(body) + "\n", encoding="utf-8")
            try:
                subprocess.run(
                    ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", str(build_dir), "figures.tex"],
                    cwd=build_dir, check=True, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, timeout=120,
                )
            except subprocess.CalledProcessError as exc:
                self.fail(f"XeLaTeX rejected the real figure sources:\n{exc.stdout[-4000:]}")
            subprocess.run(
                ["pdftoppm", "-png", "-r", "120", str(build_dir / "figures.pdf"), str(build_dir / "figure")],
                cwd=build_dir, check=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            pages = sorted(build_dir.glob("figure-*.png"))
            self.assertEqual(len(pages), 4)
            self.assertTrue(all(page.stat().st_size > 1000 for page in pages))
            if os.environ.get("KEEP_1990_NATIONAL_ARTS_FIGURES") == "1":
                review_dir = PROJECT / ".work/review-1990-national-arts"
                review_dir.mkdir(exist_ok=True)
                for page in pages:
                    shutil.copy2(page, review_dir / page.name)


if __name__ == "__main__":
    unittest.main()
