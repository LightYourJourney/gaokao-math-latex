import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER_DIR = PROJECT / "2005_上海春季卷"
sys.path.insert(0, str(PROJECT / "tools"))
import make_short_answers
import solution_sources

TRANSCRIPT = ROOT / "2005/2005_数学真题_春季上海_试题.md"
FIGURES = ROOT / "2005/2005_数学真题_春季上海_图表清单.md"
ANSWER_KEY = ROOT / "2005/2005_数学真题_春季上海_答案要点.md"
SOLUTION_BODY = ROOT / "2005/2005_数学真题_春季上海_解析正文.md"
COMBINED_RENDERED = ROOT / "2005/2005_数学真题_春季上海_含解析.md"
SOURCE_ID = "src-2cd71e4caf6708c2589791bd24ba1b55d6d80d2c08b764a325587c7a991d8c83"
SOURCE_SHA256 = "67d4850cc310a4c089729daf7ff1b8fa3bdacaaaf6b227918669bd0972fb56b5"
FIGURE_PATHS = {
    19: PAPER_DIR / "figures/gaokao_2005_shanghai_spring_q19_pyramid.tex",
    21: PAPER_DIR / "figures/gaokao_2005_shanghai_spring_q21_function.tex",
    22: PAPER_DIR / "figures/gaokao_2005_shanghai_spring_q22_ellipse.tex",
}
CONSTRUCTION_FIGURE = PAPER_DIR / "figures/gaokao_2005_shanghai_spring_q22_center_construction.tex"


