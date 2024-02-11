class profile:
    def __init__(self):
        self.balance = 10000.00
        self.wagered = 0.00
        self.total_win = 0.00
        self.biggest_win = 0.00
        self.luckiest_win = 0.00
    def spin(self, base_bet, spin_option, printer_mode=0):
        pass
    def bonus_buy(self, base_bet, option, printer_mode=0):
        pass
    def print_info(self):
        print(f"Profile info\nBalance :{self.balance:,.2f}\n")