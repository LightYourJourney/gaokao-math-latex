import unittest
from pathlib import Path


ARTS_ANSWERS = (
    Path(__file__).resolve().parents[1]
    / "2018_全国Ⅰ卷_文科"
    / "answers.tex"
)


class ChineseQuotationTypographyTests(unittest.TestCase):
    def test_canonical_solution_source_uses_chinese_quotes(self):
        source = (
            ARTS_ANSWERS.parents[2]
            / "2018"
            / "2018_数学真题_文_解析正文.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn('"', source)

    def test_answer_source_uses_chinese_quotes_instead_of_ascii_quotes(self):
        source = ARTS_ANSWERS.read_text(encoding="utf-8")
        self.assertNotIn('"', source)


if __name__ == "__main__":
    unittest.main()
