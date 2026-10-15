"""
Unit tests for s21_graph_algorithms/s21_graph_algorithms.py
Tests the public API layer (GraphAlgorithms class).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from s21_graph_algorithms.s21_graph_algorithms import GraphAlgorithms


class TestGraphAlgorithmsAPI:
    def test_depth_first_search(self, simple_undirected_graph):
        result = GraphAlgorithms.depth_first_search(simple_undirected_graph, 1)
        assert result is not None
        assert len(result) == 3
        assert result[0] == 1

    def test_depth_first_search_invalid_start(self, simple_undirected_graph):
        result = GraphAlgorithms.depth_first_search(simple_undirected_graph, 0)
        assert result is None

    def test_depth_first_search_out_of_bounds(self, simple_undirected_graph):
        result = GraphAlgorithms.depth_first_search(simple_undirected_graph, 999)
        assert result is None

    def test_breadth_first_search(self, simple_undirected_graph):
        result = GraphAlgorithms.breadth_first_search(simple_undirected_graph, 1)
        assert result is not None
        assert len(result) == 3
        assert result[0] == 1

    def test_breadth_first_search_invalid_start(self, simple_undirected_graph):
        result = GraphAlgorithms.breadth_first_search(simple_undirected_graph, 0)
        assert result is None

    def test_get_shortest_path_between_vertices(self, simple_undirected_graph):
        result = GraphAlgorithms.get_shortest_path_between_vertices(
            simple_undirected_graph, 1, 2
        )
        assert result is not None
        assert result == 2

    def test_get_shortest_paths_between_all_vertices(self, simple_undirected_graph):
        result = GraphAlgorithms.get_shortest_paths_between_all_vertices(
            simple_undirected_graph
        )
        assert result is not None
        assert len(result) == 3

    def test_get_least_spanning_tree(self, simple_undirected_graph):
        result = GraphAlgorithms.get_least_spanning_tree(simple_undirected_graph)
        assert result is not None
        assert len(result) == 3

    def test_solve_traveling_salesman_problem(self, complete_graph_4):
        result = GraphAlgorithms.solve_traveling_salesman_problem(complete_graph_4)
        assert result is not None
        # TsmResult with ctypes fields
        assert hasattr(result, "vertices")
        assert hasattr(result, "distance")


class TestGraphAlgorithmsTSPMethods:
    def test_solve_sp_brute_force(self, simple_undirected_graph):
        result = GraphAlgorithms.solve_sp_brute_force(simple_undirected_graph)
        assert result is not None
        assert result.distance == 9

    def test_solve_sp_held_karp(self, simple_undirected_graph):
        result = GraphAlgorithms.solve_sp_held_karp(simple_undirected_graph)
        assert result is not None
        assert result.distance == 9

    def test_solve_sp_nearest_neighbour(self, simple_undirected_graph):
        result = GraphAlgorithms.solve_sp_nearest_neighbour(simple_undirected_graph)
        assert result is not None
        assert result.distance == 9

    def test_solve_sp_nearest_neighbour(self, full_graph_12):
        result = GraphAlgorithms.solve_sp_nearest_neighbour(full_graph_12)
        assert result is not None
        assert result.distance == 298

    def test_solve_sp_ant_colony(self, dir_graph_11):
        result = GraphAlgorithms.solve_sp_ant_colony(dir_graph_11, starts=100)
        assert result is not None
        assert result.distance == 378

    def test_solve_sp_annealing(self, full_graph_12):
        result = GraphAlgorithms.solve_sp_annealing(full_graph_12, starts=100)
        assert result is not None

    def test_solve_sp_annealing(self, simple_undirected_graph):
        result = GraphAlgorithms.solve_sp_annealing(simple_undirected_graph, starts=1)
        assert result is not None
        assert result.distance == 9

    def test_solve_sp_ant_colony_multiple_starts(self, complete_graph_4):
        """Test that running multiple times yields a valid result"""
        result = GraphAlgorithms.solve_sp_ant_colony(complete_graph_4, starts=10)
        assert result is not None


class TestGraphAlgorithmsEdgeCases:
    def test_bfs_single_vertex(self, single_vertex_graph):
        result = GraphAlgorithms.breadth_first_search(single_vertex_graph, 1)
        assert result is not None
        assert result == [1]

    def test_dfs_single_vertex(self, single_vertex_graph):
        result = GraphAlgorithms.depth_first_search(single_vertex_graph, 1)
        assert result is not None
        assert result == [1]
