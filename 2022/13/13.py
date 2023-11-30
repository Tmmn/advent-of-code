import json


def check_pair(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    if isinstance(left, list) and isinstance(right, list):
        for e1, e2 in zip(left, right):
            if (comparison := check_pair(e1, e2)) is not None:
                return comparison
        return check_pair(len(left), len(right))

    if isinstance(left, int):
        return check_pair([left], right)
    return check_pair(left, [right])


packets = {}
with open('13.txt', 'r') as f:
    for index, packet in enumerate(f.read().split("\n\n")):
        split_packet = packet.split("\n")
        packets[index + 1] = [json.loads(split_packet[0])]
        packets[index + 1].append(json.loads(split_packet[1]))

indices = [i for i in packets if check_pair(packets[i][0], packets[i][1])]
print(f"sum for part 1: {sum(indices)}")

all_packets = [p for pack in packets.values() for p in pack]
# + 1 and + 2 because [[2]] and [[6]] are extra
position1 = 1 + sum([1 for p in all_packets if check_pair(p, [[2]])])
position2 = 2 + sum([1 for p in all_packets if check_pair(p, [[6]])])
print(f"product for part 2: {position1 * position2}")
