
class Num:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def check_explode(self, depth):
        return False, self, None, None

    def accept_left(self, num):
        self.val += num

    def accept_right(self, num):
        self.val += num

    def check_split(self):
        if self.val > 9:
            left = self.val // 2
            right = self.val - left
            return True, Pair(Num(left), Num(right))
        else:
            return False, self

    def magnitude(self):
        return self.val

    def clone(self):
        return Num(self.val)

class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"[{self.left},{self.right}]"

    def check_explode(self, depth):
        if depth == 4:
            # do explode
            return True, Num(0), self.left.val, self.right.val
        else:
            # process left
            result, self.left, left_val, right_val = self.left.check_explode(depth + 1)
            if result:
                if right_val is not None:
                    self.right.accept_left(right_val)
                return True, self, left_val, None
            else:
                result, self.right, left_val, right_val = self.right.check_explode(depth + 1)
                if result:
                    if left_val is not None:
                        self.left.accept_right(left_val)
                    return True, self, None, right_val
                else:
                    return False, self, None, None

    def accept_left(self, num):
        self.left.accept_left(num)

    def accept_right(self, num):
        self.right.accept_right(num)

    def check_split(self):
        result, self.left = self.left.check_split()
        if not result:
            result, self.right = self.right.check_split()
        return result, self

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def clone(self):
        return Pair(self.left.clone(), self.right.clone())

def parse_pair(str, idx):
    assert str[idx] == "["
    idx += 1
    if str[idx] == "[":
        idx, left = parse_pair(str, idx)
    else:
        idx, left = idx + 1, Num(int(str[idx]))
    assert str[idx] == ","
    idx += 1
    if str[idx] == "[":
        idx, right = parse_pair(str, idx)
    else:
        idx, right = idx + 1, Num(int(str[idx]))
    assert str[idx] == "]"
    idx += 1
    return idx, Pair(left, right)

def parse(line):
    return parse_pair(line, 0)

with open("input.txt") as f:
    lines = f.readlines()
    data = [parse(line)[1] for line in lines]


def one_step(pair):
    result, pair, _, _= pair.check_explode(0)
    if result:
        return "explode", pair
    else:
        result, pair = pair.check_split()
        if result:
            return "split", pair
        else:
            return None, pair

def process(pair):
    action = "start"
    # print(pair)
    while action is not None:
        action, pair = one_step(pair)
        # print(action, pair)
    return pair

# part 1

current = data[0].clone()
for pair in data[1:]:
    current = Pair(current, pair.clone())
    current = process(current)
    # print(current)

print(current)
print(current.magnitude())

# part 2

largest = 0
bigl, bigr = None, None
for left in data:
    for right in data:
        if left is right: continue
        result = process(Pair(left.clone(), right.clone())).magnitude()
        if result > largest:
            largest = result
            bigl = left
            bigr = right

print(bigl)
print(bigr)
print(largest)


