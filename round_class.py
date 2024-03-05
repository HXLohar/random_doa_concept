import random
import numpy as np

class symbol:
    def __init__(self, new_symbol):
        self.symbol = new_symbol
        self.sticky = False
        self.multiplier = 1
        self.is_converted = False
def get_symbol_list(class_spin, payline_id):
    symbol_list = []
    for i in range(0, 5):
        index = (payline_id[i]-1)*5 + i
        symbol_list.append(class_spin.symbols[index])
    return symbol_list
def get_payout(symbol_id, OAKs):
    if OAKs < 3:
        return 0
def calc_payline(symbol_list):
    # param: 5 symbols, in the correct order
    payout_symbol = "W"
    flag_symbol_confirmed = False
    for i in range(0, 5):
        if i < 3 and symbol_list[i] == "S":
            return 0
        if not symbol_list[i] in ["W", "S"] and not flag_symbol_confirmed:
            payout_symbol = symbol_list[i]
            flag_symbol_confirmed = True
        if flag_symbol_confirmed and payout_symbol != symbol_list[i]:
            break

    OAKs = i + 1

    payout = get_payout(payout_symbol, OAKs)

    for i in range(0, 5):
        payout *= symbol_list[i].multiplier
    return payout

class spin:
    def __init__(self):
        self.symbols = []
class round:
    def __init__(self):

        self.round_type = "base"
        self.cost_multi = 1.0
        self.spins_left = 0
        self.seed = 0
        self.sticky_wilds = []
        self.spin_win = []
        self.total_win = 0
        self.msg = ""
    def throw_dead_spin(self):
        self.msg = "(dead spin)"

    def base_spin(self):
        round_task_odds = []

        # round_task_odds: determine the intended task of the spin
        # but the result can go higher than the intended goal, mainly due to 2S converting to wilds with multiplier.
        # this is only valid for 0-2 scatter spins.
        # 0: dead spin
        # 1: <1x
        # 2: 1x-3x
        # 3: 3x-5x
        # 4: 5x-10x
        # 5: 10x-25x
        # 6: 25x-100x
        # 7: 100x-300x
        # 8: 300x+

        scatter_odds = [96034270, 3469000, 480000, 15400, 1330]

        # the odds of getting 0-5 scatters (per 100M spins)

        if self.round_type == "extra_bet":
            round_task_odds = []
            scatter_odds = [89049320, 9872000, 1035000, 39300, 4380]
        else:
            pass


    def place_scatters(self, scatter_count):
        # return a list, which indicates where to place those scatters.

        # yeah, different reels have different weights.
        # remember gulag and the rave seems to have similar design, where landing a scatter on the last reel is much
        # harder comparing to previous reels.

        if scatter_count == 0:
            return []
        if scatter_count == 5:
            return [0, 1, 2, 3, 4]

        if not self.round_type == "extra_bet":
            reel = [0, 1, 2, 3, 4]
            probabilities = [14, 40, 40, 28, 6]
            result = np.random.choice(reel, scatter_count, p=np.array(probabilities) / sum(probabilities), replace=False)
            result_list = result.tolist()
        else:
            reel = [0, 2, 3, 4]
            probabilities = [12, 46, 26, 4]
            result = np.random.choice(reel, scatter_count-1, p=np.array(probabilities) / sum(probabilities),
                                      replace=False)
            result_list = result.tolist()
            result_list.append(1)
        return result_list











