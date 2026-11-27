"""Exact and numerical spot checks for 1993 new-track science derivations."""
from fractions import Fraction as F
import cmath
import math
import unittest


class NewTrackScience1993MathChecks(unittest.TestCase):
    def test_q4_polar_conic_has_eccentricity_and_directrix_distance(self):
        e = F(5, 3)
        ed = F(4, 3)
        distance = ed / e
        self.assertGreater(e, 1)
        self.assertEqual(distance, F(4, 5))

    def test_q9_parameter_eliminates_to_parabola_and_option_point_is_reached(self):
        theta = math.pi
        x = math.cos(theta / 2) + math.sin(theta / 2)
        y = (1 + math.sin(theta)) / 2
        self.assertAlmostEqual(x * x, 2 * y, places=12)
        self.assertAlmostEqual(x, 1, places=12)
        self.assertAlmostEqual(y, 0.5, places=12)
        # The other listed endpoint needs theta=2*pi, excluded by the source.
        theta = 2 * math.pi - 1e-6
        x = math.cos(theta / 2) + math.sin(theta / 2)
        self.assertGreater(x, -1)

    def test_q19_circle_hyperbola_intersection_parameter_interval(self):
        # k^2=(13X-9)/36 for X=x^2 in [0,1], so the range is [-1/4,1/9].
        low = (13 * F(0) - 9) / 36
        high = (13 * F(1) - 9) / 36
        self.assertEqual((low, high), (F(-1, 4), F(1, 9)))
        # k=0 is excluded because the displayed hyperbola is undefined there.
        self.assertEqual(F(1, 9), F(1, 3) ** 2)

    def test_q28_argument_condition_depends_on_argument_range_convention(self):
        candidates = [math.pi / 12, 5 * math.pi / 12, 7 * math.pi / 12, 11 * math.pi / 12]
        phases = []
        for theta in candidates:
            z = cmath.exp(1j * theta)
            omega = (1 - z.conjugate() ** 4) / (1 + z**4)
            self.assertAlmostEqual(abs(omega), 1 / math.sqrt(3), places=12)
            phases.append(cmath.phase(omega))
        self.assertEqual(
            [round(value / math.pi * 6) for value in phases],
            [1, -1, 1, -1],
        )
        positive_argument = [t for t, phase in zip(candidates, phases) if phase % (2 * math.pi) < math.pi / 2]
        self.assertEqual(positive_argument, [math.pi / 12, 7 * math.pi / 12])
        self.assertTrue(all(phase < math.pi / 2 for phase in phases))


if __name__ == "__main__":
    unittest.main()
