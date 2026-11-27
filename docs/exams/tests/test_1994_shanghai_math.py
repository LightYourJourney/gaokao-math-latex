"""1994 上海 Q25 精确几何复算；有限参数回归不替代全域证明或异人盲核。"""

import re
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / '1994' / '1994_数学真题_上海_试题.md'


def quadrant_clip(polygon):
    """对凸多边形依次裁剪 x>=0、y>=0，全程用 Fraction。"""
    for axis in (0, 1):
        result = []
        if not polygon:
            return []
        previous = polygon[-1]
        for current in polygon:
            previous_inside = previous[axis] >= 0
            current_inside = current[axis] >= 0
            if previous_inside != current_inside:
                ratio = previous[axis] / (previous[axis] - current[axis])
                result.append(tuple(p + ratio * (c - p)
                                    for p, c in zip(previous, current)))
            if current_inside:
                result.append(current)
            previous = current
        polygon = result
    return polygon


def area(polygon):
    if len(polygon) < 3:
        return F(0)
    return abs(sum(p[0] * q[1] - p[1] * q[0]
                   for p, q in zip(polygon, polygon[1:] + polygon[:1]))) / 2


def rectangle(t):
    return [(F(0), F(0)), (F(1), t), (1 - 2 * t, 2 + t), (-2 * t, F(2))]


def multiply(left, right):
    """升幂系数的精确多项式乘法，用于全系数恒等式。"""
    result = [F(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


class Shanghai1994MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = SOURCE.read_text(encoding='utf-8')
        match = re.search(r'^\*\*25．\*\*(.*?)(?=^\*\*26．\*\*)',
                          text, re.MULTILINE | re.DOTALL)
        if match is None:
            raise AssertionError('缺少 Q25 独立题块')
        cls.question = match.group(1)

    def test_source_coordinates_and_domain_bind_the_calculation(self):
        for condition in ['矩形 $OPQR$', '逆时针', '$O(0,0)$', '$P(1,t)$',
                          '$Q(1-2t,2+t)$', '$R(-2t,2)$',
                          r'$t\in(0,+\infty)$', '第一象限', '单调区间']:
            self.assertIn(condition, self.question)
        # OP·OR=(1,t)·(-2t,2)恒为0；det(OP,OR)=2+2t²>0。
        dot = [a + b for a, b in zip(multiply([1], [0, -2]),
                                    multiply([0, 1], [2]))]
        self.assertEqual(dot, [0, 0])
        determinant = [a - b for a, b in zip([2, 0, 0],
                                            multiply([0, 1], [0, -2]))]
        self.assertEqual(determinant, [2, 0, 2])

    def test_exact_polygon_clipping_against_both_area_branches(self):
        samples = [F(1, 100), F(1, 4), F(49, 100), F(1, 2),
                   F(51, 100), F(3, 4), F(1), F(3, 2), F(2), F(3), F(100)]
        for t in samples:
            with self.subTest(t=t):
                original = rectangle(t)
                self.assertTrue(all(y >= 0 for x, y in original))
                clipped = quadrant_clip(original)
                expected = (2 * (1 - t + t**2 - t**3) if t <= F(1, 2)
                            else (t + 1 / t) / 2)
                self.assertEqual(area(clipped), expected)
                self.assertTrue(all(x >= 0 and y >= 0 for x, y in clipped))
                self.assertLessEqual(area(clipped), area(original))

    def test_geometric_branch_vertices_on_each_side_of_half(self):
        t = F(1, 4)
        self.assertEqual(set(quadrant_clip(rectangle(t))),
                         {(F(0), F(0)), (F(1), t), (1 - 2*t, 2+t),
                          (F(0), 2 + 2*t*t)})
        t = F(3, 4)
        self.assertEqual(set(quadrant_clip(rectangle(t))),
                         {(F(0), F(0)), (F(1), t), (F(0), t + 1/t)})
        t = F(1, 2)
        self.assertEqual(set(quadrant_clip(rectangle(t))),
                         {(F(0), F(0)), (F(1), t), (F(0), F(5, 2))})

    def test_full_polynomial_identity_and_join_values(self):
        # 小t时四边形OPQL的有向面积：
        # [det(P,Q)+det(Q,L)]/2，L=(0,2+2t²)。
        pq = [2, 0, 2, 0]
        ql = multiply([1, -2], [2, 0, 2])
        self.assertEqual([(a+b)/F(2) for a, b in zip(pq, ql)],
                         [2, -2, 2, -2])
        t = F(1, 2)
        self.assertEqual(2*(1-t+t*t-t**3), F(5, 4))
        self.assertEqual((t+1/t)/2, F(5, 4))
        self.assertEqual(2*(-1+2*t-3*t*t), F(-3, 2))
        self.assertEqual((1-1/(t*t))/2, F(-3, 2))

    def test_derivative_sign_identity_and_minimum(self):
        # -6(t-1/3)²-4/3恒为负，全系数检查而非采样证明。
        completed = [-6*c for c in multiply([F(-1, 3), 1], [F(-1, 3), 1])]
        completed[0] -= F(4, 3)
        self.assertEqual(completed, [-2, 4, -6])
        # 第二支导数(t²-1)/(2t²)：t>0时符号由(t-1)(t+1)决定。
        self.assertEqual(multiply([-1, 1], [1, 1]), [-1, 0, 1])
        for t, sign in [(F(1, 2), -1), (F(3, 4), -1), (F(1), 0), (F(2), 1)]:
            derivative = (1-1/(t*t))/2
            self.assertEqual((derivative > 0)-(derivative < 0), sign)
        self.assertEqual(area(quadrant_clip(rectangle(F(1)))), 1)


if __name__ == '__main__':
    unittest.main()
