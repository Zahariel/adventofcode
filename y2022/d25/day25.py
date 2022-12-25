


SNAFU_DIGITS = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

DIGITS_SNAFU = {v: k for (k, v) in SNAFU_DIGITS.items()}

def unSNAFU(snafu):
    answer = 0
    for c in snafu:
        answer *= 5
        answer += SNAFU_DIGITS[c]
    return answer


def parse(line):
    return unSNAFU(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

final_answer = sum(lines)
print(final_answer)

def snafu(val):
    answer = []
    while val != 0:
        digit = (val + 2) % 5 - 2
        answer.append(DIGITS_SNAFU[digit])
        val = (val + 2) // 5

    return "".join(reversed(answer))

print(snafu(final_answer))
