start = [5,1,9,18,13,8,0]

def calc_end(end):
    history = {num: i for i, num in enumerate(start[:-1])}
    i = len(start)
    last = start[-1]
    next = 0
    while i < end:
        if last in history:
            next = (i - 1) - history[last]
        else:
            next = 0
        history[last] = i - 1
        last = next
        i += 1
    return next


print(calc_end(2020))
print(calc_end(30000000))
