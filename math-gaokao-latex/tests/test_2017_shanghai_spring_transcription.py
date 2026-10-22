import json
import math
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2017/2017_数学真题_春季上海_试题.md"
FIGURES = ROOT / "2017/2017_数学真题_春季上海_图表清单.md"
ANSWER_KEY = ROOT / "2017/2017_数学真题_春季上海_答案要点.md"
SOLUTION_BODY = ROOT / "2017/2017_数学真题_春季上海_解析正文.md"
SOURCE_ID = "src-480836465b22d00a9a18f0d5cdfe26306df617cbe558553c86a162ef92ea16c9"
SOURCE_SHA256 = "5379de046c452e20504865f84b019a4ad6b8e9edf73c209efe484fcbf68adc37"
sys.path.insert(0, str(PROJECT / "tools"))
import solution_sources


class ShanghaiSpring2017TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def test_fixed_source_fingerprint_is_preserved_without_claiming_official_original(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 4)
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        self.assertEqual(source["upstream_path"], "春季高考/2017/2017春季上海.pdf")

        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription must be committed as a canonical input")
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        self.assertIn(SOURCE_ID, transcript)
        self.assertIn(SOURCE_SHA256, transcript)
        self.assertIn("上游公开副本", transcript)
        self.assertIn("未核验为官方原件", transcript)
        self.assertIn("PDF 第 1–3 页", transcript)

    def test_transcription_covers_all_21_questions_and_preserves_high_risk_notation(self):
        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription must exist before it can be checked")
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 22)))
        self.assertEqual(transcript.count("## 一、填空题"), 1)
        self.assertEqual(transcript.count("## 二、选择题"), 1)
        self.assertEqual(transcript.count("## 三、解答题"), 1)
        normalized = transcript.replace(r"\dfrac", r"\frac")

        for source_detail in (
            r"2\bar z-1=3+6i",
            r"\left(x+\frac2x\right)^n",
            r"\frac{x^2}{2}+y^2=1",
            r"|a_1-a_2|+|a_3-a_4|+|a_5-a_6|=3",
            r"$(1,2)$ 上有两个不同的零点",
            r"\overrightarrow{A_1A_3}\cdot\overrightarrow{A_1P}",
            r"A_1C",
            r"DD_1",
            r"f(x)=\frac{2^x+a}{2^x+1}",
            r"AB\perp AC",
            r"AB=AC=AD=60",
            r"每米 0.8 千元与每米 0.9 千元",
            r"x^2-\frac{y^2}{b^2}=1",
            r"\overrightarrow{NP'}=\frac32\overrightarrow{P'Q}",
            r"(-1)^{n+1}\frac{3x_n-1}{3-x_n}",
        ):
            self.assertIn(source_detail, normalized, f"missing source-critical anchor: {source_detail}")

    def test_source_figures_are_inventoried_as_vector_redraw_work_not_raster_assets(self):
        self.assertTrue(FIGURES.is_file(), "the source diagrams must be inventoried before redraw")
        figures = FIGURES.read_text(encoding="utf-8")
        for question in (16, 17, 19):
            self.assertIn(f"第 {question} 题", figures)
        self.assertIn("待重绘为 TikZ/PGFPlots", figures)
        raster_embed = r"!\[[^\]]*\]\([^)]*\.(?:png|jpe?g)(?:\?[^)]*)?\)"
        self.assertNotRegex(figures, raster_embed)
        self.assertNotRegex(TRANSCRIPT.read_text(encoding="utf-8"), raster_embed)

    def test_nonofficial_answer_points_preserve_all_21_derived_conclusions(self):
        self.assertTrue(ANSWER_KEY.is_file(), "derived answers must be separate from the transcribed questions")
        answer_key = ANSWER_KEY.read_text(encoding="utf-8")
        self.assertIn("编者独立推导（非官方）", answer_key)
        points = solution_sources.parse_answer_points(answer_key)
        self.assertEqual([point.number for point in points], list(range(1, 22)))
        self.assertEqual(
            [point.answers for point in points],
            [
                ((None, r"$\{1,2,3,4\}$"),),
                ((None, "$(-2,4)$"),),
                ((None, "$2-3i$"),),
                ((None, r"$-\dfrac13$"),),
                ((None, "$6$"),),
                ((None, "$10$"),),
                ((None, "$2$"),),
                ((None, r"$\dfrac32$"),),
                ((None, "$160$"),),
                ((None, "$6$"),),
                ((None, "$48$"),),
                ((None, "$(0,1)$"),),
                ((None, "B"),),
                ((None, "C"),),
                ((None, "A"),),
                ((None, "B"),),
                ((1, "$4$"), (2, r"$\arctan\dfrac{2\sqrt2}{3}$")),
                ((1, "$a=-1$"), (2, r"$a\in[0,2]$")),
                (
                    (1, r"$r_1=20\sqrt3\approx34.6\,\text{米},\quad r_2=60(2-\sqrt3)\approx16.1\,\text{米}$"),
                    (2, r"$r_1=30\,\text{米},\quad r_2=20\,\text{米},\quad K=84\pi\approx263.9\,\text{千元}$"),
                ),
                (
                    (1, r"$y=\pm\sqrt3x$"),
                    (2, r"$k=\pm\dfrac12$"),
                    (3, r"$n=-\dfrac{b^2}{2}$"),
                ),
                ((1, r"$x=\dfrac13$"), (3, r"$x_1\in(-1,\dfrac13]$")),
            ],
        )
        self.assertEqual(points[-1].subparts, (1, 2, 3))

    def test_answer_conflicts_have_counterexamples_and_correct_path_length_cost(self):
        self.assertTrue(ANSWER_KEY.is_file(), "answer conflict review must be recorded with the derived answers")
        r, s = 1.5, 1.75
        a, b = r * s, -(r + s)
        self.assertEqual(r * r + b * r + a, 0)
        self.assertEqual(s * s + b * s + a, 0)
        f_at_one = 1 + a + b
        self.assertEqual(f_at_one, 3 / 8)
        self.assertGreater(f_at_one, 3 - 2 * math.sqrt(2))

        cost = 2 * math.pi * (0.8 * 30 + 0.9 * 20)
        self.assertEqual(round(cost, 1), 263.9)

        answer_key = ANSWER_KEY.read_text(encoding="utf-8")
        self.assertIn("Q13 来源答案页列 D", answer_key)
        self.assertIn("Q19 来源答案页总造价写 42.0 千元", answer_key)

    def test_detailed_solution_blocks_match_the_transcribed_question_structure(self):
        self.assertTrue(SOLUTION_BODY.is_file(), "detailed solutions must be stored independently from answer points")
        questions = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWER_KEY.read_text(encoding="utf-8")
        raw_solutions = SOLUTION_BODY.read_text(encoding="utf-8")
        extracted = solution_sources.extract_solution_blocks(raw_solutions, questions)
        question_blocks = solution_sources.parse_question_blocks(questions, style="inline")
        solution_blocks = solution_sources.parse_question_blocks(extracted, style="heading")
        source_subparts = [
            (
                block.number,
                tuple(int(value) for value in re.findall(
                    r"(?m)^[ \t　]*[（(](\d+)[）)]", block.body
                )),
            )
            for block in question_blocks
        ]
        self.assertEqual(
            source_subparts,
            [(number, ()) for number in range(1, 17)]
            + [(17, (1, 2)), (18, (1, 2)), (19, (1, 2)), (20, (1, 2, 3)), (21, (1, 2, 3))],
        )
        self.assertEqual(
            [(block.number, block.subparts) for block in question_blocks],
            source_subparts,
        )
        self.assertEqual(
            [(block.number, block.subparts) for block in solution_blocks],
            source_subparts,
        )
        combined = solution_sources.render_combined(questions, extracted, answers)
        self.assertIn("2017 年上海市春季高考数学试卷", combined)
        self.assertIn("84\\pi\\approx263.9", combined)


if __name__ == "__main__":
    unittest.main()
