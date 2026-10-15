import json
import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
PROJECT = REPO / "math-gaokao-latex"
SOURCE_ID = "src-ff04f7f2223009c3c15fc98a35cc99ba9f03d8be55457e6551b982fbb17f2766"
QUESTION_FILE = REPO / "1989/1989_数学真题_广东文_试题.md"
FIGURE_DIR = PROJECT / "1989_广东卷_文科/figures"


class GuangdongArtsTranscriptionTests(unittest.TestCase):
    def setUp(self):
        self.transcript = QUESTION_FILE.read_text(encoding="utf-8")
        self.manifest = json.loads(
            (PROJECT / "source-manifest.json").read_text(encoding="utf-8")
        )

    def test_fixed_source_identity_and_scope_are_not_overstated(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["upstream_path"], "普通高考/1989/1989广东文.pdf")
        self.assertEqual(
            source["artifact"]["sha256"],
            "e0b112f4d4576e791844332f7ffb465c65f3a3ba6516467a7888f9333ca7169f",
        )
        self.assertIsNone(source["paper_id"])
        self.assertIn("来源身份待核", self.transcript)

    def test_question_blocks_cover_25_choices_and_five_second_volume_items(self):
        choice_numbers = re.findall(r"^\*\*(\d+)．\*\*", self.transcript, re.MULTILINE)
        self.assertEqual([int(number) for number in choice_numbers], list(range(1, 26)))
        for label in ("一", "二", "三", "四", "五"):
            self.assertIsNotNone(re.search(rf"^### {label}、", self.transcript, re.MULTILINE))
        self.assertIn("第一卷：选择题（25题，共50分）", self.transcript)
        self.assertIn("第二卷：五道大题（共70分，考生必须全部作答）", self.transcript)

    def test_high_risk_symbols_and_conditions_are_explicit(self):
        for fragment in (
            r"x^{1/5}",
            r"2\log_x 8-3\log_8 x=1",
            r"y=|x-1|",
            r"\dfrac{x^2}{9}-y^2=1",
            r"a\le-3",
            r"|z|=1",
            r"0\le\theta<2\pi",
        ):
            self.assertIn(fragment, self.transcript)

    def test_referenced_drawings_are_local_vector_sources_only(self):
        targets = re.findall(r"\]\(([^)]+\.tex)\)", self.transcript)
        self.assertEqual(len(targets), 2)
        for target in targets:
            resolved = (QUESTION_FILE.parent / target).resolve()
            self.assertTrue(resolved.is_file(), target)
            self.assertEqual(resolved.suffix, ".tex")
        self.assertFalse(list(FIGURE_DIR.glob("*.png")))
        self.assertFalse(list(FIGURE_DIR.glob("*.jpg")))
        self.assertFalse(list(FIGURE_DIR.glob("*.jpeg")))


if __name__ == "__main__":
    unittest.main()
