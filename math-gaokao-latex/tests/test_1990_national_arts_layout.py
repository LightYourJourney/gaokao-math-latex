"""Regression tests for the 1990 National Arts editions' page layout."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
PAPER = PROJECT / "1990_全国卷_文科"
QUESTION_26_MARKER = "设椭圆的中心是坐标原点"


class NationalArtsQuestionPaginationTests(unittest.TestCase):
    def compile_and_extract_pages(self, edition):
        xelatex = shutil.which("xelatex")
        pdftotext = shutil.which("pdftotext")
        if not xelatex or not pdftotext:
            self.skipTest("xelatex 与 pdftotext 是本回归测试的实际渲染依赖")

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            source = f"{edition}.tex"
            compiled = subprocess.run(
                [xelatex, "-interaction=nonstopmode", "-halt-on-error",
                 "-output-directory", str(output), source],
                cwd=PAPER,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(0, compiled.returncode, compiled.stdout + compiled.stderr)
            extracted = subprocess.run(
                [pdftotext, "-layout", str(output / f"{edition}.pdf"), "-"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ).stdout
            return extracted.split("\f")

    def test_question_26_shares_page_four_in_submission_and_concise_editions(self):
        for edition in ("试题版", "简答版"):
            with self.subTest(edition=edition):
                pages = self.compile_and_extract_pages(edition)
                question_pages = [
                    page_number
                    for page_number, page in enumerate(pages, start=1)
                    if QUESTION_26_MARKER in page
                ]
                self.assertEqual([4], question_pages)

    def test_question_seven_and_nine_options_do_not_split_across_lines(self):
        pages = self.compile_and_extract_pages("解析版")
        page_two = pages[1].splitlines()
        self.assertTrue(
            any("既不充分也不必要条件" in line for line in page_two),
            "第 7 题 D 项文字应保持在同一行",
        )
        self.assertTrue(
            any("（D）" in line and "a = 3" in line and "b = 6" in line
                for line in page_two),
            "第 9 题 D 项标记与内容应保持在同一行",
        )


if __name__ == "__main__":
    unittest.main()
