def parse(line):
    return line.split()

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

root = dict()

current = root
path = []

def follow_path(path):
    here = root
    for node in path:
        here = here[node]
    return here

for line in lines:
    if line[0] == '$':
        if line[1] == 'ls':
            continue
        elif line[1] == 'cd':
            if line[2] == '/':
                current = root
                path = []
            elif line[2] == '..':
                path = path[:-1]
                current = follow_path(path)
            else:
                current = current[line[2]]
                path.append(line[2])
            continue
        else:
            print("unknown command", line)
            exit(1)
    else:
        # must be in an ls
        if line[0] == 'dir':
            if line[1] not in current:
                current[line[1]] = dict()
        else:
            current[line[1]] = int(line[0])

print(root)

#part 1
results = dict()
def calc_sizes(path, node):
    size = 0
    for subname, obj in node.items():
        if type(obj) == dict:
            calc_sizes((*path, subname), obj)
            size += results[(*path,subname)]
        else:
            size += obj
    results[path] = size

calc_sizes(('/',), root)

print([name for name, size in results.items() if size <= 100000])

print(sum(size for size in results.values() if size <= 100000))

# part 2
MAX_SIZE = 70000000
NEEDED = 30000000
max_used = MAX_SIZE - NEEDED
need_to_delete = results['/',] - max_used
print(need_to_delete)

sorted_sizes = sorted(list(results.items()), key=lambda p: p[1])
for path, size in sorted_sizes:
    if size > need_to_delete:
        print(size)
        break
