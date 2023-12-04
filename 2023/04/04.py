class CardGame:
    def __init__(self, cards):
        self.cards = cards
        self.points = self._calculate_points()
        self.new_points = self._calculate_new_points()

    def _calculate_new_points(self):
        table = {i: 1 for i in range(1, len(self.cards)+1)}
        for card in self.cards:
            wins = 0
            card_nr, all_numbers = card[:-1].split(": ")
            card_nr = int(card_nr.split()[1])
            win_nums, my_nums = all_numbers.split(" | ")
            win_nums = win_nums.split()
            my_nums = my_nums.split()
            for number in win_nums:
                if number in my_nums:
                    wins += 1
            for i in range(1, wins+1):
                try:
                    table[card_nr+i] += table[card_nr]
                except KeyError:
                    break
        return sum(table.values())

    def _calculate_points(self):
        total_points = 0
        for card in self.cards:
            points = 0
            all_numbers = card[:-1].split(": ")[1]
            win_nums, my_nums = all_numbers.split(" | ")
            win_nums = win_nums.split()
            my_nums = my_nums.split()
            for number in win_nums:
                if number in my_nums:
                    points = (points * 2) if points != 0 else 1
            total_points += points
        return total_points


if __name__ == "__main__":
    with open('04.txt', 'r') as source:
        lines = source.readlines()
    game1 = CardGame(lines)
    print(game1.points)
    print(game1.new_points)
