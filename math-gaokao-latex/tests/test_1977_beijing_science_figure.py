"""Regression checks for the 1977 Beijing science Q10 tangent diagram."""

import re
import unittest
from fractions import Fraction
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIGURE = PROJECT_ROOT / "1977_北京卷_理科" / "figures" / "f1977_t10_ellipse.tex"


class BeijingScience1977Q10FigureTests(unittest.TestCase):
    def test_marked_tangent_point_lies_on_ellipse_and_line(self):
        source = FIGURE.read_text(encoding="utf-8")
        marker = re.search(
            r"\\fill\s*\(([-\d.]+),\s*([-\d.]+)\)\s*circle",
            source,
        )
        self.assertIsNotNone(marker, "diagram must mark the tangent point")
        x, y = map(Fraction, marker.groups())

        self.assertEqual(x * x / 16 + y * y / 9, 1)
        self.assertEqual(y, x + 5)

    def test_line_label_anchor_is_separate_from_tangent_point(self):
        source = FIGURE.read_text(encoding="utf-8")
        line = re.search(
            r"\\draw\[thick\]\s*\(([-\d.]+),\s*([-\d.]+)\)"
            r"--\(([-\d.]+),\s*([-\d.]+)\)\s*"
            r"node\[pos=([-\d.]+)(?:,([^]]+))?\]\s*\{\$y=x\+5\$\}",
            source,
        )
        self.assertIsNotNone(line, "line label must have its own position on the tangent")
        x1, y1, x2, y2, position = map(Fraction, line.groups()[:5])
        marker = re.search(
            r"\\fill\s*\(([-\d.]+),\s*([-\d.]+)\)\s*circle",
            source,
        )
        self.assertIsNotNone(marker, "diagram must mark the tangent point")
        px, py = map(Fraction, marker.groups())
        label_x = x1 + position * (x2 - x1)
        label_y = y1 + position * (y2 - y1)

        self.assertGreater((label_x - px) ** 2 + (label_y - py) ** 2, 1)


if __name__ == "__main__":
    unittest.main()
