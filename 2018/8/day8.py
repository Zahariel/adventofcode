
class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata
        if len(children) == 0:
            self.value = sum(metadata)
        else:
            self.value = sum(children[node-1].value for node in metadata if node <= len(children))

    def sumMetadata(self):
        return sum(child.sumMetadata() for child in self.children) + sum(self.metadata)

def parseNode(tokens):
    numChildren = int(tokens.pop())
    numMetadata = int(tokens.pop())
    # this is sleazy because it's a comprehension with side effects, but oh well,
    # comprehensions are guaranteed to run in order
    children = [parseNode(tokens) for _ in range(numChildren)]
    metadata = [int(tokens.pop()) for _ in range(numMetadata)]
    return Node(children, metadata)

with open("day8input.txt") as file:
    tokens = file.readline().strip().split(" ")
    # tokens.pop() works on the end of the list
    tokens.reverse()
    root = parseNode(tokens)

    print(root.sumMetadata())

    print(root.value)
