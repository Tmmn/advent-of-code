# Rock defeats Scissors,
# Scissors defeats Paper,
# Paper defeats Rock
# A => Rock, B => Paper, C => Scissors
# Part 1: X => Rock, Y => Paper, Z => Scissors
# Part 2: X => lose, Y => draw, Z => win

# scores:
# Rock: 1, Paper: 2, Scissors: 3
# lost: 0, draw: 3, win: 6

def part1(you, me):
    if me == "X":
        my_score = 1
    elif me == "Y":
        my_score = 2
    elif me == "Z":
        my_score = 3
    else:
        raise Warning("could not calculate my_score")

    # lost
    if you == "A" and me == "Z" or you == "B" and me == "X" or you == "C" and me == "Y":
        return my_score + 0
    # draw
    elif you == "A" and me == "X" or you == "B" and me == "Y" or you == "C" and me == "Z":
        return my_score + 3
    # win
    elif you == "A" and me == "Y" or you == "B" and me == "Z" or you == "C" and me == "X":
        return my_score + 6
    raise Warning("reached end of function part 1 without return")


def part2(you, goal):
    # need lose
    if goal == "X":
        if you == "A":  # rock -> scissors (3)
            my_score = 3
        elif you == "B":  # paper -> rock (1)
            my_score = 1
        elif you == "C":  # scissors -> paper (2)
            my_score = 2
        else:
            raise Warning("could not calculate my_score")
        return my_score + 0
    # need draw
    elif goal == "Y":
        if you == "A":  # rock -> rock (1)
            my_score = 1
        elif you == "B":  # paper -> paper (2)
            my_score = 2
        elif you == "C":  # scissors -> scissors (3)
            my_score = 3
        else:
            raise Warning("could not calculate my_score")
        return my_score + 3
    # need win
    elif goal == "Z":
        if you == "A":  # rock -> paper (2)
            my_score = 2
        elif you == "B":  # paper -> scissors (3)
            my_score = 3
        elif you == "C":  # scissors -> rock (1)
            my_score = 1
        else:
            raise Warning("could not calculate my_score")
        return my_score + 6
    raise Warning("reached end of function part 2 without return")


score1 = 0
score2 = 0
with open('2.txt', 'r') as f:
    for line in f:
        opponent, player = tuple(line[:-1].split())
        score1 += part1(opponent, player)
        score2 += part2(opponent, player)

print(f"your score with rules from Part 1 is: {score1}")
print(f"your score with rules from Part 2 is: {score2}")
