
# test
# puzzle_input = "389125467"

# real
import typing

puzzle_input = "135468729"

class Node:
    def __init__(self, val, prev=None, next=None):
        if prev is None: prev = self
        if next is None: next = self

        self.val = val
        self.prev = prev
        self.next = next


class Circle:
    def __init__(self, vals: typing.Sequence[int]):
        self.size = len(vals)
        self.nodes:typing.List[typing.Optional[Node]] = [None] * (self.size + 1)
        self.root = Node(vals[0])
        self.nodes[self.root.val] = self.root
        for val in vals[1:]:
            self.root = self.insert(val)
        self.root = self.root.next

    def insert(self, val, where=None):
        if where is None: where = self.root
        if not self.nodes[val]:
            self.nodes[val] = Node(val)
        self.nodes[val].prev = where
        self.nodes[val].next = where.next
        where.next = self.nodes[val]
        self.nodes[val].next.prev = self.nodes[val]
        return self.nodes[val]

    def pop(self):
        result = self.root.val
        self.root.prev.next = self.root.next
        self.root.next.prev = self.root.prev
        self.root = self.root.next
        return result

    def one_turn(self):
        current_val = self.root.val
        self.root = self.root.next
        removed = [self.pop(), self.pop(), self.pop()]
        target_val = (current_val - 2) % self.size + 1
        while target_val in removed:
            target_val = (target_val - 2) % self.size + 1

        # go find target
        target = self.nodes[target_val]
        for val in removed:
            target = self.insert(val, target)

    def __str__(self):
        vals = [self.root.val]
        walker = self.root.next
        while walker != self.root:
            vals.append(walker.val)
            walker = walker.next
        return str(vals)


circle = Circle([int(val) for val in puzzle_input])

ROUNDS = 100
for i in range(ROUNDS):
    print(i+1, circle)
    circle.one_turn()

print(101, circle)

CIRCLE_SIZE = 1_000_000
circle_nums = list(range(1, CIRCLE_SIZE+1))
circle_nums[:len(puzzle_input)] = [int(val) for val in puzzle_input]

circle = Circle(circle_nums)

ROUNDS = 10_000_000
for i in range(ROUNDS):
    if i % 100_000 == 0:
        print(i)
    circle.one_turn()

one = circle.nodes[1]
print(one.next.val, one.next.next.val, one.next.val * one.next.next.val)

