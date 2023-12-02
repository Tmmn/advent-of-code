class GameMaster:
    def __init__(self, game_nr, games):
        self._max_cubes = {"red": 12, "blue": 14, "green": 13}
        if game_nr == 2:
            results = [self.play2(ln[:-1]) for ln in games]
        else:
            results = [self.play(ln[:-1]) for ln in games]
        self.sum = sum(results)

    def play(self, line):
        game_name, game = line.split(": ")
        game_id = game_name.split(" ")[1]
        game_set = game.split("; ")
        for revealed in game_set:
            cubes = revealed.split(", ")
            for cube in cubes:
                num, col = cube.split(" ")
                if int(num) > self._max_cubes[col]:
                    return 0
        return int(game_id)

    @staticmethod
    def play2(line):
        game = line.split(": ")[1]
        game_set = game.split("; ")
        biggest = {"red": 0, "blue": 0, "green": 0}
        for revealed in game_set:
            cubes = revealed.split(", ")
            for cube in cubes:
                num, col = cube.split(" ")
                if biggest[col] < int(num):
                    biggest[col] = int(num)
        power = 1
        for i in biggest.values():
            power *= i
        return power


if __name__ == "__main__":
    with open('02.txt', 'r') as source:
        lines = source.readlines()
    elf1 = GameMaster(1, lines)
    print(elf1.sum)

    elf2 = GameMaster(2, lines)
    print(elf2.sum)
