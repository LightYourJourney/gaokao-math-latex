"""Source-bound completeness checks for the 1995 Shanghai science paper."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1995_上海卷_理工农医类"
DRAFT = PAPER / "题面转录草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"
SOLUTIONS = PAPER / "解析草稿.md"
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"
PROGRESS = ROOT / "PROGRESS.md"
SOURCE_ID = "src-ba07d7a09bef9f724f8587c86ffcfd862c046e315f01063cf37b3176262d384e"


class ShanghaiScience1995SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next(
            (source for source in cls.manifest["sources"] if source["source_id"] == SOURCE_ID),
            None,
        )
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.draft = DRAFT.read_text(encoding="utf-8") if DRAFT.is_file() else ""
        cls.answers = ANSWERS.read_text(encoding="utf-8") if ANSWERS.is_file() else ""
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""

    def test_draft_is_bound_to_the_fixed_unbound_source(self):
        self.assertIsNotNone(self.source)
        if not DRAFT.is_file() or not RECORD.is_file():
            self.fail("1995 Shanghai science transcription and source record are missing")
            return
        self.assertEqual(self.source["source_state"], "ready")
        self.assertEqual(self.source["paper_id"], "gk-1995-regular-shanghai-science")
        self.assertEqual(self.source["upstream_path"], "普通高考/1995/1995上海理.pdf")
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(
            self.record["pdf_sha256"],
            "b45c3f98d35b6ad0c7788945110e6295b686dfce4f330c678da769db31f5d6eb",
        )
        self.assertEqual(self.record["pdf_sha256"], self.source["artifact"]["sha256"])
        self.assertEqual(self.record["git_blob_oid"], self.source["git_blob_oid"])
        self.assertEqual(self.record["draft_sha256"], hashlib.sha256(DRAFT.read_bytes()).hexdigest())
        self.assertEqual(self.record["answers_draft_sha256"], hashlib.sha256(ANSWERS.read_bytes()).hexdigest())
        self.assertEqual(self.record["solutions_draft_sha256"], hashlib.sha256(SOLUTIONS.read_bytes()).hexdigest())
        self.assertEqual(self.record["page_map"][-1], {"page": 9, "printed_page": None, "role": "blank-reverse"})

    def test_all_numbered_questions_and_track_variants_are_preserved(self):
        if not DRAFT.is_file() or not RECORD.is_file():
            self.fail("question draft and source record must exist")
            return
        headings = [int(number) for number in re.findall(r"^\*\*(\d+)．\*\*", self.draft, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 26)))
        self.assertEqual(self.record["question_count"], 25)
        self.assertEqual(self.record["prompt_variant_count"], 30)
        self.assertEqual(len(self.record["question_sources"]), 25)
        self.assertEqual(
            [item["question_id"] for item in self.record["question_sources"]],
            [f"1995-shanghai-science-q{number:03d}" for number in range(1, 26)],
        )
        self.assertEqual(
            [item["question_number"] for item in self.record["question_sources"]],
            list(range(1, 26)),
        )
        for track in ("A₁", "B₁", "A₂", "B₂"):
            with self.subTest(track=track):
                self.assertIn(track, self.draft)
        for number in (18, 19, 20, 21, 22):
            with self.subTest(question=number):
                start = self.draft.index(f"**{number}．**")
                next_heading = self.draft.find("\n**", start + 1)
                question = self.draft[start:next_heading if next_heading >= 0 else len(self.draft)]
                tracks = ("A₁组", "B₁组") if number <= 20 else ("A₂组", "B₂组")
                for track in tracks:
                    with self.subTest(question=number, track=track):
                        self.assertIn(track, question)

    def test_source_specific_stems_and_math_are_transcribed(self):
        required = (
            "上海数学试卷（理工农医类）",
            r"y=\sin^2 x",
            r"(x-1)(2x-5)<0",
            r"\tan\left(2x+\dfrac\pi3\right)=\dfrac{\sqrt3}{3}",
            r"\dfrac{x^2}{2}-\dfrac{8y^2}{9}=8",
            r"\rho^2=\dfrac1{4\cos^2\theta-1}",
            r"\left(\dfrac{\sqrt3}{2},\dfrac12,0\right)",
            r"\dfrac{x^2}{m^2}+\dfrac{y^2}{n^2}=1",
            r"f(x)g(x)+a_nx+b_n=x^{n+1}",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertTrue(fragment in self.draft, f"missing source-specific fragment: {fragment}")

    def test_answer_key_and_solutions_are_separate_and_source_attributed(self):
        if not ANSWERS.is_file() or not SOLUTIONS.is_file() or not RECORD.is_file():
            self.fail("source answer points, explanations, and provenance must be present separately")
            return
        self.assertEqual(self.record["source_has_answers"], True)
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["answer_provenance"], "source-provided-unverified")
        self.assertEqual(self.record["mathematical_verification_status"], "verified")
        self.assertEqual(self.record["review_status"], "reviewed")
        self.assertTrue(any(
            issue["question_number"] == 24 and issue["type"] == "source-answer-boundary-omission"
            for issue in self.record["source_issues"]
        ))
        self.assertEqual(
            [int(number) for number in re.findall(r"^## (\d+)．", self.answers, re.MULTILINE)],
            list(range(1, 26)),
        )
        self.assertEqual(
            [int(number) for number in re.findall(r"^## (\d+)．", self.solutions, re.MULTILINE)],
            list(range(1, 26)),
        )
        for answer in ("答案：C", "答案：B", "答案：B", "答案：C", "答案：A", "答案：A", "答案：D", "答案：B"):
            with self.subTest(choice_answer=answer):
                self.assertTrue(answer in self.answers, f"missing answer point {answer}")
        self.assertIn(r"2mn", self.answers)
        self.assertIn(r"m=n", self.answers)
        self.assertIn("来源答案在此处漏掉", self.answers)
        self.assertTrue("x>2" in self.answers, "Q9 solution must use the correct sign interval")
        self.assertIn("\n## 25．", self.answers)
        self.assertIn("\n## 25．", self.solutions)

    def test_figures_are_registered_vector_sources_and_progress_is_recorded(self):
        if not DRAFT.is_file() or not RECORD.is_file():
            self.fail("question draft and source record must exist")
            return
        figures = self.record.get("figure_files", [])
        self.assertEqual({figure["question_number"] for figure in figures}, {6, 21, 23})
        self.assertEqual(len(figures), 4)
        for figure in figures:
            path = PAPER / figure["path"]
            linked_document = self.solutions if figure["role"] == "solution-construction" else self.draft
            with self.subTest(path=figure["path"]):
                self.assertTrue(path.is_file(), figure["path"])
                self.assertEqual(path.suffix, ".tex")
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), figure["sha256"])
                self.assertIn(f"]({figure['path']})", linked_document)
        raster_files = [
            path for path in PAPER.rglob("*")
            if path.is_file() and ".work" not in path.parts and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
        ]
        self.assertEqual(raster_files, [])
        progress = PROGRESS.read_text(encoding="utf-8")
        marker = "## 1995 上海卷理科：25题、30个分支题面转录完成"
        self.assertTrue(any(line.startswith(marker) for line in progress.splitlines()), "completed transcription is absent from PROGRESS.md")
        entry_start = progress.index(marker)
        next_heading = progress.find("\n## ", entry_start + len(marker))
        entry = progress[entry_start:next_heading if next_heading >= 0 else len(progress)]
        for section in ("已完成：", "修改文件：", "验证：", "剩余/下一步："):
            with self.subTest(section=section):
                self.assertIn(section, entry)
        self.assertIn("0次OCR", entry)
        self.assertIn("待独立", entry)


if __name__ == "__main__":
    unittest.main()
