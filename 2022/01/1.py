calories = []
calorie_sum = 0

with open('1.txt', 'r') as f:
    for line in f:
        if line[:-1] == "":
            calories.append(calorie_sum)
            calorie_sum = 0
        else:
            calorie_sum += int(line[:-1])

calories.sort(reverse=True)

print(f"the highest calorie sum is: {max(calories)}")
print(f"the sum of the top 3 sums is: {sum(calories[:3])}")
