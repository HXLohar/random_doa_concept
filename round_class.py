
class symbol:
    def __init__(self, new_symbol):
        self.symbol = new_symbol
        self.sticky = False
        self.multiplier = 1
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

        self.spins = []
        self.round_type = "base"
        self.seed = 0
        self.sticky_wilds = []
        self.total_win = 0