class ShanghaiSpring2005TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription draft must exist")
        self.assertTrue(FIGURES.is_file(), "the source-figure inventory must exist")
        self.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        self.figures = FIGURES.read_text(encoding="utf-8")

    def test_fixed_source_fingerprint_is_traceable_and_bound_to_the_paper(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], "春季高考/2005/2005春季上海.pdf")
        self.assertEqual(source["paper_id"], "gk-2005-spring-shanghai")
        self.assertEqual(source["paper_relation"], "canonical")
        self.assertIn(SOURCE_ID, self.transcript)
        self.assertIn(SOURCE_SHA256, self.transcript)
        self.assertIn("原卷印刷页码 217–218", self.transcript)
        self.assertIn("来源已按上游固定文件绑定", self.transcript)
        self.assertNotIn("paper_id 未绑定", self.transcript)

    def test_formal_registration_is_complete_with_verified_source(self):
        paper_id = "gk-2005-spring-shanghai"
        paper = next(
            (item for item in self.manifest["papers"] if item["paper_id"] == paper_id),
            None,
        )
        self.assertIsNotNone(paper, "the 2005 spring Shanghai project must be registered")
        self.assertEqual(paper["project_dir"], "2005_上海春季卷")
        self.assertEqual(paper["question_count"], 22)
        self.assertEqual(paper["production_state"], "complete")
        self.assertEqual(paper["source_ids"], [SOURCE_ID])
        self.assertIn("Q1–22 分段异人盲核已完成", paper["index_metadata"]["note"])
        self.assertIn("来源已按上游固定 blob/卷标题绑定", paper["index_metadata"]["note"])
        self.assertIn("Q21 示意曲线已修订并经局部复核", paper["index_metadata"]["note"])
        self.assertEqual(paper["index_metadata"]["structure"], {
            "填空题": [1, 12], "选择题": [13, 16], "解答题": [17, 22],
        })
        figures = {
            item["path"]: item["expected_occurrences"]
            for item in paper["figure_files"]
        }
        self.assertEqual(figures, {
            "2005_上海春季卷/figures/gaokao_2005_shanghai_spring_q19_pyramid.tex": 2,
            "2005_上海春季卷/figures/gaokao_2005_shanghai_spring_q21_function.tex": 2,
            "2005_上海春季卷/figures/gaokao_2005_shanghai_spring_q22_ellipse.tex": 2,
            "2005_上海春季卷/figures/gaokao_2005_shanghai_spring_q22_center_construction.tex": 1,
        })

    def test_generated_source_note_has_no_unsafe_inline_identifier(self):
        questions_tex = (PAPER_DIR / "questions.tex").read_text(encoding="utf-8")
        self.assertNotIn(r"\texttt{paper_id}", questions_tex)
        self.assertIn("已进入正式 LaTeX 四版本构建流程", questions_tex)

    def test_all_22_questions_and_source_sections_are_present(self):
        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("## 一、填空题"), 1)
        self.assertEqual(self.transcript.count("## 二、选择题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertEqual(self.transcript.count("$") % 2, 0)

    def test_high_risk_math_and_wording_match_the_fixed_source(self):
        normalized = self.transcript.replace(r"\dfrac", r"\frac")
        for source_detail in (
            r"\lg x^2-\lg(x+2)=0",
            r"\frac{n+2}{1+2+\cdots+n}",
            r"\cos\alpha=\frac35",
            r"f(x)=-x^2",
            r"x\in(-\infty,-2]",
            r"\overrightarrow{BA}\cdot\overrightarrow{BC}",
            r"9x^2-16y^2=1",
            r"(x+2)^n=x^n+\cdots+ax^3+bx^2+cx+2^n",
            r"3\cos 2\pi x=3^x",
            r"y=\sin x+\arcsin x",
            r"f(x)=2^x+\log_2 x",
            r"m\parallel n",
            r"\frac{a}{\cos A}=\frac{b}{\cos B}=\frac{c}{\cos C}",
            r"b^2-4ac<0",
            r"\frac{z}{2-i}",
            r"x^2+2x\sec\alpha+1=0",
            r"72\sqrt3",
            r"1200\text{ 万平方米}",
            r"f(2)=2+\frac{\sqrt2}{2}",
            r"\frac{x^2}{a^2}+\frac{y^2}{b^2}=1\ (a>b>0)",
        ):
            self.assertIn(source_detail, normalized)
        self.assertIn(r"a_n=0.1n", self.transcript)
        self.assertIn(r"\tan\alpha", self.transcript)
        self.assertIn("较小的根", self.transcript)
        self.assertIn("Q1–22 为编者独立推导（非官方）", self.transcript)

    def test_derived_answers_are_nonofficial_and_cover_all_questions(self):
        self.assertTrue(ANSWER_KEY.is_file(), "derived answer key must be kept separate from the source transcript")
        self.assertTrue(SOLUTION_BODY.is_file(), "derived solutions must be traceable as a separate artifact")
        answer_key = ANSWER_KEY.read_text(encoding="utf-8")
        solution_body = SOLUTION_BODY.read_text(encoding="utf-8")
        self.assertIn("非官方标准答案", answer_key)
        self.assertIn("官方答案页缺失", answer_key)
        self.assertIn("分段异人盲核已完成", answer_key)
        self.assertIn("分段异人盲核已完成", solution_body)
        self.assertIn("q22_center_construction.tex", solution_body)
        self.assertEqual(
            [int(number) for number in re.findall(r"^\*\*(\d+)．\*\*", answer_key, re.M)],
            list(range(1, 23)),
        )
        self.assertEqual(
            [int(number) for number in re.findall(r"^### 第 (\d+) 题$", solution_body, re.M)],
            list(range(1, 23)),
        )

    def test_derived_answers_follow_the_formal_renderer_contract(self):
        answer_key = ANSWER_KEY.read_text(encoding="utf-8")
        parsed = solution_sources.parse_answer_points(answer_key)
        self.assertEqual([point.number for point in parsed], list(range(1, 23)))
        expected = [
            ((None, r"$\{-1,2\}$"),),
            ((None, "$0$"),),
            ((None, r"$\dfrac12$"),),
            ((None, r"$f^{-1}(x)=-\sqrt{-x}\ (x\le-4)$"),),
            ((None, "$16$"),),
            ((None, r"$\dfrac1{260}$"),),
            ((None, r"$\dfrac56$"),),
            ((None, "$11$"),),
            ((None, "①②③"),),
            ((None, r"$\{1\}$"),),
            ((None, r"$[-\dfrac\pi2-\sin1,\dfrac\pi2+\sin1]$"),),
            ((None, "$110$"),),
            ((None, "D"),),
            ((None, "B"),),
            ((None, "A"),),
            ((None, "C"),),
            ((None, "$2<a<6$"),),
            ((None, r"$\alpha=\dfrac{7\pi}{6}+2k\pi\ (k\in\mathbb{Z})$"),),
            ((1, r"$PA\perp BC$"), (2, "$3$")),
            ((1, "$1240$、$1282$"), (2, "$2522.64$ 万平方米")),
            ((1, r"$a=\sqrt2$"), (2, "定值为 $1$"), (3, r"面积最小值为 $1+\sqrt2$")),
            ((1, r"$\dfrac{x^2}{8}+\dfrac{y^2}{4}=1$"),
             (2, "弦中点轨迹为过原点的定直线"), (3, "作图见解析")),
        ]
        self.assertEqual([point.answers for point in parsed], expected)

    def test_choice_quick_table_matches_questions_13_through_16(self):
        answer_key = ANSWER_KEY.read_text(encoding="utf-8")
        records = make_short_answers.expected_answer_records(answer_key)
        answers = {
            record.number: record.value
            for record in records if record.subpart is None
        }
        structure = (
            ("填空题", 1, 12),
            ("选择题", 13, 16),
            ("解答题", 17, 22),
        )
        self.assertEqual(
            make_short_answers.cross_check_quick_table(answer_key, structure, answers),
            (),
        )

    def test_combined_markdown_is_deterministic_from_canonical_sources(self):
        questions = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWER_KEY.read_text(encoding="utf-8")
        raw_solutions = SOLUTION_BODY.read_text(encoding="utf-8")
        solution = solution_sources.extract_solution_blocks(raw_solutions, questions)
        expected = solution_sources.render_combined(questions, solution, answers)
        self.assertTrue(COMBINED_RENDERED.is_file(), "combined Markdown must be generated")
        self.assertEqual(COMBINED_RENDERED.read_text(encoding="utf-8"), expected)

    def test_question_13_uses_line_parallel_to_plane_in_options_b_and_d(self):
        question = self.transcript.split("**13．**", 1)[1].split("**14．**", 1)[0]
        self.assertEqual(question.count(r"n\parallel\alpha"), 2)
        self.assertNotIn(r"n\subset\alpha", question)

    def test_every_source_figure_has_a_vector_source_and_no_raster_embedding(self):
        self.assertIn("第 19 题", self.figures)
        self.assertIn("第 21 题", self.figures)
        self.assertIn("第 22 题", self.figures)
        for question, path in FIGURE_PATHS.items():
            relative_path = os.path.relpath(path, TRANSCRIPT.parent)
            self.assertIn(str(relative_path), self.transcript)
            self.assertIn(str(relative_path), self.figures)
            self.assertTrue(path.is_file(), f"missing vector figure for Q{question}")
            source = path.read_text(encoding="utf-8")
            self.assertIn(r"\begin{tikzpicture}", source)
            self.assertNotIn(r"\includegraphics", source)
        pyramid = FIGURE_PATHS[19].read_text(encoding="utf-8")
        self.assertIn(r"\draw[dashed] (A)--(C) (P)--(O);", pyramid)
        self.assertIn(r"\draw (A)--(B)--(C) (P)--(A) (P)--(B) (P)--(C);", pyramid)

        function_figure = FIGURE_PATHS[21].read_text(encoding="utf-8")
        coordinates = {
            name: (float(x), float(y))
            for name, x, y in re.findall(
                r"\\coordinate \((\w+)\) at \((-?[0-9.]+),(-?[0-9.]+)\);",
                function_figure,
            )
        }
        px, py = coordinates["P"]
        nx, ny = coordinates["N"]
        mx, my = coordinates["M"]
        self.assertEqual(nx, 0)
        self.assertAlmostEqual(py, ny)
        self.assertAlmostEqual(mx, my)
        self.assertAlmostEqual(px + py, mx + my)
        self.assertAlmostEqual(px, 2.0)
        self.assertAlmostEqual(py, 2.0 + math.sqrt(2) / 2, places=5)
        self.assertIn(
            r"plot[domain=0.42:3.55,samples=80,variable=\x] ({\x},{\x+sqrt(2)/\x})",
            function_figure,
        )
        self.assertAlmostEqual(py, px + math.sqrt(2) / px, places=5)

        ellipse = FIGURE_PATHS[22].read_text(encoding="utf-8")
        self.assertNotIn(r"\node", ellipse)
        self.assertNotIn(r"\coordinate", ellipse)
        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")
        self.assertTrue(CONSTRUCTION_FIGURE.is_file(), "Q22 answer construction diagram must be a TikZ source")
        construction = CONSTRUCTION_FIGURE.read_text(encoding="utf-8")
        self.assertIn(r"\begin{tikzpicture}", construction)
        self.assertNotIn(r"\includegraphics", construction)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and Poppler are required")
    def test_vector_figures_compile_and_render_together(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2005-shanghai-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            inputs = "\n".join(
                r"\input{" + str(path) + "}"
                for path in [*FIGURE_PATHS.values(), CONSTRUCTION_FIGURE]
            )
            (build_dir / "figures.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{tikz}\n"
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
                ["pdftoppm", "-singlefile", "-png", "-r", "140", str(pdf), str(build_dir / "figures")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            self.assertGreater((build_dir / "figures.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2005_SHANGHAI_FIGURE_REVIEW") == "1":
                review_dir = PROJECT / ".work/review-2005-shanghai-spring"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(build_dir / "figures.png", review_dir / "figures.png")


if __name__ == "__main__":
    unittest.main()
