import unittest
from src.options_pricing.volatility_smile import VolatilitySmile

class TestVolatilitySmile(unittest.TestCase):

    def test_binarysearch(self):
        lo = 0.0001
        hi = 0.9999
        tol = 0.00005
        answer_squared = 0.17
        vs = VolatilitySmile("aapl")
        answer = vs.binarysearch(lo, hi, tol, answer_squared, lambda x: x*x)
        self.assertAlmostEqual(answer, 0.4123, 4)

if __name__=='__main__':
    unittest.main()