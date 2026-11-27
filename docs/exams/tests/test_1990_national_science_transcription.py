import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = ROOT / "1990/1990_数学真题_全国理_试题.md"
ANSWER_KEY = ROOT / "1990/1990_数学真题_全国理_答案要点.md"
SOLUTION_BODY = ROOT / "1990/1990_数学真题_全国理_解析正文.md"
PROJECT_DIR = PROJECT / "1990_全国卷_理科"
QUESTIONS_TEX = PROJECT_DIR / "questions.tex"
ANSWERS_TEX = PROJECT_DIR / "answers.tex"
ANSWERS_SHORT_TEX = PROJECT_DIR / "answers_short.tex"
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
import make_short_answers
from solution_sources import parse_answer_points


EXPECTED_ANSWERS = {
    1: "A",
    2: "B",
    3: "D",
    4: "C",
    5: "C",
    6: "B",
    7: "A",
    8: "D",
    9: "B",
    10: "D",
    11: "C",
    12: "B",
    13: "B",
    14: "C",
    15: "D",
    16: r"$y=\pm\dfrac{16}{5}$",
    17: r"$-20$",
    18: r"$2$",
    19: r"$\sqrt2+\dfrac12$",
    20: r"待核（靠 $A$ 侧:其余=$7:5$；$V_1,V_2$ 对应未标）",
    21: r"$(0,4,8,16)$ 或 $(15,9,3,1)$",
    22: r"$\dfrac{24}{7}$",
    23: r"$60^\circ$",
    24: r"$z=\pm(\sqrt{1+a}-1)$；当 $0\le a\le1$ 时另有 $z=\pm i(1\pm\sqrt{1-a})$",
    25: r"椭圆方程为 $\dfrac{x^2}{4}+y^2=1$；所求点为 $(\pm\sqrt3,-\dfrac12)$",
    26: r"统一对所有 $n\ge2$：$a>-\dfrac12$；固定 $n$ 时：$a>-\dfrac{n-1}{2}$；不等式证明见解析",
}


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

    def test_answer_and_solution_sources_are_editor_derived_not_official(self):
        self.assertTrue(ANSWER_KEY.is_file(), f"missing answer key: {ANSWER_KEY}")
        self.assertTrue(SOLUTION_BODY.is_file(), f"missing solution body: {SOLUTION_BODY}")
        answer_text = ANSWER_KEY.read_text(encoding="utf-8")
        solution_text = SOLUTION_BODY.read_text(encoding="utf-8")
        self.assertRegex(answer_text, r"(?m)^official_answer:\s*null\s*$")
        self.assertIn("编者自行推导，非官方答案", answer_text)
        self.assertIn("编者自行推导，非来源印载解析", solution_text)
        self.assertIn("独立盲核已逐题完成", answer_text)
        self.assertIn("独立盲解已逐题提供", solution_text)
        self.assertNotIn("盲核尚待独立复核", answer_text)
        self.assertNotIn("独立盲解报告尚未提供", solution_text)
        self.assertRegex(answer_text, r"(?m)^状态:\s*pending\s*$")
        self.assertRegex(solution_text, r"(?m)^状态:\s*pending\s*$")

    def test_answer_key_covers_all_questions_with_independently_derived_results(self):
        self.assertTrue(ANSWER_KEY.is_file(), f"missing answer key: {ANSWER_KEY}")
        text = ANSWER_KEY.read_text(encoding="utf-8")
        points = parse_answer_points(text)
        self.assertEqual([point.number for point in points], list(range(1, 27)))
        actual = {point.number: point.answers[0][1] for point in points}
        self.assertEqual(actual, EXPECTED_ANSWERS)
        self.assertEqual(
            make_short_answers.parse_quick_table(text, 15),
            ("A", "B", "D", "C", "C", "B", "A", "D", "B", "D", "C", "B", "B", "C", "D"),
        )

    def test_solution_conclusions_cover_all_questions_and_match_the_answer_key(self):
        self.assertTrue(SOLUTION_BODY.is_file(), f"missing solution body: {SOLUTION_BODY}")
        text = SOLUTION_BODY.read_text(encoding="utf-8")
        sections = re.split(r"(?m)^### 第 (\d+) 题\s*$", text)
        actual_numbers = [int(sections[index]) for index in range(1, len(sections), 2)]
        self.assertEqual(actual_numbers, list(range(1, 27)))
        for index in range(1, len(sections), 2):
            number = int(sections[index])
            body = sections[index + 1]
            conclusion = re.search(r"(?m)^\*\*结论：(.+?)\*\*\s*$", body)
            with self.subTest(question=number):
                self.assertIsNotNone(conclusion, f"Q{number} lacks a final conclusion")
                self.assertEqual(conclusion.group(1), EXPECTED_ANSWERS[number])

    def test_q20_reports_only_the_unordered_ratio_and_preserves_label_ambiguity(self):
        self.assertTrue(ANSWER_KEY.is_file(), f"missing answer key: {ANSWER_KEY}")
        self.assertTrue(SOLUTION_BODY.is_file(), f"missing solution body: {SOLUTION_BODY}")
        answer_text = ANSWER_KEY.read_text(encoding="utf-8")
        solution_text = SOLUTION_BODY.read_text(encoding="utf-8")
        answer_section = re.split(r"(?m)^\*\*20．\*\*\s*$", answer_text)[1].split("**21．**", 1)[0]
        solution_section = re.split(r"(?m)^### 第 20 题\s*$", solution_text)[1].split("### 第 21 题", 1)[0]
        for text in (answer_section, solution_section):
            self.assertIn("7:5", text)
            self.assertIn("V_1", text)
            self.assertIn("V_2", text)
            self.assertIn("未标", text)
            self.assertNotRegex(text, r"V_1\s*:\s*V_2\s*=\s*(?:7:5|5:7)")

    def test_generated_project_tex_and_short_answers_match_their_source_contracts(self):
        for path in (ANSWER_KEY, SOLUTION_BODY, ANSWERS_TEX, ANSWERS_SHORT_TEX):
            self.assertTrue(path.is_file(), f"missing answer-stage artifact: {path}")

        figure_files = tuple(
            (f"1990_全国卷_理科/figures/{name}", 2)
            for name in sorted(FIGURES)
        )
        sources = generate_projects.ProjectSources(
            paper_id="gk-1990-regular-national-science",
            project_dir="1990_全国卷_理科",
            title="1990 年·全国卷·理科",
            question_count=26,
            questions=PAPER.relative_to(ROOT).as_posix(),
            answer_key=ANSWER_KEY.relative_to(ROOT).as_posix(),
            solution_body=SOLUTION_BODY.relative_to(ROOT).as_posix(),
            figures=figure_files,
        )
        generated = generate_projects.generate_project(ROOT, sources)
        self.assertEqual(generate_projects.validate_project_result(sources, generated), ())
        questions_target = "math-gaokao-latex/1990_全国卷_理科/questions.tex"
        self.assertEqual(generated.targets[questions_target], QUESTIONS_TEX.read_bytes())
        answers_target = "math-gaokao-latex/1990_全国卷_理科/answers.tex"
        self.assertEqual(generated.targets[answers_target], ANSWERS_TEX.read_bytes())

        short_sources = make_short_answers.ShortAnswerSources(
            paper_id=sources.paper_id,
            project_dir=sources.project_dir,
            title=sources.title,
            question_count=26,
            questions=sources.questions,
            answer_key=sources.answer_key,
            answers_tex=answers_target,
            structure=(("选择题", 1, 15), ("填空题", 16, 20), ("解答题", 21, 26)),
        )
        short_generated, problems = make_short_answers.generate_short_answers(ROOT, short_sources)
        self.assertEqual(problems, ())
        short_target = "math-gaokao-latex/1990_全国卷_理科/answers_short.tex"
        self.assertEqual(short_generated.targets[short_target], ANSWERS_SHORT_TEX.read_bytes())

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

if __name__ == "__main__":
    unittest.main()
