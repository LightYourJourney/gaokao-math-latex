"""Regression checks for editor-derived 2006 Shanghai arts answers."""
import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ANSWER_KEY = ROOT / "2006/2006_数学真题_上海文_答案要点.md"
SOLUTIONS = ROOT / "2006/2006_数学真题_上海文_解析正文.md"
COMBINED = ROOT / "2006/2006_数学真题_上海文_含解析.md"
MANIFEST = ROOT / "math-gaokao-latex/source-manifest.json"
TOOLS = ROOT / "math-gaokao-latex/tools"
QUESTION_NUMBERS = set(range(1, 23))
sys.path.insert(0, str(TOOLS))
import generate_projects


class ShanghaiArts2006SolutionTests(unittest.TestCase):
    def require_file(self, path):
        self.assertTrue(path.is_file(), f"required answer artifact is missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_official_answer_source_is_recorded_and_solution_prose_is_distinguished(self):
        answer_key = self.require_file(ANSWER_KEY)
        solutions = self.require_file(SOLUTIONS)

        for document in (answer_key, solutions):
            with self.subTest(document=document[:80]):
                self.assertIn("paper_id: gk-2006-regular-shanghai-arts", document)
                self.assertIn("official_answer_status: verified", document)
                self.assertIn("source_identity_status: exam_identity_verified", document)
                self.assertIn("scan_publisher_edition_status: unknown", document)
                self.assertIn("scan_lineage_status: unknown", document)
                self.assertIn(
                    'official_answer_source: "https://www.shmeea.edu.cn/page/02200/20061015/3886.html"',
                    document,
                )
        self.assertIn("编者独立撰写", solutions)
        self.assertIn("非官方推导与说明", solutions)
        self.assertIn("Q1–Q22 的最终答案要点均一致", answer_key)
        for image_name in ("00007817.jpg", "00007819.jpg", "00007820.jpg", "00007822.jpg"):
            with self.subTest(image=image_name):
                self.assertIn(f"https://www.shmeea.edu.cn/u/cms/www/wdcms/{image_name}", answer_key)

    def test_both_documents_cover_each_question_once(self):
        answer_key = self.require_file(ANSWER_KEY)
        solutions = self.require_file(SOLUTIONS)

        answer_numbers = [
            int(value)
            for value in re.findall(r"(?m)^\*\*(\d{1,2})．\*\*", answer_key)
        ]
        solution_numbers = [
            int(value)
            for value in re.findall(r"(?m)^### 第 (\d{1,2}) 题$", solutions)
        ]
        self.assertEqual(set(answer_numbers), QUESTION_NUMBERS)
        self.assertEqual(len(answer_numbers), 22)
        self.assertEqual(set(solution_numbers), QUESTION_NUMBERS)
        self.assertEqual(len(solution_numbers), 22)

    def test_detailed_render_does_not_duplicate_subpart_answer_boxes(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        paper = next(
            item for item in manifest["papers"]
            if item["paper_id"] == "gk-2006-regular-shanghai-arts"
        )
        generated = generate_projects.generate_project(
            ROOT, generate_projects.paper_sources(paper)
        )
        answers_path = (
            "math-gaokao-latex/"
            f"{paper['project_dir']}/answers.tex"
        )
        answers_tex = generated.targets[answers_path].decode("utf-8")

        # Q1–Q18 have one answer each; Q19–Q22 have 2, 2, 3, 3 subparts.
        # These 28 official-key boxes are the only answer callouts in the detailed output.
        self.assertEqual(answers_tex.count(r"\gkanswer{"), 28)

    def test_source_disclosure_box_uses_ragged_right_text(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        paper = next(
            item for item in manifest["papers"]
            if item["paper_id"] == "gk-2006-regular-shanghai-arts"
        )
        generated = generate_projects.generate_project(
            ROOT, generate_projects.paper_sources(paper)
        )
        questions_path = (
            "math-gaokao-latex/"
            f"{paper['project_dir']}/questions.tex"
        )
        questions_tex = generated.targets[questions_path].decode("utf-8")
        notice = re.search(
            r"\\begin\{gktip\}\s*(.*?)\\end\{gktip\}",
            questions_tex,
            re.DOTALL,
        )

        self.assertIsNotNone(notice)
        self.assertTrue(notice.group(1).lstrip().startswith(r"\raggedright"))

    def test_q15_choice_rows_break_after_the_second_option(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        paper = next(
            item for item in manifest["papers"]
            if item["paper_id"] == "gk-2006-regular-shanghai-arts"
        )
        generated = generate_projects.generate_project(
            ROOT, generate_projects.paper_sources(paper)
        )
        answers_path = (
            "math-gaokao-latex/"
            f"{paper['project_dir']}/answers.tex"
        )
        answers_tex = generated.targets[answers_path].decode("utf-8")

        self.assertIn(
            "（A）充分非必要条件　（B）必要非充分条件\\\\\n"
            "（C）充分必要条件　（D）既非充分又非必要条件",
            answers_tex,
        )

    def test_each_solution_conclusion_matches_the_answer_key(self):
        answer_key = self.require_file(ANSWER_KEY)
        combined = self.require_file(COMBINED)
        answers = {}
        current_question = None
        for line in answer_key.splitlines():
            question = re.match(r"^\*\*(\d{1,2})．\*\*", line)
            if question is not None:
                current_question = int(question.group(1))
            single = re.match(
                r"^\*\*\d{1,2}．\*\* \*\*答案：(.*?)\*\*。?$", line
            )
            if single is not None:
                answers[(current_question, None)] = single.group(1).strip().rstrip("。")
                continue
            subpart = re.match(r"^\*\*\((\d+)\) 答案：(.*?)\*\*。?$", line)
            if subpart is not None:
                answers[(current_question, int(subpart.group(1)))] = (
                    subpart.group(2).strip().rstrip("。")
                )
        sections = {
            int(number): body
            for number, body in re.findall(
                r"(?ms)^### 第 (\d{1,2}) 题\s*\n(.*?)(?=^### 第 \d{1,2} 题\s*$|\Z)",
                combined,
            )
        }

        self.assertEqual(set(sections), QUESTION_NUMBERS)
        for number in sorted(QUESTION_NUMBERS):
            with self.subTest(question=number):
                conclusions = {}
                single = re.search(r"(?m)^\*\*答案：(.*?)\*\*$", sections[number])
                if single is not None:
                    conclusions[(number, None)] = single.group(1).strip().rstrip("。")
                for part, value in re.findall(
                    r"(?m)^\*\*答案（(\d+)）：(.*?)\*\*$", sections[number]
                ):
                    conclusions[(number, int(part))] = value.strip().rstrip("。")
                expected = {
                    key: value for key, value in answers.items() if key[0] == number
                }
                self.assertTrue(conclusions, f"Q{number} has no explicit conclusion")
                self.assertEqual(conclusions, expected)

    def test_high_risk_results_and_q22_domain_cases_remain_explicit(self):
        answer_key = self.require_file(ANSWER_KEY)
        solutions = self.require_file(SOLUTIONS)
        for expected in (
            r"\frac{x^2}{9}-\frac{y^2}{16}=1",
            r"\frac{14}{33}",
            r"b\in[-1,1]",
            "D，即 $36$ 个",
            r"-\frac{13\sqrt2}{14}",
            r"71^\circ",
            r"\dfrac{\sqrt2}{6}",
            "第 $46$ 项起",
            r"\sqrt2",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, answer_key)

        q22 = re.search(r"(?ms)^### 第 22 题\s*\n(.*)\Z", solutions)
        self.assertIsNotNone(q22)
        for marker in ("定义域", "$x>0$", "$x<0$", "偶数", "奇数"):
            with self.subTest(marker=marker):
                self.assertIn(marker, q22.group(1))


if __name__ == "__main__":
    unittest.main()
