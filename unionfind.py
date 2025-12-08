from mypy.checkexpr import defaultdict


class UnionFind:
    def __init__(self, elements):
        self.parents = {e: e for e in elements}
        self.ranks = {e: 1 for e in elements}
        self.size = len(elements)

    def find(self, x):
        while self.parents[x] != x:
            x, self.parents[x] = self.parents[x], self.parents[self.parents[x]]
        return x

    def union(self, x1, x2):
        x1 = self.find(x1)
        x2 = self.find(x2)
        if x1 == x2: return
        if self.ranks[x1] < self.ranks[x2]: x1, x2 = x2, x1
        self.parents[x2] = x1
        if self.ranks[x1] == self.ranks[x2]: self.ranks[x1] += 1
        self.size -= 1

    def to_sets(self):
        results = defaultdict(set)
        for e in self.parents:
            results[self.find(e)].add(e)

        return results.values()

