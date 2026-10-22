import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = ROOT / "1990/1990_数学真题_全国理_试题.md"
PROJECT_DIR = PROJECT / "1990_全国卷_理科"
QUESTIONS_TEX = PROJECT_DIR / "questions.tex"
FIGURE_DIR = PROJECT_DIR / "figures"
SOURCE_ID = "src-9c2fc92cdbbeac0484bf7355db2d32805c316e1a7be74e3bf175a3891a167a49"
SOURCE_SHA256 = "7801e6dab50ca58eabdc74d074cdaa7012cdee873dcc5304e0df37248986b43a"
FIGURES = {
    "f1990_national_science_q05_sine.tex",
    "f1990_national_science_q11_pyramid.tex",
    "f1990_national_science_q20_prism.tex",
    "f1990_national_science_q23_pyramid.tex",
}

sys.path.insert(0, str(PROJECT / "tools"))
import generate_projects
import md2tex


class NationalScience1990TranscriptionTests(unittest.TestCase):
    def test_fixed_source_and_question_ranges_match_the_printed_paper(self):
        self.assertTrue(PAPER.is_file(), f"missing question draft: {PAPER}")
        text = PAPER.read_text(encoding="utf-8")
        self.assertIn(f"source_id: {SOURCE_ID}", text)
        self.assertIn(f"source_sha256: {SOURCE_SHA256}", text)
        self.assertIn("印刷页: 36", text)
        self.assertIn("PDF 不含答案或解析页", text)

        expected_sections = (
            ("### 一、选择题", "### 二、填空题", list(range(1, 16))),
            ("### 二、填空题", "### 三、解答题", list(range(16, 21))),
            ("### 三、解答题", "", list(range(21, 27))),
        )
        for heading, next_heading, expected in expected_sections:
            start = text.index(heading) + len(heading)
            end = text.index(next_heading, start) if next_heading else len(text)
            numbers = [
                int(value)
                for value in re.findall(r"^\*\*(\d+)．\*\*", text[start:end], re.MULTILINE)
            ]
            self.assertEqual(numbers, expected, heading)

    def test_q9_retains_the_two_complement_overbars(self):
        self.assertTrue(PAPER.is_file(), f"missing question draft: {PAPER}")
        text = PAPER.read_text(encoding="utf-8")
        question = text.split("**9．**", 1)[1].split("**10．**", 1)[0]
        self.assertIn(r"\overline{M}\cap\overline{N}", question)

    def test_q26_a_is_a_coefficient_of_n_to_the_x(self):
        self.assertTrue(PAPER.is_file(), f"missing question draft: {PAPER}")
        text = PAPER.read_text(encoding="utf-8")
        question = text.split("**26．**", 1)[1]
        self.assertIn(r"n^x a", question)
        self.assertNotIn(r"n x^a", question)

    def test_four_source_diagrams_are_linked_tikz_without_raster_files(self):
        self.assertTrue(PAPER.is_file(), f"missing question draft: {PAPER}")
        text = PAPER.read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)]+\.tex)\)", text)
        self.assertEqual(len(links), 4)
        self.assertEqual({Path(link).name for link in links}, FIGURES)

        for link in links:
            target = (PAPER.parent / link).resolve()
            with self.subTest(figure=target.name):
                self.assertTrue(target.is_file(), f"broken figure link: {link}")
                self.assertIn(r"\begin{tikzpicture}", target.read_text(encoding="utf-8"))
        raster_files = [
            path for path in FIGURE_DIR.rglob("*")
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
        ]
        self.assertEqual(raster_files, [])

    def test_q20_keeps_the_volume_label_direction_unresolved(self):
        self.assertTrue(PAPER.is_file(), f"missing question draft: {PAPER}")
        text = PAPER.read_text(encoding="utf-8")
        self.assertIn("V_1:V_2", text)
        self.assertIn("未说明图中哪一部分对应 $V_1$ 或 $V_2$", text)

    def test_q20_prism_places_C_lower_right_of_B1_as_in_the_source(self):
        figure = FIGURE_DIR / "f1990_national_science_q20_prism.tex"
        self.assertTrue(figure.is_file(), f"missing source-vector figure: {figure}")
        coordinates = {
            name: (float(x), float(y))
            for name, x, y in re.findall(
                r"\\coordinate \((\w+)\) at \(([-\d.]+),([-\d.]+)\);",
                figure.read_text(encoding="utf-8"),
            )
        }
        self.assertGreater(coordinates["C"][0], coordinates["Bone"][0])
        self.assertLess(coordinates["C"][1], coordinates["Bone"][1] - 0.5)

    def test_q20_C_label_is_offset_from_the_dashed_edge_intersection(self):
        figure = FIGURE_DIR / "f1990_national_science_q20_prism.tex"
        text = figure.read_text(encoding="utf-8")
        self.assertRegex(text, r"\\node\[above right\] at \(C\) \{\$C\$\};")

    @unittest.skipUnless(shutil.which("xelatex") and shutil.which("pdftoppm"), "XeLaTeX and Poppler are required")
    def test_all_four_vector_figures_compile_and_render_without_raster_inputs(self):
        self.assertTrue(PAPER.is_file(), f"missing question draft: {PAPER}")
        figures = sorted(FIGURE_DIR.glob("*.tex"))
        self.assertEqual({figure.name for figure in figures}, FIGURES)
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="1990-national-science-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            body = [
                r"\documentclass{article}",
                r"\usepackage[margin=2cm]{geometry}",
                r"\usepackage{amsmath}",
                r"\usepackage{tikz}",
                r"\pagestyle{empty}",
                r"\begin{document}",
            ]
            for index, figure in enumerate(figures):
                body.append(r"\noindent\input{" + str(figure) + "}")
                if index != len(figures) - 1:
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
                self.fail(f"XeLaTeX rejected the figure sources:\n{exc.stdout[-4000:]}")
            subprocess.run(
                ["pdftoppm", "-png", "-r", "120", str(build_dir / "figures.pdf"), str(build_dir / "figure")],
                cwd=build_dir, check=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            pages = sorted(build_dir.glob("figure-*.png"))
            self.assertEqual(len(pages), 4)
            self.assertTrue(all(page.stat().st_size > 1000 for page in pages))

    def test_questions_tex_is_the_deterministic_conversion_of_the_question_source(self):
        self.assertTrue(PAPER.is_file(), f"missing question draft: {PAPER}")
        self.assertTrue(QUESTIONS_TEX.is_file(), f"missing generated questions: {QUESTIONS_TEX}")
        text = PAPER.read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)]+\.tex)\)", text)
        figure_map = {link: Path(link).stem for link in links}
        converted = md2tex.convert_markdown(
            text,
            md2tex.ConversionContext(figure_map=figure_map, strict=True),
        )
        wrapped, numbers = generate_projects.wrap(converted.text, "questions")
        self.assertEqual(numbers, list(range(1, 27)))
        expected = (
            "% questions.tex —— 1990 年·全国卷·理科 · 题目内容片段（无答案）\n"
            "% 由 tools/generate_projects.py 依固定源稿生成，待来源登记后重生成\n"
            + wrapped
        )
        self.assertEqual(QUESTIONS_TEX.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
