def first_and_last_digit(line):
    i, j = 0, len(line)-1
    first, last = None, None
    while first is None or last is None:
        if i >= len(line) or j < 0:
            raise NotImplementedError(f"{line} without any number")
        if first is None and line[i].isnumeric():
            first = int(line[i])
        if last is None and line[j].isnumeric():
            last = int(line[j])
        i += 1
        j -= 1

    return first * 10 + last

def first_and_last_digits_with_letters(line):
    # one:3, two:3, three:5, four:4, five:4, six:3, seven:5, eight:5, nine:4, zero:4
    helper = {3: {"one": 1, "two": 2, "six": 6}, 4: {"four": 4, "five": 5, "nine": 9, "zero": 0},
              5: {"three": 3, "seven": 7, "eight": 8}}
    i, j = 0, len(line)-1
    first, last = None, None
    while first is None or last is None:
        if i >= len(line) or j < 0:
            raise NotImplementedError(f"{line} without any number")

        # first
        if first is None:
            if line[i].isnumeric():
                first = int(line[i])
            # 3
            elif i < len(line) - 2 and line[i:i+3] in helper[3]:
                first = helper[3][line[i:i+3]]
            # 4
            elif i < len(line) - 3 and line[i:i+4] in helper[4]:
                first = helper[4][line[i:i+4]]
            # 5
            elif i < len(line) - 4 and line[i:i+5] in helper[5]:
                first = helper[5][line[i:i+5]]
            i += 1

        # last
        if last is None:
            if line[j].isnumeric():
                last = int(line[j])
            # 3
            elif j >= 2 and line[j-2:j+1] in helper[3]:
                last = helper[3][line[j-2:j+1]]
            # 4
            elif j >= 3 and line[j-3:j+1] in helper[4]:
                last = helper[4][line[j-3:j+1]]
            # 5
            elif j >= 4 and line[j-4:j+1] in helper[5]:
                last = helper[5][line[j-4:j+1]]
            j -= 1
    return first * 10 + last

def main():
    with open('01.txt', 'r') as source:
        lines = source.readlines()

    result1 = [first_and_last_digit(line[:-1]) for line in lines]
    print(sum(result1))

    # test = [
    #     "one\n",
    #     "oneight\n",
    #     "bathree45six\n",
    #     "oh4ahdsfone4\n",
    #     "oh4ahsdfone4o\n"
    # ]
    # test_result = [first_and_last_digits_with_letters(line[:-1]) for line in test]
    # print(test_result)

    result2 = [first_and_last_digits_with_letters(line[:-1]) for line in lines]
    print(sum(result2))

if __name__ == "__main__":
    main()
