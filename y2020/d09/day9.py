with open("input.txt") as f:
    numbers = [int(line.strip()) for line in f]

BUFFER_LENGTH = 25
pos = 0
buffer = numbers[:BUFFER_LENGTH]
buffer_set = set(buffer)

def validate(target, buffer, buffer_set):
    for old in buffer:
        if target != 2 * old and (target - old) in buffer_set:
            return True
    return False


impostor = -1
for target in numbers[BUFFER_LENGTH:]:
    if validate(target, buffer, buffer_set):
        buffer_set.remove(buffer[pos])
        buffer_set.add(target)
        buffer[pos] = target
        pos = (pos + 1) % BUFFER_LENGTH
    else:
        impostor = target
        break

print(impostor)

# all the numbers are positive, which makes this a lot easier
i = 0
j = 0
sum = 0
while i < len(numbers) and j <= len(numbers):
    if sum == impostor:
        break
    elif sum < impostor:
        sum += numbers[j]
        j += 1
    else:
        sum -= numbers[i]
        i += 1

minimum = min(numbers[i:j])
maximum = max(numbers[i:j])
print(i, j, minimum, maximum, minimum + maximum)

