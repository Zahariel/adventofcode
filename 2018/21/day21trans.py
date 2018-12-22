r4 = 0
last_r4 = 0
seen = set()
i = 0
while True:
    if i % 10000 == 0:
        print(i)
    r5 = r4 | 0x10000
    r4 = 0x1C4E46
    while True:
        r2 = r5 & 0xFF
        r4 += r2
        r4 &= 0xFFFFFF
        r4 *= 65899
        r4 &= 0xFFFFFF
        if 256 > r5:
            break
        r5 = r5 // 0x100
    if r4 in seen:
        print("repeat found", r4)
        print("last r4 was", last_r4)
        break
    seen.add(r4)
    last_r4 = r4
    i += 1
    # print("%8d"%r4, "0x%06x"%r4)
    # input()
