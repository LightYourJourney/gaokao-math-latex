"""Regression coverage for the 1977 Beijing arts Q10 final intersection answer."""
import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent
SOURCE_ROOT = REPO_ROOT / "1977"
PAPER_ROOT = PROJECT_ROOT / "1977_北京卷_文科"


def answer_points(path: Path, marker: str):
    text = path.read_text(encoding="utf-8")
    lines = [
        line for line in text.splitlines()
        if marker in line and "交点为" in line
    ]
    if len(lines) != 1:
        raise AssertionError(f"expected one answer line with {marker!r} in {path}")
    return [
        (int(x), int(y))
        for x, y in re.findall(
            r"\$\((-?\d+)\s*,\s*(-?\d+)\)\$",
            lines[0].split(marker, maxsplit=1)[1],
        )
    ]


class BeijingArts1977Q10Tests(unittest.TestCase):
    def test_intersection_answers_match_the_quadratic_and_line(self):
        # x^2 - 4x + 3 = x - 3 gives (x - 2)(x - 3) = 0;
        # substituting into y = x - 3 gives (2, -1) and (3, 0).
        expected = [(2, -1), (3, 0)]
        artifacts = (
            (SOURCE_ROOT / "1977_数学真题_北京文_答案要点.md", "(3) 答案"),
            (SOURCE_ROOT / "1977_数学真题_北京文_含解析.md", "答案（3）"),
            (PAPER_ROOT / "answers.tex", "答案（3）"),
            (PAPER_ROOT / "answers_short.tex", "(3) 交点为"),
        )
        for path, marker in artifacts:
            with self.subTest(artifact=path.name, marker=marker):
                self.assertEqual(answer_points(path, marker), expected)


if __name__ == "__main__":
    unittest.main()
