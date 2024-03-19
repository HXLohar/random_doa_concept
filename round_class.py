import random
import numpy as np

class symbol:
    def __init__(self, new_symbol="empty"):
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
    PAYTABLE_FILENAME = "config_paytable.txt"
    with open(PAYTABLE_FILENAME, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            if parts[0].strip() == symbol_id:
                values = parts[1].strip().split("/")
                return float(values[OAKs - 3])

def map_symbol_to_value(symbol_string):
    symbol_map = {
        "W": 0,
        "H1": 1,
        "H2": 2,
        "H3": 3,
        "H4": 4,
        "H5": 5,
        "L1": 6,
        "L2": 7,
        "L3": 8,
        "L4": 9,
        "L5": 10
    }
    return symbol_map.get(symbol_string, None)

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
        self.blocks = []
        self.cost_multi = 1.0
        self.spins_left = 0
        self.seed = 0
        self.sticky_wilds = []
        self.spin_win = []
        self.total_win = 0
        self.msg = ""
        for i in range(0, 5):
            reel = []
            for j in range(0, 4):
                reel.append(symbol())
            self.blocks.append(reel)

    def throw_dead_spin(self):
        self.msg = "(dead spin)"

    def base_spin(self):

        scatter_count = [0, 1, 2, 3, 4, 5]
        scatter_odds = [85034270, 11000000, 3469000, 480000, 15400, 1330]

        # the odds of getting 0-5 scatters (per 100M spins)
        if self.round_type == "extra_bet":

            scatter_odds = [0, 89049320, 9872000, 1035000, 39300, 4380]
        scatter_count = random.choices(scatter_count, weights=scatter_odds, k=1)[0]

        # First, generate a board at random.
        # Only H1-H5, L1-L5 and Ww might appear.
        symbol_list = ["W, H1, H2, H3, H4, H5, L1, L2, L3, L4, L5"]
        symbol_weight = [170,
                         440, 640, 720, 980, 1040,
                         1720, 2160, 2360, 2580, 2900]

        for reel in self.blocks:
            symbol_adjustment = [1.0] * 11
            adjusted_symbol_weight = [x * y for x, y in zip(symbol_weight, symbol_adjustment)]
            for item in reel:
                for i in range(0, 11):
                    adjusted_symbol_weight.append(symbol_weight[i] * symbol_adjustment[i])
                new_symbol = random.choices(symbol_list, weights=adjusted_symbol_weight, k=1)[0]
                if new_symbol == "W":
                    symbol_adjustment[0] -= 1
                else:
                    symbol_adjustment[map_symbol_to_value(new_symbol)] -= 0.5
                item.symbol = new_symbol


        # todo
        # symbol weight might randomly fluctuate. like randomly you might enter a "premium" spin
        # and in that spin, it's much more likely to land premium symbols
        # will do it later

        # Second, create some "intentional" wins.
        # todo

        # Determine which reel got scatters
        scatter_reels = self.determine_scatter_reels(scatter_count)
        # Place scatters. This overwrites existing symbols
        for i in range(0, 5):
            if not i in scatter_reels:
                continue
            self.place_scatter(i)
        # convert it to x2-x4 Wilds, if only 2 S lands
        if scatter_count == 2:
            self.convert_scatters()
    def debug_print(self):
        # todo
        # print some strings about the current board
        # will do this tomorrow (maybe)
        pass

    def place_scatter(self, reel_id):
        height = random.randint(0, 3)
        for i in range(0, 4):
            if self.blocks[reel_id][i].symbol == "W":
                height = i
        self.blocks[reel_id][height].symbol = "S"
    def convert_scatters(self):
        for i in range(0, 5):
            for j in range(0, 4):
                if self.blocks[i][j].symbol == "S":
                    self.blocks[i][j].symbol = "W"
                    if self.blocks[i][j].multiplier < 2:
                        multi_list = [2, 3, 4]
                        weight_list = [54, 34, 12]
                        self.blocks[i][j].multiplier = random.choices(multi_list, weights=weight_list, k=1)[0]

    def get_winning_lines(self):
        # todo
        # return a list of winning paylines
        pass
    def get_occupied_blocks(self):
        # todo
        # occupied: it's not W, and part of an existing payline
        # so replacing it with something else will break that payline
        pass
    def get_available_lines(self, OAKs):
        # todo
        # search for non-winning lines that are safe to throw in
        # a X OAKs win, where X is the OAks param given
        # returns a list
        pass

    def determine_scatter_reels(self, scatter_count):
        # return a list, which indicates where to place those scatters.

        # yeah, different reels have different weights.
        # remember gulag and the rave seems to have similar design, where landing a scatter on the last reel is much
        # harder comparing to previous reels.

        if scatter_count == 0:
            return []
        if scatter_count == 5:
            return [0, 1, 2, 3, 4]
        if scatter_count == 1 and self.round_type == "extra bet":
            return [1]

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











