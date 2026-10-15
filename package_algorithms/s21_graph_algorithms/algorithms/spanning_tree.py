"""Module for search shortest spanning tree 
    in graph with Prim algorithm"""

from typing import List

from s21_graph.s21_graph import Graph
from s21_graph.models.models import WeightedNextVertex

# https://en.wikipedia.org/wiki/Prim%27s_algorithm


class GetLeastSpanningTree:
    """Class for search shortest spanning tree
    in graph with Prim algorithm"""

    @staticmethod
    def get_least_spanning_tree(graph: Graph) -> List[List[int]] | None:
        """Function for search shortest spanning tree
        in graph with Prim algorithm"""

        if not graph.is_graph_directed():
            visited = set()
            spanning_tree = {}

            can_move: List[WeightedNextVertex] | None = graph.next_vertices(1)
            if can_move is None:
                can_move = []
            first_step = True

            while len(can_move) > 0:
                minimum = sorted(can_move, key=lambda x: x.weight)[0]
                visited.add(minimum.second_vertex)
                if first_step:
                    visited.add(minimum.first_vertex)
                    first_step = False
                spanning_tree[(minimum.first_vertex, minimum.second_vertex)] = (
                    minimum.weight
                )

                can_move = []
                for i in visited:
                    neighbors: List[WeightedNextVertex] | None = graph.next_vertices(i)
                    for next_step in neighbors:
                        if next_step.second_vertex not in visited:
                            can_move.append(next_step)

            res = [
                [0 for _ in range(graph.get_vertices_count())]
                for _ in range(graph.get_vertices_count())
            ]
            for obj, value in spanning_tree.items():
                res[obj[0] - 1][obj[1] - 1] = value
                res[obj[1] - 1][obj[0] - 1] = value

            return res
        return None
