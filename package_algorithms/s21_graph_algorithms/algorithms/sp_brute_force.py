"""Module for solving the traveling salesman problem by brute force method"""

# https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm

from typing import List
from s21_graph.models.models import WeightedNextVertex
from s21_graph.models.models import TsmResultPython
from s21_graph.s21_graph import Graph


class BruteForceSalesmanProblem:
    """Class for solving the traveling salesman problem by brute force method"""

    def __init__(self):
        self.__graph: Graph | None = None
        self.__graph_size: int = 0
        self.__best_path_weight: int = 0
        self.__best_path: List[WeightedNextVertex] | None = None

    def solve_traveling_salesman_problem(self, graph: Graph) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by brute force method"""
        self.__graph = graph
        self.__graph_size = graph.get_vertices_count()
        self.__best_path_weight = 0
        self.__best_path = None
        visited: List[int] = [1]
        self.__next_step(visited, [])
        if self.__best_path is not None:
            res_list: List[int] = [1]
            for obj in self.__best_path:
                res_list.append(obj.second_vertex)
            return TsmResultPython(res_list, self.__best_path_weight)

        return None

    def __next_step(self, visited: List[int], path: List[WeightedNextVertex]):
        """Auxiliary function for solving the traveling salesman problem by brute force method"""

        if len(visited) == self.__graph_size:
            neighbors: List[WeightedNextVertex] | None = self.__graph.next_vertices(
                visited[-1]
            )
            finish: WeightedNextVertex | None = None
            if neighbors is not None:
                for next_step in neighbors:
                    if next_step.second_vertex == visited[0]:
                        finish = next_step

            if finish is None:
                return

            path.append(finish)
            path_weight = 0
            for obj in path:
                path_weight += obj.weight
            if self.__best_path is None or self.__best_path_weight > path_weight:
                self.__best_path_weight = path_weight
                self.__best_path = path.copy()
                return

        neighbors: List[WeightedNextVertex] | None = self.__graph.next_vertices(
            visited[-1]
        )
        can_move: List[WeightedNextVertex] = []
        if neighbors is not None:
            for next_step in neighbors:
                if next_step.second_vertex not in visited:
                    can_move.append(next_step)
        if len(can_move) == 0:
            return

        path_weight = 0
        for obj in path:
            path_weight += obj.weight
        for next_step in can_move:
            if self.__best_path is not None:
                if self.__best_path_weight < path_weight + next_step.weight:
                    return
            visited_copy = visited.copy()
            visited_copy.append(next_step.second_vertex)
            path_copy = path.copy()
            path_copy.append(next_step)
            self.__next_step(visited_copy, path_copy)
