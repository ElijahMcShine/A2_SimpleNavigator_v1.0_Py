"""BFS module"""

from typing import List

from s21_graph.models.models import WeightedNextVertex
from s21_graph.s21_graph import Graph
from s21_graph_algorithms.algorithms.s21_queue_stack.s21_queue_stack_interface import (
    Queue,
)

# https://en.wikipedia.org/wiki/Breadth-first_search


class BreadthFirstSearch:
    """BFS class"""

    @staticmethod
    def breadth_first_search(graph: Graph, start_vertex: int) -> List[int]:
        """BFS function"""

        vertex_queue = Queue()
        vertex_queue.push(start_vertex)
        res: List[int] = []

        while vertex_queue:
            current = vertex_queue.pop()
            if current not in res:
                res.append(current)

                neighbors: List[WeightedNextVertex] | None = graph.next_vertices(
                    current
                )

                if neighbors is not None:
                    for neighbor in neighbors:
                        if neighbor.second_vertex not in res:
                            vertex_queue.push(neighbor.second_vertex)
        return res
