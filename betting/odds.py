from fractions import Fraction
from decimal import Decimal
from . import ROUND


class Odds(object):
    '''
    Class to convert between different odds models.
    Internally all odds are saved as decimal.

    Models taken from Wikipedia at 2012-11-18:
      http://en.wikipedia.org/wiki/Sports_betting#Odds

    Usage:
    >>> Odds.us(-200).decimal
    1.5
    >>> Odds(-200, 'us').decimal
    1.5
    '''
    def __init__(self, odds, type='decimal'):
        '''
        Converts an input odds into decimal for further comprisons.

        Valid values for type (example odds):
        - decimal (1.5)
        - fractional (1/2)
        - us (-200)
        - hk (0.5)
        - indo (-2)
        - malay (0.5)
        '''
        self.input_odds = odds
        self.input_type = type
        self.decimal = None

        conversion = getattr(self, '_{0}'.format(type))
        self.decimal = conversion(odds)

    def __eq__(self, other): return self.decimal == other

    def __ne__(self, other): return self.decimal != other

    def __lt__(self, other): return self.decimal < other

    def __gt__(self, other): return self.decimal > other

    def _decimal(self, odds):
        '''
        Decimal shows the amount bet * odds = amount paid out if won.

        1.5 means you get 50% extra if you win, eg. 1 * 1.5 = 1.50
        0.5 means you get 50% of wagered if you win, eg. 1 * 0.5 = 0.5
        '''
        return float(odds)

    def _fractional(self, odds):
        '''
        Fractional odds of 1/2 imply that the bet would pay out 1 unit for
        every 2 units risked, while fractional odds of 2/1 imply that the
        bet would pay out $2 for every $1 risked.
        '''
        return 1 + float(Fraction(odds))

    def _us(self, odds):
        '''
        When negative, they show how big a wager is needed for a profit of
        100 and when positive they show a profit from a wager of 100.

        So -200 means the bettor bet $200, and won, would get $300.
        $100 more than the initial bet.

        So 200 means the bettor bet $100, and won, would get $300.
        $200 more than the initial bet.
        '''
        if odds > 0: return (odds / 100.0) + 1
        if odds < 0: return (-100.0 / odds) + 1

    def _hk(self, odds):
        '''
        Just the same as decimal except that it's off by one
        Eg. 0.5 hk = 1.5 dec
        '''
        return odds + 1

    def _indo(self, odds):
        '''
        When negative, they show how big wager is needed for a profit of
        1 and when positive, they show the profit from a wager of 1.

        -2 means the bettor bet 2, and won, he would get 3.
        1 more than the initial bet.

        2 means the bettor bet 1, and won, he would get 3.
        2 more than the initial bet.

        Basically the US style but at one tenth value.
        '''
        if odds >= 1: return self._hk(odds)
        if odds < 1:
            return self._hk(
                float(ROUND((1 / ROUND(Decimal(odds))) * -1))
            )

    def _malay(self, odds):
        '''
        When Malay odds are positive they are interpretted in the same manner
        as Hong Kong odds.

        When quoted as a negative number the odds figure represents the unit
        amount a bettor would need to risk in order to win 1 units.
        Malay odds of -0.50 imply a bettor would need to risk $0.50 in order
        to win $1.
        '''
        if odds >= 0: return self._hk(odds)
        print 1 / ROUND(Decimal(odds))
        print ROUND(1 / ROUND(Decimal(odds)))
        if odds < 0: return float(ROUND(1 - (1 / ROUND(Decimal(odds)))))

    @classmethod
    def fractional(cls, odds): return cls(odds, type='fractional')

    @classmethod
    def decimal(cls, odds): return cls(odds, type='decimal')

    @classmethod
    def us(cls, odds): return cls(odds, type='us')

    @classmethod
    def hk(cls, odds): return cls(odds, type='hk')

    @classmethod
    def indo(cls, odds): return cls(odds, type='indo')

    @classmethod
    def malay(cls, odds): return cls(odds, type='malay')
