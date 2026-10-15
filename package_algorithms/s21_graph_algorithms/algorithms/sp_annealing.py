"""Module for solving the traveling salesman problem by annealing imitation"""

# https://en.wikipedia.org/wiki/Simulated_annealing
# https://rutube.ru/video/b7ff83a69726bc1462acdca293b51697/
import random

from typing import List

from math import exp

from s21_graph.models.models import WeightedNextVertex, TsmResultPython
from s21_graph.s21_graph import Graph


class AnnealingSalesmanProblem:
    """Class for solving the traveling salesman problem by annealing imitation"""

    def __init__(self):
        self.__graph: Graph | None = None
        self.__temperature: float = 100
        self.__temp_decrease: float = 1
        self.__paths = {}
        self.__current_path: List[int] | None = None

    def solve_traveling_salesman_problem(
        self, graph: Graph, temp_start: float = 100, temp_decrease: float = 1
    ) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by annealing imitation"""

        self.__graph = graph
        self.__temperature = temp_start
        self.__temp_decrease = temp_decrease
        self.__current_path = None
        self.__paths = {}
        for obj in graph.get_all_edges():
            self.__paths[(obj.first_vertex, obj.second_vertex)] = obj.weight

        if not self.__init_path():
            return None

        fails = 0
        while self.__temperature > 5:
            if self.__next_iteration() or fails == 5:
                self.__temperature -= self.__temp_decrease
                fails = 0
            else:
                fails += 1

        return TsmResultPython(
            self.__current_path, self.__get_current_path_weight(self.__current_path)
        )

    def __next_iteration(self) -> bool:
        """Auxiliary function for solving the traveling salesman problem by annealing imitation"""

        current_path_weight = self.__get_current_path_weight(self.__current_path)
        new_path = [self.__current_path[i] for i in range(len(self.__current_path))]
        to_turn = random.sample(range(len(new_path) - 1), 2)
        temp = new_path[to_turn[0]]
        new_path[to_turn[0]] = new_path[to_turn[1]]
        new_path[to_turn[1]] = temp
        new_path[len(new_path) - 1] = new_path[0]

        new_path_weight = self.__get_current_path_weight(new_path)
        if new_path_weight is None:
            return False

        if new_path_weight < current_path_weight:
            self.__current_path = new_path
        else:
            p = exp(-((new_path_weight - current_path_weight) / self.__temperature))
            if p > random.random():
                self.__current_path = new_path
        return True

    def __get_current_path_weight(self, path: List[int]) -> int | None:
        """Auxiliary function for solving the traveling salesman problem by annealing imitation"""

        res = 0
        for i in range(1, len(path)):
            if (path[i - 1], path[i]) in self.__paths:
                res += self.__paths[(path[i - 1], path[i])]
            else:
                return None
        return res

    def __init_path(self) -> bool:
        """Auxiliary function for solving the traveling salesman problem by annealing imitation"""

        for i in range(1, self.__graph.get_vertices_count() + 1):
            visited: List[int] = [i]
            path: List[WeightedNextVertex] = []
            flag = True
            while flag:
                neighbors: List[WeightedNextVertex] | None = self.__graph.next_vertices(
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
            if len(visited) == self.__graph.get_vertices_count():
                neighbors: List[WeightedNextVertex] | None = self.__graph.next_vertices(
                    visited[-1]
                )
                if neighbors is not None:
                    for obj in neighbors:
                        if obj.second_vertex == visited[0]:
                            visited.append(visited[0])
                            self.__current_path = visited
                            return True
        return False
