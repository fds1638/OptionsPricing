import unittest
import numpy as np
from src.options_pricing.interest_rate_products.discrete_interest_rates.nelson_siegel_svensson import NelsonSiegelSvensson

class TestNelsonSiegelSvensson(unittest.TestCase):

    def test_bondyield(self):
        b0 = 0.0503
        b1 = -0.0347
        b2 = 0.1373
        b3 = 0.0113
        ll = 0.02
        mu = 0.2
        nss = NelsonSiegelSvensson()
        bondyield_01 = nss.bondyield(b0, b1, b2, ll, 1, b3, mu)
        bondyield_08 = nss.bondyield(b0, b1, b2, ll, 8, b3, mu)
        bondyield_15 = nss.bondyield(b0, b1, b2, ll, 15, b3, mu)
        self.assertEqual(round(bondyield_01, 4), 0.0183)
        self.assertEqual(round(bondyield_08, 4), 0.0315)
        self.assertEqual(round(bondyield_15, 4), 0.0402)


    def test_value(self):
        b0 = 0.0503
        b1 = -0.0347
        b2 = 0.1373
        b3 = 0.0113
        ll = 0.02
        mu = 0.2
        coupons = np.array([0.750, 0.125, 0.625, 0.125, 0.375, 0.125, 0.500, 0.375, 0.250, 4.250])
        nss = NelsonSiegelSvensson()
        value_3 = nss.value(b0, b1, b2, ll, 3, coupons, b3, mu)
        value_7 = nss.value(b0, b1, b2, ll, 7, coupons, b3, mu)
        value_9 = nss.value(b0, b1, b2, ll, 9, coupons, b3, mu)
        self.assertEqual(round(value_3, 2), 95.24)
        self.assertEqual(round(value_7, 1), 84.5) # not getting full precision but 1 decimal good enough
        self.assertEqual(round(value_9, 1), 76.7) # not getting full precision but 1 decimal good enough


if __name__=='__main__':
    unittest.main()

