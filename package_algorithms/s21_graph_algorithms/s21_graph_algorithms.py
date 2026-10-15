"""Module for class wrappers for various functions for working with graphs"""

import ctypes
from typing import List

from s21_graph.s21_graph import Graph
from s21_graph.models.models import TsmResultPython

from s21_graph_algorithms.algorithms.sp_annealing import AnnealingSalesmanProblem
from s21_graph_algorithms.algorithms.sp_ant_colony import AntColonySalesmanProblem
from s21_graph_algorithms.algorithms.breadth_first_search import BreadthFirstSearch
from s21_graph_algorithms.algorithms.depth_first_search import DepthFirstSearch
from s21_graph_algorithms.algorithms.dijkstra_search import (
    GetShortestPathBetweenVertices,
)
from s21_graph_algorithms.algorithms.floyd_warshall_search import (
    GetShortestPathsBetweenAllVertices,
)
from s21_graph_algorithms.algorithms.sp_brute_force import BruteForceSalesmanProblem
from s21_graph_algorithms.algorithms.sp_held_karp import HeldKarpSalesmanProblem
from s21_graph_algorithms.algorithms.sp_nearest_nieghbour import (
    NearestNeighbourSalesmanProblem,
)
from s21_graph_algorithms.algorithms.spanning_tree import GetLeastSpanningTree


class TsmResult(ctypes.Structure):
    """Auxiliary structure"""

    _fields_ = [
        ("vertices", ctypes.POINTER(ctypes.c_int)),
        ("distance", ctypes.c_double),
    ]


class GraphAlgorithms:
    """Class wrappers for various functions for working with graphs"""

    # https://en.wikipedia.org/wiki/Depth-first_search
    @staticmethod
    def depth_first_search(graph: Graph, start_vertex: int) -> List[int] | None:
        """Function for DFS"""

        if start_vertex < 1 or start_vertex > graph.get_vertices_count():
            return None
        return DepthFirstSearch.depth_first_search(graph, start_vertex)

    # https://en.wikipedia.org/wiki/Breadth-first_search
    @staticmethod
    def breadth_first_search(graph: Graph, start_vertex: int) -> List[int] | None:
        """Function for BFS"""

        if start_vertex < 1 or start_vertex > graph.get_vertices_count():
            return None
        return BreadthFirstSearch.breadth_first_search(graph, start_vertex)

    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    @staticmethod
    def get_shortest_path_between_vertices(
        graph: Graph, vertex1: int, vertex2: int
    ) -> int | None:
        """Function for Dijkstra algorithm"""

        res = GetShortestPathBetweenVertices.get_shortest_path_between_vertices(
            graph, vertex1, vertex2
        )
        return res.distance

    @staticmethod
    def get_shortest_path_between_vertices_with_path(
        graph: Graph, vertex1: int, vertex2: int
    ) -> TsmResultPython | None:
        """Function for Dijkstra algorithm. Returns path and cost"""

        return GetShortestPathBetweenVertices.get_shortest_path_between_vertices(
            graph, vertex1, vertex2
        )

    # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    @staticmethod
    def get_shortest_paths_between_all_vertices(graph: Graph) -> List[List[int]] | None:
        """Function for Floyd-Warshall algorithm"""

        return (
            GetShortestPathsBetweenAllVertices.get_shortest_paths_between_all_vertices(
                graph
            )
        )

    # https://en.wikipedia.org/wiki/Prim%27s_algorithm
    @staticmethod
    def get_least_spanning_tree(graph: Graph) -> List[List[int]] | None:
        """Function for Prim algorithm"""

        return GetLeastSpanningTree.get_least_spanning_tree(graph)

    # https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms
    # https://rutube.ru/video/e434d91fbd072d264c9be6172edc1ede/
    @staticmethod
    def solve_sp_ant_colony(graph: Graph, starts: int = 1) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by ant colony method"""

        res: TsmResultPython | None = None
        for _ in range(starts):
            temp = AntColonySalesmanProblem()
            temp_res = temp.solve_traveling_salesman_problem(graph)
            if temp_res is not None:
                if res is None:
                    res = temp_res
                else:
                    if temp_res.distance < res.distance:
                        res = temp_res

        return res

    @staticmethod
    def solve_traveling_salesman_problem(graph: Graph) -> TsmResult | None:
        """Function for solving the traveling salesman problem by ant colony method"""

        res: TsmResultPython | None = GraphAlgorithms.solve_sp_ant_colony(graph)
        if res is not None:
            arr = (ctypes.c_int * len(res.vertices))(*res.vertices)
            return TsmResult(arr, res.distance)

        return None

    @staticmethod
    def solve_sp_brute_force(graph: Graph) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by brute force method"""

        temp = BruteForceSalesmanProblem()
        return temp.solve_traveling_salesman_problem(graph)

    @staticmethod
    def solve_sp_held_karp(graph: Graph) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by Held-Karp method"""

        temp = HeldKarpSalesmanProblem()
        return temp.solve_traveling_salesman_problem(graph)

    @staticmethod
    def solve_sp_nearest_neighbour(graph: Graph) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by nearest neighbour method"""

        temp = NearestNeighbourSalesmanProblem()
        return temp.solve_traveling_salesman_problem(graph)

    @staticmethod
    def solve_sp_annealing(graph: Graph, starts: int = 1) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by annealing imitation"""

        res: TsmResultPython | None = None
        for _ in range(starts):
            temp = AnnealingSalesmanProblem()
            temp_res = temp.solve_traveling_salesman_problem(graph)
            if temp_res is not None:
                if res is None:
                    res = temp_res
                else:
                    if temp_res.distance < res.distance:
                        res = temp_res

        return res
