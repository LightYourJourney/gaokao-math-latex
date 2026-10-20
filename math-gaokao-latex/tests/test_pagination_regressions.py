# -*- coding: utf-8 -*-
"""已构建 PDF 的局部分页回归检查。"""
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def pdf_pages_text(path: Path):
    pdftotext = shutil.which("pdftotext")
    if pdftotext is None:
        raise RuntimeError("分页回归测试需要 Poppler 的 pdftotext")
    result = subprocess.run(
        [pdftotext, "-layout", str(path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return [page for page in result.stdout.split("\f") if page.strip()]


class PublishedPaginationRegressionTests(unittest.TestCase):
    def test_2017_arts_q23_solution_and_answer_boxes_share_a_page(self):
        pdf = ROOT / "2017_全国Ⅰ卷_文科" / "build" / "解析版.pdf"
        pages = pdf_pages_text(pdf)
        q23 = next(
            page
            for page in pages
            if "第 23 题（10 分，不等式选讲）" in page
        )
        self.assertIn("分三段去绝对值", q23)
        self.assertIn("答案（1）", q23)
        self.assertIn("−1 ≤ a ≤ 1", q23)

    def test_2018_arts_cancelled_questions_share_a_page_in_each_edition(self):
        for edition in ("试题版", "简答版", "解析版"):
            with self.subTest(edition=edition):
                pdf = ROOT / "2018_全国Ⅰ卷_文科" / "build" / f"{edition}.pdf"
                pages = pdf_pages_text(pdf)
                q23_page = next(
                    page for page in pages if "23．（10 分）" in page
                )
                self.assertIn("22．（10 分）", q23_page)


if __name__ == "__main__":
    unittest.main()
