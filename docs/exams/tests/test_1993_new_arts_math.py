"""Exact arithmetic cross-checks for selected derived results, not a blind review."""
from fractions import Fraction as F
from math import comb
import unittest


class NewTrackArts1993MathChecks(unittest.TestCase):
    def test_q13_x4_coefficient_in_binomial_product(self):
        coefficient = sum(
            comb(4, k) * comb(5, 4 - k // 2) * (-1) ** (5 - (4 - k // 2))
            for k in (0, 2, 4)
        )
        self.assertEqual(coefficient, 45)

    def test_q14_rotation_surface_and_volume_at_the_inferred_scale(self):
        height = F(1)
        upper_base = 2 * height
        lower_base = 3 * height
        self.assertEqual(lower_base / upper_base, F(3, 2))
        self.assertEqual(lower_base - upper_base, height)
        # Coefficients of pi*h^2: bottom disk + cylinder + conical surface.
        self.assertEqual(F(1) + 2 * upper_base / height, F(5))
        # The sloping side contributes sqrt(2) in the same units.
        slant_squared = height**2 + (lower_base - upper_base) ** 2
        self.assertEqual(slant_squared, F(2))
        volume_over_pi = height**2 * upper_base + height**2 * (
            lower_base - upper_base
        ) / 3
        self.assertEqual(volume_over_pi, F(7, 3))

    def test_q15_geometric_sum_difference_has_the_claimed_sign(self):
        for q in (F(2), F(1, 2), F(3, 2), F(2, 3)):
            difference = 1 + q**7 - q**3 - q**4
            factored = (1 - q**3) * (1 - q**4)
            self.assertEqual(difference, factored)
            self.assertGreater(difference, 0)

    def test_q23_folded_point_preserves_edges_and_gives_thirty_degree_dihedral(self):
        y = F(1, 2)
        z_squared = F(3, 4)
        self.assertEqual(y**2 + z_squared, F(1))  # PE^2
        self.assertEqual(1 + (y - 2) ** 2 + z_squared, F(4))  # PD^2 = PC^2
        oe_squared = F(4)
        op_squared = F(3)
        dot = F(3)
        self.assertGreater(dot, 0)
        self.assertEqual(4 * dot**2, 3 * oe_squared * op_squared)

    def test_q26_term_telescopes_to_the_predicted_partial_sum(self):
        partial = F(0)
        for n in range(1, 21):
            term = F(8 * n, (2 * n - 1) ** 2 * (2 * n + 1) ** 2)
            self.assertEqual(
                term,
                F(1, (2 * n - 1) ** 2) - F(1, (2 * n + 1) ** 2),
            )
            partial += term
            self.assertEqual(partial, F(1) - F(1, (2 * n + 1) ** 2))

    def test_q27_point_to_intersection_line_distance_is_13_over_5(self):
        # A=(4,0,1), l lies in z=0 and has direction (-4,3,0).
        cross_product_squared = 3**2 + 4**2 + 12**2
        direction_squared = 4**2 + 3**2
        self.assertEqual(F(cross_product_squared, direction_squared), F(169, 25))

    def test_q28_area_and_focal_distances_fix_the_ellipse_axes(self):
        sin_a, cos_a = 1, 2  # both divided by sqrt(5)
        sin_b, cos_b = 2, -1  # both divided by sqrt(5)
        sin_p = F(sin_a * cos_b + cos_a * sin_b, 5)
        self.assertEqual(sin_p, F(3, 5))
        k_squared = F(25, 3)  # from area 1 = 3 k^2 / 25
        mn_squared = F(9, 25) * k_squared
        focus_c_squared = mn_squared / 4
        sum_focal_distances_squared = F(9, 5) * k_squared
        a_squared = sum_focal_distances_squared / 4
        b_squared = a_squared - focus_c_squared
        self.assertEqual(mn_squared, F(3))
        self.assertEqual(a_squared, F(15, 4))
        self.assertEqual(b_squared, F(3))


if __name__ == "__main__":
    unittest.main()
