import re
import math
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
PAPER = REPO / "2000/2000_数学真题_春季北京安徽理_试题.md"
ANSWERS = REPO / "2000/2000_数学真题_春季北京安徽理_答案要点.md"
SOLUTIONS = REPO / "2000/2000_数学真题_春季北京安徽理_解析正文.md"
FIGURES = REPO / "2000/figures"
FIGURE_FILES = {
    14: "gaokao_2000_spring_beijing_anhui_science_q14_cubic.tex",
    20: "gaokao_2000_spring_beijing_anhui_science_q20_fold.tex",
    22: "gaokao_2000_spring_beijing_anhui_science_q22_locus.tex",
    24: "gaokao_2000_spring_beijing_anhui_science_q24_axes.tex",
}


class BeijingAnhuiSpring2000TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PAPER.read_text(encoding="utf-8")

    def test_source_identity_and_unbound_metadata(self):
        self.assertIn("paper_id: null", self.text)
        self.assertIn("official_answer: null", self.text)
        self.assertIn(
            "source_id: src-a0269cc0034b8f71793418f0abb911e424058f04f18389e6ff78004045ca1eba",
            self.text,
        )
        self.assertIn(
            "source_sha256: 37f07244497aa0a21be12d8a31eac78b61490f835f088719a5990463585a35ce",
            self.text,
        )
        self.assertIn("来源出版信息: 未知", self.text)
        self.assertIn("来源版本: 未知", self.text)

    def test_all_question_numbers_are_present_once_in_order(self):
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．\*\*", self.text, re.M)]
        self.assertEqual(numbers, list(range(1, 25)))
        self.assertEqual(self.text.count("## 一、选择题"), 1)
        self.assertEqual(self.text.count("## 二、填空题"), 1)
        self.assertEqual(self.text.count("## 三、解答题"), 1)

    def test_high_risk_items_and_track_specific_wording_are_present(self):
        for anchor in (
            r"z_1=2\sin\theta",
            r"\dfrac{3\pi}{4}",
            r"\left(\sqrt{x}-\dfrac1{\sqrt[3]{x}}\right)^{10}",
            r"y^2=4px\ (p>0)",
            r"\dfrac12AB=a",
            "0.55",
            "f_1(x)=-2",
            "f_2(x)=-2x+2",
        ):
            self.assertIn(anchor, self.text)
        self.assertNotIn("文科", self.text)
        self.assertIn("sxlg10.gif", self.text)
        self.assertIn("非官方答案来源", self.text)

    def test_choice_options_and_answer_subparts_are_complete(self):
        question_blocks = re.split(r"(?=^\*\*\d+．\*\*)", self.text, flags=re.M)
        for number in range(1, 15):
            block = next(
                item for item in question_blocks
                if item.startswith(f"**{number}．**")
            )
            for option in "ABCD":
                self.assertIn(f"{option}．", block, f"Q{number} missing option {option}")
        for number, expected in ((20, (1, 2)), (23, (1, 2)), (24, (1, 2, 3))):
            block = next(
                item for item in question_blocks
                if item.startswith(f"**{number}．**")
            )
            found = tuple(int(value) for value in re.findall(r"^  \((\d+)\)", block, re.M))
            self.assertEqual(found, expected, f"Q{number} subparts")

    def test_figure_references_resolve_to_vector_sources(self):
        refs = re.findall(r"\]\((figures/[^)]+\.tex)\)", self.text)
        self.assertEqual(len(refs), 4)
        for ref in refs:
            self.assertTrue((PAPER.parent / ref).is_file(), ref)
        self.assertTrue((PAPER.parent / "2000_春季北京安徽_理科_图表清单.md").is_file())
        self.assertEqual(set(Path(ref).name for ref in refs), set(FIGURE_FILES.values()))
        raster_files = [path for path in FIGURES.rglob("*") if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}]
        self.assertEqual(raster_files, [])

    def test_science_q22_figure_obeys_the_stated_geometry(self):
        source = (FIGURES / FIGURE_FILES[22]).read_text(encoding="utf-8")

        def point(label):
            match = re.search(
                rf"\\coordinate \({label}\) at \(([-0-9.]+),([-0-9.]+)\)",
                source,
            )
            self.assertIsNotNone(match, f"missing coordinate {label}")
            return tuple(float(value) for value in match.groups())

        a, b, m = point("A"), point("B"), point("M")
        direction = (b[0] - a[0], b[1] - a[1])
        self.assertAlmostEqual(a[1] ** 2, 2 * a[0], places=6)
        self.assertAlmostEqual(b[1] ** 2, 2 * b[0], places=6)
        self.assertAlmostEqual(a[0] * b[0] + a[1] * b[1], 0, places=6)
        self.assertAlmostEqual(m[0] * direction[0] + m[1] * direction[1], 0, places=6)
        self.assertAlmostEqual(
            (m[0] - a[0]) * direction[1] - (m[1] - a[1]) * direction[0],
            0,
            places=6,
        )
        self.assertFalse(math.isclose(a[0], b[0]))
        self.assertGreater(a[0], b[0])
        self.assertLess(m[1], 0)
        segment_parameter = (
            (m[0] - a[0]) * direction[0] + (m[1] - a[1]) * direction[1]
        ) / (direction[0] ** 2 + direction[1] ** 2)
        self.assertGreater(segment_parameter, 0)
        self.assertLess(segment_parameter, 1)

    def test_science_q20_base_figure_obeys_the_stated_lengths(self):
        source = (FIGURES / FIGURE_FILES[20]).read_text(encoding="utf-8")

        def point(label):
            match = re.search(
                rf"\\coordinate \({label}\) at \(([-0-9.]+),([-0-9.]+)\)",
                source,
            )
            self.assertIsNotNone(match, f"missing base coordinate {label}")
            return tuple(float(value) for value in match.groups())

        a, b, c, d = (point(label) for label in "ABCD")
        distance = lambda first, second: math.hypot(first[0] - second[0], first[1] - second[1])
        self.assertTrue(math.isclose(distance(a, d), distance(d, c)))
        self.assertTrue(math.isclose(distance(a, b), 2 * distance(a, d)))

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and Poppler are required")
    def test_all_science_tikz_sources_compile_and_render(self):
        work_root = REPO / "math-gaokao-latex/.work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2000-beijing-anhui-science-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            inputs = "\n\\newpage\n".join(
                r"\input{" + (FIGURES / filename).as_posix() + "}"
                for filename in FIGURE_FILES.values()
            )
            (build_dir / "figures.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1.5cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\usepackage{pgfplots}\n"
                "\\pgfplotsset{compat=1.18}\n"
                "\\usepackage{xeCJK}\n"
                "\\setCJKmainfont{Songti SC}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                + inputs
                + "\n\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figures.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figures.pdf"
            self.assertTrue(pdf.is_file())
            subprocess.run(
                ["pdftoppm", "-png", "-r", "120", str(pdf), str(build_dir / "figure")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pages = sorted(build_dir.glob("figure-*.png"))
            self.assertEqual(len(pages), len(FIGURE_FILES))
            self.assertTrue(all(page.stat().st_size > 1000 for page in pages))

    def test_no_answers_or_solutions_were_added(self):
        self.assertNotIn("## 答案", self.text)
        self.assertNotIn("## 解析", self.text)
        self.assertIn("本稿不转录其中解答", self.text)

    def test_independent_answer_and_solution_drafts_cover_all_questions(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        for document in (answers, solutions):
            self.assertIn(
                "source_id: src-a0269cc0034b8f71793418f0abb911e424058f04f18389e6ff78004045ca1eba",
                document,
            )
            self.assertIn(
                "source_sha256: 37f07244497aa0a21be12d8a31eac78b61490f835f088719a5990463585a35ce",
                document,
            )
            self.assertIn("official_answer: null", document)
            self.assertIn("solution_status: draft-independent-solutions-pending-cross-check", document)
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．\*\*", solutions, re.M)]
        self.assertEqual(numbers, list(range(1, 25)))
        self.assertIn("| 答案 | D | B | C | D | C | B | B | B | D | B | A | D | C | A |", answers)
        self.assertIn("| 答案 | $3$ | $2\\sqrt2$ | $210$ | ①④ |", answers)
        self.assertIn("填 **①④**", solutions)
        self.assertIn("若允许$a=b$", answers)
        self.assertIn("若不把$a,b$理解为异线", solutions)


if __name__ == "__main__":
    unittest.main()
