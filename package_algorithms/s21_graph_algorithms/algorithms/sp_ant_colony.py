"""Module for solving the traveling salesman problem by ant colony method"""

import random
from dataclasses import dataclass
from typing import List
from s21_graph.models.models import WeightedNextVertex
from s21_graph.models.models import TsmResultPython
from s21_graph.s21_graph import Graph


@dataclass
class Ant:
    """Auxiliary class for solving the traveling salesman problem by ant colony method"""

    visited: List[int]
    edges: List[WeightedNextVertex]


class AntColonySalesmanProblem:
    """Class for solving the traveling salesman problem by ant colony method"""

    def __init__(self):
        self.__graph: Graph | None = None
        self.__graph_size: int = 0
        self.__alpha: float = 1
        self.__beta: float = 1
        self.__q: float = 1
        self.__p: float = 0.3
        self.__paths = {}
        self.__ants_on_vertex = 1
        self.__ants: List[Ant] = []
        self.__best_path_weight: int = 0
        self.__best_path: List[WeightedNextVertex] | None = None
        self.__best_path_record: int = 0

    def solve_traveling_salesman_problem(
        self,
        graph: Graph,
        alpha: float = 1,
        beta: float = 3,
        q: float = 1,
        p: float = 0.5,
        ants_on_vertex: int = 1,
        starts: int = 10,
    ) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by ant colony method"""

        self.__graph = graph
        self.__graph_size = graph.get_vertices_count()
        self.__alpha = alpha
        self.__beta = beta
        self.__q = q
        self.__p = p
        self.__ants_on_vertex = ants_on_vertex
        self.__ants: List[Ant] = []
        self.__best_path_weight = 0
        self.__best_path = None
        self.__best_path_record = 0
        self.__paths = {}
        for obj in graph.get_all_edges():
            self.__paths[(obj.first_vertex, obj.second_vertex, obj.weight)] = 1

        while self.__best_path_record < starts:
            flag = False
            for _ in range(self.__graph_size * 2):
                self.__new_generation()
                self.__next_iteration()
                if self.__is_there_path():
                    self.__update_pheromones()
                    self.__update_best_path()
                    flag = True
                    break
            if not flag and self.__best_path is None:
                return None

        if self.__best_path is not None and len(self.__best_path) > 0:
            res_list = [self.__best_path[0].first_vertex]
            for obj in self.__best_path:
                res_list.append(obj.second_vertex)
            return TsmResultPython(res_list, self.__best_path_weight)

        return None

    def __new_generation(self):
        """Auxiliary function for solving the traveling salesman problem by ant colony method"""

        if self.__graph is not None:
            self.__ants = []
            # self.__ants = [Ant([i + 1], []) for i in range(self.__graph_size)]
            for i in range(self.__graph_size):
                for _ in range(self.__ants_on_vertex):
                    self.__ants.append(Ant([i + 1], []))

    def __next_iteration(self) -> bool:
        """Auxiliary function for solving the traveling salesman problem by ant colony method"""

        for ant in self.__ants:
            for _ in range(self.__graph_size - 1):
                neighbors: List[WeightedNextVertex] | None = self.__graph.next_vertices(
                    ant.visited[-1]
                )
                can_move: List[WeightedNextVertex] = []
                for next_step in neighbors:
                    if next_step.second_vertex not in ant.visited:
                        can_move.append(next_step)
                if len(can_move) == 0:
                    ant.edges = []
                    break

                denom: float = 0.0
                for obj in can_move:
                    denom += (
                        self.__paths[(obj.first_vertex, obj.second_vertex, obj.weight)]
                        ** self.__alpha
                    ) * ((1 / obj.weight) ** self.__beta)
                chances = [
                    (
                        (
                            self.__paths[
                                (obj.first_vertex, obj.second_vertex, obj.weight)
                            ]
                            ** self.__alpha
                        )
                        * ((1 / obj.weight) ** self.__beta)
                    )
                    / denom
                    for obj in can_move
                ]
                chosen = random.choices(can_move, weights=chances, k=1)[0]
                ant.edges.append(chosen)
                ant.visited.append(chosen.second_vertex)

            if len(ant.edges) > 0:
                neighbors: List[WeightedNextVertex] | None = self.__graph.next_vertices(
                    ant.visited[-1]
                )
                finish: WeightedNextVertex | None = None
                for next_step in neighbors:
                    if next_step.second_vertex == ant.visited[0]:
                        finish = next_step

                if finish is None:
                    ant.edges = []
                else:
                    ant.edges.append(finish)
                    ant.visited.append(finish.second_vertex)
        return True

    def __update_best_path(self):
        """Auxiliary function for solving the traveling salesman problem by ant colony method"""

        if self.__is_there_path():
            current_best_path_weight = self.__best_path_weight
            for ant in self.__ants:
                if len(ant.edges) > 0:
                    path_weight = 0
                    for obj in ant.edges:
                        path_weight += obj.weight
                    if (
                        self.__best_path is None
                        or self.__best_path_weight > path_weight
                    ):
                        self.__best_path = ant.edges
                        self.__best_path_weight = path_weight
                        self.__best_path_record = 0
            if self.__best_path_weight == current_best_path_weight:
                self.__best_path_record += 1

    def __update_pheromones(self):
        """Auxiliary function for solving the traveling salesman problem by ant colony method"""

        if self.__is_there_path():
            for edge in self.__paths:
                self.__paths[edge] = self.__paths[edge] * (1 - self.__p)
            for ant in self.__ants:
                if len(ant.edges) > 0:
                    path_weight = 0
                    for obj in ant.edges:
                        path_weight += obj.weight
                    if path_weight > 0:
                        delta_t = self.__q / path_weight
                    else:
                        delta_t = 0
                    for obj in ant.edges:
                        self.__paths[
                            (obj.first_vertex, obj.second_vertex, obj.weight)
                        ] += delta_t
                        if not self.__graph.is_graph_directed():
                            self.__paths[
                                (obj.second_vertex, obj.first_vertex, obj.weight)
                            ] += delta_t

    def __is_there_path(self) -> bool:
        """Auxiliary function for solving the traveling salesman problem by ant colony method"""

        for ant in self.__ants:
            if len(ant.edges) > 0:
                return True
        return False
