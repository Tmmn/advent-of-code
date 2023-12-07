import time


# decorator that prints result that execution time when calling calculate_winnings method
def runner(func):
    def wrapper(*args):
        start = time.perf_counter_ns()
        result = func(*args)
        end = time.perf_counter_ns()
        execution_time = end - start
        print(f"Function '{func.__name__}' took {(10e-6 * execution_time):.3f} ms to execute "
              f"and the result is: {result}")
        return result
    return wrapper

class CamelCards:
    def __init__(self, hands):
        self._rank = \
            {"A": 12, "K": 11, "Q": 10, "J": 9, "T": 8, "9": 7, "8": 6, "7": 5, "6": 4, "5": 3, "4": 2, "3": 1, "2": 0}
        self.hands = hands

    @runner
    def calculate_winnings(self):
        # general idea: first sort by type and then by power
        # create dictionary where the hands are sorted by their type (dict keys)
        hands_by_type = {x: [] for x in range(1, 8)}
        # fill the dict
        for hand in self.hands:
            cards = hand[0]  # hand[1] would get you the bet
            hands_by_type[self._get_type(cards)].append(hand)
        # sort list of hands of the same type that are in hands_by_type
        for hand_type in hands_by_type.keys():
            # change method call here if you want to switch sorting algorithm
            self._insertion_sort(hands_by_type[hand_type])
        # join all sorted hands together into big list
        all_hands_sorted = [item for sublist in hands_by_type.values() for item in sublist]
        # go through big list and calculate winnings by multiplying with index
        winning_sum = 0
        for i, hand in enumerate(all_hands_sorted, 1):
            winning_sum += hand[1] * i  # betting value times rank
        return winning_sum

    # both sorting functions work
    def _bubble_sort(self, array):
        for i in range(len(array) - 1, 0, -1):
            for j in range(1, i+1):
                if self._compare(array[j][0], array[j-1][0]):
                    array[j], array[j-1] = array[j-1], array[j]

    def _insertion_sort(self, array):
        for i in range(1, len(array)):
            j = i - 1
            temp = array[i]
            while j >= 0 and self._compare(temp[0], array[j][0]):  # temp[0] < array[j][0]
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = temp

    # helper function for sorting
    # returns necessary condition to decide whether one value is smaller or larger than the other
    def _compare(self, hand1, hand2):
        for i in range(len(hand1)):
            if self._rank[hand1[i]] < self._rank[hand2[i]]:
                return True
            elif self._rank[hand1[i]] > self._rank[hand2[i]]:
                return False
        return False

    def _get_type(self, cards):
        # count how often we have one kind of card
        unique_chars = {card: cards.count(card) for card in set(cards)}
        # get the type of hand
        return self._help_get_type(unique_chars)

    @staticmethod
    def _help_get_type(unique_chars):
        # Five of a kind
        if 5 in unique_chars.values():
            return 7
        # Four of a kind
        elif 4 in unique_chars.values():
            return 6
        # Full house
        elif 3 in unique_chars.values() and 2 in unique_chars.values():
            return 5
        # Three of a kind
        elif 3 in unique_chars.values():
            return 4
        # Two pair
        elif 2 == list(unique_chars.values()).count(2):
            return 3
        # One pair
        elif 1 == list(unique_chars.values()).count(2):
            return 2
        # High card
        elif 5 == list(unique_chars.values()).count(1):
            return 1

        raise Exception


class CamelCardsNEW(CamelCards):
    def __init__(self, hands):
        super().__init__(hands)
        # same hands but new ranking system
        self._rank = \
            {"A": 12, "K": 11, "Q": 10, "T": 9, "9": 8, "8": 7, "7": 6, "6": 5, "5": 4, "4": 3, "3": 2, "2": 1, "J": 0}

    def _get_type(self, cards):
        jokers = cards.count("J")
        unique_chars = {card: cards.count(card) for card in set(cards) if card != "J"}
        if not unique_chars:  # if there are no other cards than jokers
            unique_chars = {"J": 0}
        # add jokers to the value of card with the highest count
        unique_chars[max(unique_chars, key=unique_chars.get)] += jokers
        return super()._help_get_type(unique_chars)


if __name__ == "__main__":
    with open('07.txt', 'r') as source:
        lines = []
        for line in source.readlines():
            h = line.split()[0]
            b = int(line.split()[1])
            lines.append([h, b])
    # PART 1
    ride_desert_island = CamelCards(lines)
    ride_desert_island.calculate_winnings()

    # PART 2
    ride_desert_island_round_2 = CamelCardsNEW(lines)
    ride_desert_island_round_2.calculate_winnings()
