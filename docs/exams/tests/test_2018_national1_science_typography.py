from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
ANSWERS = PROJECT / "2018_全国Ⅰ卷_理科" / "answers.tex"


class ChineseQuotationTypographyTests(unittest.TestCase):
    def test_answer_source_uses_chinese_quotes_instead_of_ascii_quotes(self):
        source = ANSWERS.read_text(encoding="utf-8")

        self.assertNotIn('"', source)


if __name__ == "__main__":
    unittest.main()
