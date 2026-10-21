"""2016 上海理科印刷版末页正文与页脚间距回归。"""

import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
PAPER_ID = "gk-2016-regular-shanghai-science"
sys.path.insert(0, str(PROJECT / "tools"))

import build_projects


@unittest.skipUnless(
    all(shutil.which(tool) for tool in ("latexmk", "xelatex", "pdfinfo", "pdftotext")),
    "latexmk/xelatex/Poppler 不齐，无法运行真实 PDF 回归",
)
class ShanghaiScience2016PrintFooterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        paper = next(paper for paper in manifest["papers"] if paper["paper_id"] == PAPER_ID)
        cls.project_dir = paper["project_dir"]

        cls.temporary = tempfile.TemporaryDirectory(prefix="gk2016-shanghai-science-footer-")
        root = Path(cls.temporary.name)
        project_copy = root / "docs" / "exams" / "math-gaokao-latex"
        project_copy.mkdir(parents=True)
        shutil.copytree(PROJECT / "common", project_copy / "common")
        shutil.copytree(
            PROJECT / cls.project_dir,
            project_copy / cls.project_dir,
            ignore=shutil.ignore_patterns("build", "receipts", ".work"),
        )

        cls.toolchain = build_projects.resolve_toolchain()
        cls.result = build_projects.build_target(root, cls.project_dir, "印刷版", cls.toolchain)
        cls.pdf = root / cls.result["record"]["pdf"]["path"]
        pdftotext = next(
            tool["path"] for tool in cls.toolchain["tools"]
            if tool["name"] == "pdftotext"
        )
        cls.full_text = subprocess.run(
            [pdftotext, "-layout", str(cls.pdf), "-"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        page = cls.result["record"]["pdf"]["page_count"]
        cls.bbox = subprocess.run(
            [pdftotext, "-bbox", "-f", str(page), "-l", str(page), str(cls.pdf), "-"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_final_answer_boxes_stay_together_and_clear_the_footer(self):
        record = self.result["record"]
        self.assertEqual([], record["problems"])
        self.assertIn(record["pdf"]["page_count"], (15, 16))
        self.assertNotIn("三个答案框作为整体分页", self.full_text)

        words = []
        for match in re.finditer(r"<word\b([^>]*)>(.*?)</word>", self.bbox, re.DOTALL):
            attributes, text = match.groups()
            y_min = float(re.search(r'yMin="([0-9.]+)"', attributes).group(1))
            y_max = float(re.search(r'yMax="([0-9.]+)"', attributes).group(1))
            words.append((y_min, y_max, html.unescape(text)))

        footer = next((word for word in words if word[2].startswith("——第")), None)
        self.assertIsNotNone(footer, "last page footer marker was not extracted")
        extracted = "".join(word[2] for word in words)
        self.assertIn("该证明允许", extracted)
        for subpart in (1, 2, 3):
            with self.subTest(subpart=subpart):
                self.assertIn(f"答案（{subpart}）", extracted)
        last_content_y_max = max(y_max for y_min, y_max, _ in words if y_min < footer[0])
        clearance = footer[0] - last_content_y_max
        self.assertGreaterEqual(
            clearance,
            10.0,
            f"last answer is only {clearance:.2f}pt above the page footer",
        )


if __name__ == "__main__":
    unittest.main()
