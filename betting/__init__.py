from decimal import Decimal, getcontext, ROUND_CEILING
TWO_PLACES = Decimal(10) ** -2

# Always round upwards
getcontext().rounding = ROUND_CEILING


def ROUND(val, fp=TWO_PLACES):
    return val.quantize(fp)

from odds import Odds
from bets import Bet
