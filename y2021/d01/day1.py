

with open("input.txt") as f:
    lines = f.readlines()
    data = [int(line) for line in lines]

increase_count = 0
for i in range(1,len(data)):
    if data[i] > data[i-1]:
        increase_count += 1

print(increase_count)

windows = [data[i-2] + data[i-1] + data[i] for i in range(2, len(data))]
increase_count = 0
for i in range(1,len(windows)):
    if windows[i] > windows[i-1]:
        increase_count += 1

print(increase_count)
