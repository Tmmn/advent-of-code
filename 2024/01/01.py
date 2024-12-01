
def part_1():
    with open("01.txt", "r") as f:
        parsed_list = [[int(i.strip().split("   ")[0]), int((i.strip().split("   "))[1])] for i in f.readlines()]
    left_list = sorted([i[0] for i in parsed_list])
    right_list = sorted([i[1] for i in parsed_list])
    distance_list = [abs(i - j) for i, j in zip(left_list, right_list)]
    print(sum(distance_list))
    return parsed_list

def part_2(input_list):
    left_list = [i[0] for i in input_list]
    right_list = [i[1] for i in input_list]
    score = 0
    for i in left_list:
        score += i * right_list.count(i)
    print(score)

if __name__ == "__main__":
    notes = part_1()
    part_2(notes)
