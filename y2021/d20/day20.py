from collections import defaultdict

def parse(line):
    return line.strip()

with open("input.txt") as f:
    transformation = [c == '#' for c in f.readline().strip()]
    print(transformation)
    print(len(transformation))
    assert len(transformation) == 512
    f.readline()
    data = [parse(line) for line in f.readlines()]

pixels = defaultdict(bool)

for y, line in enumerate(data):
    for x, c in enumerate(line):
        if c == '#':
            pixels[x,y] = True

def get_bounds(image):
    xmin = min(x for x,_ in image)
    xmax = max(x for x,_ in image)
    ymin = min(y for _,y in image)
    ymax = max(y for _,y in image)
    return xmin-1, xmax+2, ymin-1, ymax+2

def get_neighborhood(image, x, y):
    val = 0
    for dy in range(y-1,y+2):
        for dx in range(x-1, x+2):
            val *= 2
            if image[dx,dy]:
                val += 1
    return val

def enhance(image:defaultdict):
    xmin, xmax, ymin, ymax = get_bounds(image)
    old_default = image.default_factory()
    if old_default:
        new_default = transformation[511]
    else:
        new_default = transformation[0]
    new_image = defaultdict(lambda:new_default)

    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            new_pixel = transformation[get_neighborhood(image, x, y)]
            if new_pixel != new_default:
                new_image[x,y] = new_pixel

    return new_image

def print_image(image):
    xmin, xmax, ymin, ymax = get_bounds(image)
    for y in range(ymin, ymax):
        print("".join("#" if image[x,y] else "." for x in range(xmin, xmax)))
    print()

print_image(pixels)

pixels1 = enhance(pixels)
print_image(pixels1)
pixels2 = enhance(pixels1)
print_image(pixels2)
print(len([1 for p in pixels2.values() if p]))

# part 2

image = pixels2
for i in range(2, 50):
    image = enhance(image)

print(len([1 for p in image.values() if p]))
