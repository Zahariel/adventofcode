
with open("input.txt") as file:
    input = file.readline().rstrip()

def find_packet(SIZE):
    for i in range(len(input) - SIZE + 1):
        if len(set(input[i:i + SIZE])) == SIZE:
            return i + SIZE

print(find_packet(4))
print(find_packet(14))


