
MIN = 165432
MAX = 707912

def legal(input):
    digits = str(input)
    double = False
    for i in range(5):
        if digits[i] == digits[i+1]:
            if (i == 0 or digits[i-1] != digits[i]) and (i == 4 or digits[i+1] != digits[i+2]):
                double = True
        elif digits[i] > digits[i+1]:
            return False
    return double


print(sum(1 for x in range(MIN, MAX+1) if legal(x)))
