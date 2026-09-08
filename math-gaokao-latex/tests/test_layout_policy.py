# -*- coding: utf-8 -*-
"""公共题块版式策略的回归测试。"""
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_SOURCES = (
    ROOT / "common" / "questions_env.tex",
    ROOT / "common" / "macros.tex",
)


class LayoutPolicyTests(unittest.TestCase):
    def test_question_and_answer_reserve_space_before_starting_a_block(self):
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in ENV_SOURCES
        )
        patterns = {
            "question": r"\\newenvironment\{question\}\{\\Needspace\{0\.15\\textheight\}\}\{\}",
            "answer": r"\\newenvironment\{answer\}\{\\Needspace\{0\.5\\textheight\}\}\{\}",
            "gkpart": r"\\newcommand\{\\gkpart\}\[1\]\{\\Needspace\{0\.4\\textheight\}",
        }
        for environment, pattern in patterns.items():
            self.assertRegex(
                source,
                re.compile(pattern),
                msg=f"{environment} 环境必须在题块开始前保留 0.4\\textheight",
            )

    def test_reviewed_pagination_boundaries_reserve_space_in_source(self):
        cases = {
            ROOT.parent / "2017" / "2017_数学真题_文_解析正文.md": [
                ("**情形二：长轴在 $y$ 轴上**", r"\\Needspace\{0\.25\\textheight\}"),
            ],
            ROOT.parent / "2018" / "2018_数学真题_文_解析正文.md": [
                ("### 第 23 题（10 分，不等式选讲）", r"\\Needspace\{0\.5\\textheight\}"),
                ("**第二步：与已知条件联立。**", r"\\Needspace\{0\.25\\textheight\}"),
                ("## 选考题（现行考纲已取消，仅存档）", r"\\Needspace\{0\.4\\textheight\}"),
            ],
            ROOT.parent / "2018" / "2018_数学真题_理_解析正文.md": [
                ("### 第 20 题（12 分，二项分布与决策）", r"\\Needspace\{0\.5\\textheight\}"),
                ("### 第 23 题（10 分，绝对值不等式）", r"\\Needspace\{0\.5\\textheight\}"),
            ],
            ROOT.parent / "2018" / "2018_数学真题_理_试题.md": [
                ("## 一、选择题", r"\\Needspace\{0\.4\\textheight\}"),
            ],
        }
        for path, boundaries in cases.items():
            text = path.read_text(encoding="utf-8")
            for heading, directive in boundaries:
                self.assertRegex(
                    text,
                    re.compile(directive + r"\s+" + re.escape(heading)),
                    msg=f"{path.name} 的 {heading} 前必须保留源级分页空间",
                )


if __name__ == "__main__":
    unittest.main()
