from collections import namedtuple
from decimal import Decimal, getcontext
from . import ROUND

getcontext().prec = 10
BetDetail = namedtuple('BetDetail', 'name placed outcome')


class Bet(object):
    _placements = []

    def __init__(self, bet, **kwargs):
        self.bet = Decimal(bet)
        self.odds = {}
        self.placed = {}
        self.outcome = {}
        self.sum_placed = Decimal(0.0)

        for name, odds in kwargs.items():
            self.odds[name] = ROUND(Decimal(odds.decimal))
            bet = ROUND(self.bet / self.odds[name])
            self._bet(name, bet, odds.decimal)

    @property
    def placements(self):
        if len(self._placements) == 0:
            for name in self.placed.keys():
                self._placements.append(
                    BetDetail(name,
                              float(self.placed[name]),
                              float(self.outcome[name]))
                )

        return self._placements

    @property
    def max_outcome(self): return max(self.placements, key=lambda x: x.outcome)

    @property
    def min_outcome(self): return min(self.placements, key=lambda x: x.outcome)

    @property
    def min_odds(self): return min(self.odds, key=lambda x: x[1])

    @property
    def max_odds(self): return max(self.odds, key=lambda x: x[1])

    def _bet(self, name, amount, odds):
        '''
        To keep track of all things that needs to be re-calculated when a
        bet is made.
        Changed the placed amount, change the possible outcome, change
        the calculated sum for placed and clear out the placements.
        '''
        prev = Decimal(0)
        if name in self.placed: prev = Decimal(self.placed[name])
        self.placed[name] = amount
        self.outcome[name] = ROUND(amount * Decimal(odds))

        if prev > amount:
            self.sum_placed -= prev - amount
        else:
            self.sum_placed += amount - prev

        self._placements = []

    def break_even(self):
        return self.bet > self.sum_placed

    def fulfill_placement(self):
        '''
        If the bet has broken even and there is still some money to bet,
        put it to good use eavenly against all three.

        If the extra amount can't be evenly split then give the one with
        the highest bet the least amount extra.
        '''
        extra = self.bet - self.sum_placed
        if extra <= 0.00: return False

        # Since rounding is always done towards ceil we need to adjust for it.
        num_odds = len(self.odds)
        to_add = ROUND(extra / num_odds)
        placed = self.placed.keys()

        # Remove the excess from extra from the one with the highest odds,
        # since that's the one that is the least likely to win.
        if (to_add * num_odds) > extra:
            name = self.max_odds
            diff = to_add - ((to_add * 3) - extra)
            self._bet(name, self.placed[name] + diff, self.odds[name])
            placed.remove(name)

        for name in placed:
            self._bet(name, self.placed[name] + to_add, self.odds[name])

        return True
