import unittest

from betting import Bet, Odds
from betting.bets import BetDetail


class TestOdds(unittest.TestCase):
    def test_should_not_error(self):
        Bet(100, home=Odds(2), draw=Odds(3.1), away=Odds(3.7))

    def test_break_even(self):
        self.assertTrue(Bet(100, home=Odds(2.47), draw=Odds(3.1),
                            away=Odds(3.7)).break_even())
        self.assertFalse(Bet(100, home=Odds(2.0), draw=Odds(3.1),
                             away=Odds(3.7)).break_even())

    def test_fulfill_placement(self):
        self.assertFalse(Bet(100, home=Odds(2.4), draw=Odds(3.1),
                             away=Odds(3.7)).fulfill_placement())

        b = Bet(100, home=Odds(2.47), draw=Odds(3.1), away=Odds(3.7))
        self.assertTrue(b.fulfill_placement())

        details = [BetDetail(name='home', placed=40.52, outcome=100.49),
                   BetDetail(name='away', placed=27.13, outcome=100.66),
                   BetDetail(name='draw', placed=32.35, outcome=100.61)]
        placements = b.placements
        s = 0.0

        for detail in details:
            for p in placements:
                if(p.name == detail.name and p.placed == detail.placed
                   and p.outcome == detail.outcome):
                    placements.remove(p)
                    s += p.placed

        self.assertTrue(len(placements) == 0)
        self.assertEqual(b.bet, b.sum_placed)
        self.assertEqual(b.sum_placed, s)
