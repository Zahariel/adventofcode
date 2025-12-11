import heapq
import itertools
from collections import defaultdict
from typing import Mapping, Optional, Tuple, MutableMapping, TypeVar, Iterable, Callable, NamedTuple

NODE = TypeVar("NODE")
RESULT = TypeVar("RESULT")

def _get_all_nodes(source:Mapping[NODE, Iterable[NODE]]):
    return {*source.keys(), *itertools.chain(*source.values())}

def _invert_map(source:Mapping[NODE, Iterable[NODE]], target: MutableMapping[NODE, set[NODE]]):
    for left, rights in source.items():
        for r in rights:
            target[r].add(left)

class Dag[NODE]:

    def __init__(self, nodes: Iterable[NODE]):
        self.nodes = set(nodes)
        self.children:defaultdict[NODE, set[NODE]] = defaultdict(set)
        self.parents:defaultdict[NODE, set[NODE]] = defaultdict(set)

    def topological_sort(self, tiebreaker_fn:Callable[[NODE, NODE], bool] = lambda _, __: False) -> Iterable[NODE]:
        class Node(NamedTuple):
            val: NODE
            def __lt__(self, other):
                return tiebreaker_fn(self.val, other.val)

        to_process = [Node(node) for node in self.nodes]
        heapq.heapify(to_process)
        processed:set[NODE] = set()
        while to_process:
            node = heapq.heappop(to_process).val
            if node in processed: continue
            parents = self.parents[node]
            if parents <= processed:
                processed.add(node)
                yield node
                for child in self.children[node]:
                    heapq.heappush(to_process, Node(child))

    def propagate_values(self, initial:Mapping[NODE, RESULT], combiner:Callable[[Iterable[RESULT]], RESULT]) -> Mapping[NODE, RESULT]:
        return self.propagate_named_values(initial, lambda _, vs: combiner(vs))

    def propagate_named_values(
        self,
        initial: Mapping[NODE, RESULT],
        combiner: Callable[[NODE, Iterable[RESULT]], RESULT],
    ) -> Mapping[NODE, RESULT]:
        """
        Propagates an initial set of seed values through the DAG with the given combiner function.

        :param initial: Initial seed values
        :param combiner: Combiner function that takes the node name and values from all parents. Note: this needs
        to return a sensible default if there are no parents, so the input values are empty
        :return: Map of all node names to computed values
        """
        result = dict(initial)
        to_process = set(self.nodes)
        while to_process:
            node = to_process.pop()
            # i think this is only possible if node was in the initial seed
            if node in result: continue
            parents = self.parents[node]
            if parents <= result.keys():
                result[node] = combiner(node, [result[p] for p in parents])
                to_process.update(self.children[node])
        return result


    @staticmethod
    def from_parents(parents: Mapping[NODE, Iterable[NODE]], all_nodes:Optional[Iterable[NODE]] = None):
        if all_nodes is None:
            all_nodes = _get_all_nodes(parents)
        result = Dag(all_nodes)
        for c, ps in parents.items():
            result.parents[c].update(ps)
        _invert_map(parents, result.children)
        return result

    @staticmethod
    def from_children(children: Mapping[NODE, Iterable[NODE]], all_nodes:Optional[Iterable[NODE]] = None):
        if all_nodes is None:
            all_nodes = _get_all_nodes(children)
        result = Dag(all_nodes)
        for p, cs in children.items():
            result.children[p].update(cs)
        _invert_map(children, result.parents)
        return result

    @staticmethod
    def from_child_edges(edges: Iterable[Tuple[NODE, NODE]], all_nodes:Optional[Iterable[NODE]] = None):
        edges = set(edges)
        if all_nodes is None:
            all_nodes = {*itertools.chain(*edges)}
        result = Dag(all_nodes)
        for l, r in edges:
            result.children[l].add(r)
            result.parents[r].add(l)
        return result




