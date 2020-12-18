import operator
import re

class IntExpr:
    def __init__(self, val):
        self.val = int(val)

    def evaluate(self):
        return self.val

    def advanced_evaluate(self):
        return self.val

    def __repr__(self):
        return str(self.val)

class Expr:
    def __init__(self, parts):
        self.parts = parts

    def evaluate(self):
        result = self.parts[0].evaluate()
        for i in range(1, len(self.parts), 2):
            op = self.parts[i]
            next = self.parts[i+1]
            result = op(result, next.evaluate())
        return result

    def advanced_evaluate(self):
        result = 1
        factor = self.parts[0].advanced_evaluate()
        for i in range(1, len(self.parts), 2):
            op = self.parts[i]
            next = self.parts[i+1]
            if op == operator.mul:
                # start a new factor
                result *= factor
                factor = next.advanced_evaluate()
            else:
                # continue this factor
                factor += next.advanced_evaluate()
        return result * factor

    def __repr__(self):
        return repr(self.parts)

def parse(line):
    line = re.sub(r'([()])', r' \1 ', line)
    tokens = line.split()
    end, expr = parse_inner(tokens, 0)
    assert end == len(tokens)
    return expr

def parse_inner(tokens, pos):
    parts = []
    while pos < len(tokens):
        if tokens[pos] == ')':
            return pos, Expr(parts)
        elif tokens[pos] == '(':
            pos, subexpr = parse_inner(tokens, pos + 1)
            assert tokens[pos] == ')'
            parts.append(subexpr)
        elif tokens[pos] == '+':
            parts.append(operator.add)
        elif tokens[pos] == '*':
            parts.append(operator.mul)
        else:
            # must be a number
            parts.append(IntExpr(tokens[pos]))
        pos += 1
    return pos, Expr(parts)

with open("input.txt") as f:
    exprs = [parse(line.strip()) for line in f]

# part 1
print(sum(expr.evaluate() for expr in exprs))

# part 2
print(sum(expr.advanced_evaluate() for expr in exprs))

