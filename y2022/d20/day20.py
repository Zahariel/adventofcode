

def parse(line):
    return int(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]


class Node:
    def __init__(self, value, modulus=0):
        self.value = value
        if modulus == 0:
            self.usable_value = value
        else:
            self.usable_value = value % modulus
        self.next = self
        self.prev = self

    def __repr__(self):
        return f"Node({self.value})"

    def mix(self):
        # remove self
        next = self.next
        prev = self.prev
        next.prev = prev
        prev.next = next

        # find insertion point
        victim = prev
        if self.usable_value < 0:
            for _ in range(-self.usable_value):
                victim = victim.prev
        else:
            for _ in range(self.usable_value):
                victim = victim.next

        # insert self
        self.next = victim.next
        self.prev = victim
        victim.next = self
        self.next.prev = self

nodes = [Node(val) for val in lines]
zero_node = None
for i, n in enumerate(nodes):
    n.next = nodes[(i+1) % len(nodes)]
    n.prev = nodes[i-1]
    if n.value == 0: zero_node = n

def print_buffer(node):
    print(node.value, end=", ")
    ptr = node.next
    while ptr is not node:
        print(ptr.value, end=", ")
        ptr = ptr.next
    print()

# work in original order
# print_buffer(zero_node)
for n in nodes:
    # print(f"processing {n}")
    n.mix()
    # print_buffer(zero_node)


ptr = zero_node
selected = []
for _ in range(3):
    for _ in range(1000):
        ptr = ptr.next
    selected.append(ptr)

print(selected)
print(sum(n.value for n in selected))

# part 2
DECRYPTION_KEY = 811589153
nodes = [Node(val * DECRYPTION_KEY, len(lines) - 1) for val in lines]
zero_node = None
for i, n in enumerate(nodes):
    n.next = nodes[(i+1) % len(nodes)]
    n.prev = nodes[i-1]
    if n.value == 0: zero_node = n

for _ in range(10):
    for n in nodes:
        n.mix()

ptr = zero_node
selected = []
for _ in range(3):
    for _ in range(1000):
        ptr = ptr.next
    selected.append(ptr)

print(selected)
print(sum(n.value for n in selected))
