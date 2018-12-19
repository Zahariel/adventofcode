import re

class Point:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self):
        self.x += self.dx
        self.y += self.dy

def parse(line):
    match = re.match(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", line.strip()).groups()
    return Point(int(match[0]), int(match[1]), int(match[2]), int(match[3]))


def print_sky(sky):
    for line in sky:
        for spot in line:
            if spot:
                print("#", end="")
            else:
                print(".", end="")
        print()


MAX_SIZE = 200
MAX_TIME = 100000
with open("day10input.txt") as file:
    points = [parse(line) for line in file]

    time = 0
    while time < MAX_TIME:
        time += 1
        if time % 1000 == 0:
            print(time)
        for point in points:
            point.update()
        left = min(point.x for point in points)
        right = max(point.x for point in points)
        top = min(point.y for point in points)
        bottom = max(point.y for point in points)

        if right - left < MAX_SIZE and bottom - top < MAX_SIZE:
            sky = [[False for x in range(left, right+1)] for y in range(top, bottom+1)]
            for point in points:
                sky[point.y - top][point.x - left] = True
            print_sky(sky)
            input(time)

    print("hit maxtime")