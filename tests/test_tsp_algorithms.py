"""
Unit tests for Traveling Salesman Problem algorithms:
- sp_brute_force
- sp_held_karp
- sp_nearest_nieghbour
- sp_ant_colony
- sp_annealing
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from s21_graph_algorithms.algorithms.sp_brute_force import BruteForceSalesmanProblem
from s21_graph_algorithms.algorithms.sp_held_karp import HeldKarpSalesmanProblem
from s21_graph_algorithms.algorithms.sp_nearest_nieghbour import (
    NearestNeighbourSalesmanProblem,
)
from s21_graph_algorithms.algorithms.sp_ant_colony import AntColonySalesmanProblem
from s21_graph_algorithms.algorithms.sp_annealing import AnnealingSalesmanProblem


class TestBruteForceTSP:
    def test_brute_force_complete_4(self, complete_graph_4):
        solver = BruteForceSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(complete_graph_4)
        assert result is not None
        assert len(result.vertices) == 5  # 4 vertices + return to start
        assert result.vertices[0] == 1
        assert result.vertices[-1] == 1  # returns to start
        # Optimal path: 1-2(10)-4(25)-3(30)-1(15) = 80
        # Or: 1-3(15)-4(30)-2(25)-1(10) = 80
        # Or: 1-2(10)-3(35)-4(30)-1(20) = 95
        # The optimal is 80
        assert result.distance == 80

    def test_brute_force_small_graph(self, simple_undirected_graph):
        """3-vertex complete graph: 1-2(2)-3(4)-1(3) = 9, or 1-3(3)-2(4)-1(2) = 9"""
        solver = BruteForceSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(simple_undirected_graph)
        assert result is not None
        assert result.distance == 9

    def test_brute_force_single_vertex(self, single_vertex_graph):
        """Single vertex - no TSP possible"""
        solver = BruteForceSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(single_vertex_graph)
        assert result is None


class TestHeldKarpTSP:
    def test_held_karp_complete_4(self, complete_graph_4):
        solver = HeldKarpSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(complete_graph_4)
        assert result is not None
        assert len(result.vertices) == 5  # 4 vertices + return to start
        assert result.vertices[0] == 1
        assert result.vertices[-1] == 1
        assert result.distance == 80

    def test_held_karp_small_graph(self, simple_undirected_graph):
        solver = HeldKarpSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(simple_undirected_graph)
        assert result is not None
        assert result.distance == 9

    def test_held_karp_single_vertex(self, single_vertex_graph):
        solver = HeldKarpSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(single_vertex_graph)
        assert result is None or result.distance == 0


class TestNearestNeighbourTSP:
    def test_nearest_neighbour_complete_4(self, complete_graph_4):
        solver = NearestNeighbourSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(complete_graph_4)
        assert result is not None
        assert len(result.vertices) >= 2
        assert result.vertices[0] in [1, 2, 3, 4]
        assert result.vertices[-1] == result.vertices[0]  # returns to start

    def test_nearest_neighbour_small_graph(self, simple_undirected_graph):
        solver = NearestNeighbourSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(simple_undirected_graph)
        assert result is not None
        assert result.distance == 9

    def test_nearest_neighbour_single_vertex(self, single_vertex_graph):
        solver = NearestNeighbourSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(single_vertex_graph)
        assert result is None


class TestAntColonyTSP:
    def test_ant_colony_complete_4(self, complete_graph_4):
        solver = AntColonySalesmanProblem()
        result = solver.solve_traveling_salesman_problem(
            complete_graph_4, alpha=1, beta=3, q=1, p=0.5, ants_on_vertex=2, starts=20
        )
        assert result is not None
        assert len(result.vertices) >= 2
        assert result.vertices[0] in [1, 2, 3, 4]
        assert result.vertices[-1] == result.vertices[0]

    def test_ant_colony_small_graph(self, simple_undirected_graph):
        solver = AntColonySalesmanProblem()
        result = solver.solve_traveling_salesman_problem(
            simple_undirected_graph,
            alpha=1,
            beta=3,
            q=1,
            p=0.5,
            ants_on_vertex=2,
            starts=10,
        )
        assert result is not None
        assert result.distance == 9

    def test_ant_colony_single_vertex(self, single_vertex_graph):
        solver = AntColonySalesmanProblem()
        result = solver.solve_traveling_salesman_problem(single_vertex_graph, starts=1)
        assert result is None

    def test_ant_colony_uncomplete_graph_4(self, uncomplete_graph_4):
        solver = AntColonySalesmanProblem()
        result = solver.solve_traveling_salesman_problem(uncomplete_graph_4, starts=10)
        assert result is not None


class TestAnnealingTSP:
    def test_annealing_complete_4(self, complete_graph_4):
        solver = AnnealingSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(
            complete_graph_4, temp_start=100, temp_decrease=1
        )
        assert result is not None
        assert len(result.vertices) >= 2
        assert result.vertices[0] in [1, 2, 3, 4]
        assert result.vertices[-1] == result.vertices[0]

    def test_annealing_small_graph(self, simple_undirected_graph):
        solver = AnnealingSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(
            simple_undirected_graph, temp_start=100, temp_decrease=1
        )
        assert result is not None
        assert result.distance == 9

    def test_annealing_single_vertex(self, single_vertex_graph):
        solver = AnnealingSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(
            single_vertex_graph, temp_start=100, temp_decrease=1
        )
        assert result is None

    def test_annealing_uncomplete_graph_4(self, uncomplete_graph_4):
        solver = AnnealingSalesmanProblem()
        result = solver.solve_traveling_salesman_problem(
            uncomplete_graph_4, temp_start=1000, temp_decrease=1
        )
        assert result is not None


class TestTSPConsistency:
    """Test that exact algorithms produce the same result"""

    def test_brute_force_vs_held_karp(self, complete_graph_4):
        bf = BruteForceSalesmanProblem()
        hk = HeldKarpSalesmanProblem()

        bf_result = bf.solve_traveling_salesman_problem(complete_graph_4)
        hk_result = hk.solve_traveling_salesman_problem(complete_graph_4)

        assert bf_result is not None
        assert hk_result is not None
        assert bf_result.distance == hk_result.distance == 80
