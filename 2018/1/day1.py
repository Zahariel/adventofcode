
freq = 0
done = False
seen = set()
seen.add(freq)

while not done:
    with open("day1input.txt") as file:
        for line in file:
            freq += int(line.strip())
            if freq in seen:
                print(freq)
                done = True
                break
            seen.add(freq)


print(freq)
