"""Module for solving the traveling salesman problem by nearest neighbour method"""

# https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm

from typing import List

from s21_graph.models.models import WeightedNextVertex, TsmResultPython
from s21_graph.s21_graph import Graph


class NearestNeighbourSalesmanProblem:
    """Class for solving the traveling salesman problem by nearest neighbour method"""

    @staticmethod
    def solve_traveling_salesman_problem(graph: Graph) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by nearest neighbour method"""

        best_path_weight: int = 0
        best_path: List[WeightedNextVertex] | None = None
        for i in range(1, graph.get_vertices_count() + 1):
            visited: List[int] = [i]
            path: List[WeightedNextVertex] = []
            flag = True
            while flag:
                neighbors: List[WeightedNextVertex] | None = graph.next_vertices(
                    visited[-1]
                )
                can_move: List[WeightedNextVertex] = []
                if neighbors is not None:
                    for next_step in neighbors:
                        if next_step.second_vertex not in visited:
                            can_move.append(next_step)
                if len(can_move) == 0:
                    flag = False
                else:
                    minimum = can_move[0]
                    for obj in can_move:
                        if obj.weight < minimum.weight:
                            minimum = obj
                    path.append(minimum)
                    visited.append(minimum.second_vertex)
            if len(visited) == graph.get_vertices_count():
                neighbors: List[WeightedNextVertex] | None = graph.next_vertices(
                    visited[-1]
                )
                if neighbors is not None:
                    for obj in neighbors:
                        if obj.second_vertex == visited[0]:
                            path.append(obj)
                            path_weight = 0
                            for vertex in path:
                                path_weight += vertex.weight
                            if best_path is None or best_path_weight > path_weight:
                                best_path_weight = path_weight
                                best_path = path.copy()

        if best_path is not None:
            res_list: List[int] = [best_path[0].first_vertex]
            for obj in best_path:
                res_list.append(obj.second_vertex)
            return TsmResultPython(res_list, best_path_weight)

        return None
