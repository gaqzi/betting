from collections import namedtuple
import unittest

from betting import Odds

OddsTuple = namedtuple('OddsTuple', 'decimal fractional us hk indo malay')
all_odds = (
    OddsTuple(1.5, '1/2', -200, 0.5, -2.0, 0.5),
    OddsTuple(2.0, '1/1', 100, 1.0, 1.0, 1.0),
    OddsTuple(2.5, '3/2', 150, 1.5, 1.5, -0.67),
    OddsTuple(3.0, '2/1', 200, 2.0, 2.0, -0.5),
    OddsTuple(1.4, '2/5', -250, 0.4, -2.5, 0.40)
)


class TestOdds(unittest.TestCase):
    def test_decimal(self):
        for bet in all_odds:
            conv, dec = bet.decimal, bet.decimal
            o = Odds.decimal(conv)
            self.assertEqual(o.decimal, dec,
                             msg='conv: {0} = dec: {1}'.format(conv, dec))

    def test_fractional(self):
        for bet in all_odds:
            conv, dec = bet.fractional, bet.decimal
            o = Odds.fractional(conv)
            self.assertEqual(o.decimal, dec,
                             msg='conv: {0} = dec: {1}'.format(conv, dec))

    def test_us(self):
        for bet in all_odds:
            conv, dec = bet.us, bet.decimal
            o = Odds.us(conv)
            self.assertEqual(o.decimal, dec,
                             msg='conv: {0} = dec: {1}'.format(conv, dec))

    def test_hk(self):
        for bet in all_odds:
            conv, dec = bet.hk, bet.decimal
            o = Odds.hk(conv)
            self.assertEqual(o.decimal, dec,
                             msg='conv: {0} = dec: {1}'.format(conv, dec))

    def test_indo(self):
        for bet in all_odds:
            conv, dec = bet.indo, bet.decimal
            o = Odds.indo(conv)
            self.assertEqual(o.decimal, dec,
                             msg='conv: {0} = dec: {1}'.format(conv, dec))

    def test_malay(self):
        for bet in all_odds:
            conv, dec = bet.malay, bet.decimal
            o = Odds.malay(conv)
            self.assertEqual(o.decimal, dec)
#                             msg='conv: {0} = dec: {1}'.format(conv, dec))

    def test_compare_normal(self):
        self.assertEqual(Odds.fractional('1/2') == 1.5, True)
        self.assertEqual(Odds.fractional('2/1') == 3.0, True)
        self.assertTrue(Odds.fractional('2/1') == Odds.fractional('2/1'))
        self.assertEqual(Odds(1.5) < 1, False)
        self.assertEqual(Odds(0.5) > 1, False)
        self.assertEqual(Odds(1.5) != 1.0, True)
        self.assertEqual(Odds(1.5) != 1.5, False)
