"""Checks that the source answer transcription stays complete and attributed."""
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / "math-gaokao-latex/1999_上海卷_理科"
ANSWERS = PAPER / "答案要点草稿.md"
SOURCE_RECORD = PAPER / "来源校对.json"

SOURCE_ANSWERS = {
    1: r"$2-\sqrt{3}$",
    2: r"$[3,+\infty)$",
    3: r"$40$",
    4: r"$2\sqrt{3}$ 或 $\sqrt{3}$",
    5: r"$(2,2)$",
    6: r"$\pi$",
    7: r"$(-\frac{5\pi}{6},-\frac{\pi}{3})$",
    8: r"$\{\frac{\sqrt{2}}{2},\frac{3\sqrt{2}}{2}\}$",
    9: r"$(\sqrt{10},0)$、$(\sqrt{10},\pi)$",
    10: r"$9$",
    11: r"$\frac{2}{9}$",
    12: r"$\frac{\sqrt{11}}{12}$、$\frac{\sqrt{14}}{12}$、$\frac{\sqrt{11}}{6}$（三者任一）",
    13: "C",
    14: "D",
    15: "B",
    16: "C",
    17: r"$0\le a\le1$",
    18: r"$\frac32\lg2$",
    19: r"$[0,\frac\pi4)\cup(\frac{7\pi}4,2\pi)$",
    20: r"（1）$BE\perp PD$；（2）$\arccos\frac{\sqrt2}{4}$",
    21: r"（1）$\frac{2\sqrt6}{3}$米；（2）$\frac{400\sqrt6}{9}$立方米；（3）$\frac{\sqrt2}{2}$米",
    22: r"（1）$(\frac{a}{\sqrt2},\frac{\sqrt2}{a})$，$a>\sqrt2$；（2）$S(a)$值域$(0,\sqrt2)$；（3）见下方分段式",
}


class Shanghai1999ScienceAnswerTranscriptionTests(unittest.TestCase):
    def test_transcribes_all_22_source_answers_without_relabeling_them_official(self):
        self.assertTrue(ANSWERS.is_file(), "fixed-source answer transcription is missing")
        text = ANSWERS.read_text(encoding="utf-8")
        rows = {
            int(number): answer.strip()
            for number, answer in re.findall(r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|", text, re.MULTILINE)
        }
        self.assertEqual(set(rows), set(SOURCE_ANSWERS))
        for number, answer in SOURCE_ANSWERS.items():
            with self.subTest(question=number):
                self.assertEqual(rows[number], answer)
        self.assertIn(r"a^2-\dfrac{4}{a^2}", text)
        self.assertIn(r"\sqrt{2\left(1-\dfrac{4}{a^4}\right)}", text)
        self.assertIn("固定扫描件所载", text)
        self.assertIn("不称为官方答案", text)
        self.assertIn(r"\bar z(1-ci)", text)

    def test_source_state_keeps_official_answer_and_generated_solution_separate(self):
        record = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))
        self.assertIsNone(record["paper_id"])
        self.assertIsNone(record["official_answer"])
        self.assertEqual(record["source_answer_transcription_status"], "transcribed-draft-pending-independent-review")
        self.assertEqual(record["generated_solution_status"], "not-started")
        self.assertEqual(record["review_status"], "pending")
        correction = record["transcription_notes"][0]
        self.assertEqual(correction["question_number"], 19)
        self.assertEqual(correction["source_notation"], r"\bar z(1-ci)")
        self.assertEqual(correction["status"], "corrected-pending-independent-review")


if __name__ == "__main__":
    unittest.main()
