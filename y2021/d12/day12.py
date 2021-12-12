import keyeddefaultdict

class Cave:
    def __init__(self, name:str):
        self.name = name
        self.neighbors = set()

    def is_big(self):
        return self.name.isupper()

    def is_start(self):
        return self.name == "start"

def parse(line):
    [left, right] = line.strip().split("-")
    return left, right

with open("input.txt") as f:
    lines = f.readlines()
    edges = [parse(line) for line in lines]
    caves = keyeddefaultdict.KeyedDefaultdict(Cave)
    for left, right in edges:
        caves[left].neighbors.add(right)
        caves[right].neighbors.add(left)

# want to do DFS here because of revisiting nodes
def find_paths(start, end, visited):
    if start == end: return 1
    neighbors = [nbr for nbr in caves[start].neighbors if nbr not in visited]
    next_visited = set(visited)
    if not caves[start].is_big():
        next_visited.add(start)
    return sum(find_paths(nbr, end, next_visited) for nbr in neighbors)

paths = find_paths("start", "end", set())
print(paths)

# part 2

def find_paths2(start, end, visited, done_revisit, path):
    if start == end:
        # print(path)
        return 1
    neighbors = [nbr for nbr in caves[start].neighbors if nbr not in visited]
    next_visited = set(visited)
    if not caves[start].is_big():
        next_visited.add(start)
    paths1 = sum(find_paths2(nbr, end, next_visited, done_revisit, path + [start]) for nbr in neighbors)
    if done_revisit:
        return paths1
    else:
        visited_neighbors = [nbr for nbr in caves[start].neighbors if nbr in visited and not caves[nbr].is_start()]
        return paths1 + sum(find_paths2(nbr, end, next_visited, True, path + [start]) for nbr in visited_neighbors)

paths2 = find_paths2("start", "end", set(), False, [])
print(paths2)
