"""DFS module"""

from typing import List
from s21_graph.s21_graph import Graph
from s21_graph.models.models import WeightedNextVertex
from s21_graph_algorithms.algorithms.s21_queue_stack.s21_queue_stack_interface import (
    Stack,
)

# https://en.wikipedia.org/wiki/Depth-first_search


class DepthFirstSearch:
    """DFS class"""

    @staticmethod
    def depth_first_search(graph: Graph, start_vertex: int) -> List[int]:
        """DFS funtion"""

        vertex_stack = Stack()
        vertex_stack.push(start_vertex)
        res: List[int] = []

        while vertex_stack:
            current = vertex_stack.pop()
            if current not in res:
                res.append(current)

                neighbors: List[WeightedNextVertex] | None = graph.next_vertices(
                    current
                )

                if neighbors is not None:
                    for neighbor in neighbors:
                        if neighbor.second_vertex not in res:
                            vertex_stack.push(neighbor.second_vertex)
        return res
