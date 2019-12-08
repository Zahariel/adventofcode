with open("input.txt") as f:
    pixels = [[[f.read(1) for x in range(25)] for y in range(6)] for layer in range(100)]

zero_count, target_layer = min((sum(1 for row in layer for cell in row if cell == "0"), layer_num) for layer_num, layer in enumerate(pixels))

ones = sum(1 for row in pixels[target_layer] for cell in row if cell == "1")
twos = sum(1 for row in pixels[target_layer] for cell in row if cell == "2")

print(ones * twos)

print("###########################")
for y in range(6):
    print("#", end="")
    for x in range(25):
        final_pixel = "0"
        for layer in range(100):
            if pixels[layer][y][x] != "2":
                final_pixel = pixels[layer][y][x]
                break
        if final_pixel == "0":
            print("#", end="")
        else:
            print(" ", end="")
    print("#")

print("###########################")
