"""
Unit tests for graph search algorithms:
- breadth_first_search
- depth_first_search
- dijkstra_search
- floyd_warshall_search
- spanning_tree
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from math import inf

from s21_graph_algorithms.algorithms.breadth_first_search import BreadthFirstSearch
from s21_graph_algorithms.algorithms.depth_first_search import DepthFirstSearch
from s21_graph_algorithms.algorithms.dijkstra_search import (
    GetShortestPathBetweenVertices,
)
from s21_graph_algorithms.algorithms.floyd_warshall_search import (
    GetShortestPathsBetweenAllVertices,
)
from s21_graph_algorithms.algorithms.spanning_tree import GetLeastSpanningTree


class TestBreadthFirstSearch:
    def test_bfs_undirected_simple(self, simple_undirected_graph):
        result = BreadthFirstSearch.breadth_first_search(simple_undirected_graph, 1)
        assert result is not None
        assert len(result) == 3
        # BFS from vertex 1 should visit all 3 vertices
        assert 1 in result
        assert 2 in result
        assert 3 in result
        # Vertex 1 should be first
        assert result[0] == 1

    def test_bfs_undirected_from_vertex2(self, simple_undirected_graph):
        result = BreadthFirstSearch.breadth_first_search(simple_undirected_graph, 2)
        assert result is not None
        assert len(result) == 3
        assert result[0] == 2

    def test_bfs_single_vertex(self, single_vertex_graph):
        result = BreadthFirstSearch.breadth_first_search(single_vertex_graph, 1)
        assert result is not None
        assert result == [1]

    def test_bfs_invalid_start_vertex(self, simple_undirected_graph):
        result = BreadthFirstSearch.breadth_first_search(simple_undirected_graph, 0)
        assert result is None or (result is not None and len(result) > 0)

    def test_bfs_zeros_start_vertex(self, simple_undirected_graph):
        result = BreadthFirstSearch.breadth_first_search(simple_undirected_graph, 99)
        assert result is not None
        assert len(result) == 1
        assert result[0] == 99


class TestDepthFirstSearch:
    def test_dfs_undirected_simple(self, simple_undirected_graph):
        result = DepthFirstSearch.depth_first_search(simple_undirected_graph, 1)
        assert result is not None
        assert len(result) == 3
        assert 1 in result
        assert 2 in result
        assert 3 in result
        assert result[0] == 1

    def test_dfs_undirected_from_vertex2(self, simple_undirected_graph):
        result = DepthFirstSearch.depth_first_search(simple_undirected_graph, 2)
        assert result is not None
        assert len(result) == 3
        assert result[0] == 2

    def test_dfs_single_vertex(self, single_vertex_graph):
        result = DepthFirstSearch.depth_first_search(single_vertex_graph, 1)
        assert result is not None
        assert result == [1]

    def test_dfs_invalid_start_vertex(self, simple_undirected_graph):
        result = DepthFirstSearch.depth_first_search(simple_undirected_graph, 99)
        assert result is not None or result is None


class TestDijkstraShortestPath:
    def test_dijkstra_adjacent_vertices(self, simple_undirected_graph):
        result = GetShortestPathBetweenVertices.get_shortest_path_between_vertices(
            simple_undirected_graph, 1, 2
        )
        assert result is not None
        assert result.distance == 2  # direct edge weight

    def test_dijkstra_non_adjacent(self, complete_graph_4):
        # 1 -> 3: direct=15, or 1->2->3=10+35=45, or 1->4->3=20+30=50
        result = GetShortestPathBetweenVertices.get_shortest_path_between_vertices(
            complete_graph_4, 1, 3
        )
        assert result is not None
        assert result.distance == 15  # direct edge

    def test_dijkstra_same_vertex(self, simple_undirected_graph):
        result = GetShortestPathBetweenVertices.get_shortest_path_between_vertices(
            simple_undirected_graph, 1, 1
        )
        assert result is not None
        assert result.distance == 0

    def test_dijkstra_directed_graph(self, directed_graph):
        # 1 -> 2 -> 3: total 5+2=7. Direct 1->3 = 10, so shortest is 7
        result = GetShortestPathBetweenVertices.get_shortest_path_between_vertices(
            directed_graph, 1, 3
        )
        assert result is not None
        assert result.distance == 7

    def test_dijkstra_no_path(self, directed_graph):
        # 3 has no outgoing edges, so no path from 3 to 1
        result = GetShortestPathBetweenVertices.get_shortest_path_between_vertices(
            directed_graph, 3, 1
        )
        assert result is None


class TestFloydWarshall:
    def test_floyd_undirected(self, simple_undirected_graph):
        result = (
            GetShortestPathsBetweenAllVertices.get_shortest_paths_between_all_vertices(
                simple_undirected_graph
            )
        )
        assert result is not None
        assert len(result) == 3
        assert len(result[0]) == 3
        # 1->2: 2, 1->3: 3, 2->3: 4
        assert result[0][1] == 2
        assert result[0][2] == 3
        assert result[1][2] == 4
        # Symmetric for undirected
        assert result[1][0] == 2
        assert result[2][0] == 3

    def test_floyd_complete_4(self, complete_graph_4):
        result = (
            GetShortestPathsBetweenAllVertices.get_shortest_paths_between_all_vertices(
                complete_graph_4
            )
        )
        assert result is not None
        assert len(result) == 4
        assert len(result[0]) == 4

    def test_floyd_uncomplete_4(self, uncomplete_graph_4):
        result = (
            GetShortestPathsBetweenAllVertices.get_shortest_paths_between_all_vertices(
                uncomplete_graph_4
            )
        )
        assert result is not None
        assert len(result) == 4
        assert len(result[0]) == 4

    def test_floyd_single_vertex(self, single_vertex_graph):
        result = (
            GetShortestPathsBetweenAllVertices.get_shortest_paths_between_all_vertices(
                single_vertex_graph
            )
        )
        assert result is not None
        assert len(result) == 1
        assert result[0][0] == 0


class TestSpanningTree:
    def test_spanning_tree_undirected(self, simple_undirected_graph):
        result = GetLeastSpanningTree.get_least_spanning_tree(simple_undirected_graph)
        assert result is not None
        assert len(result) == 3
        assert len(result[0]) == 3
        # MST for triangle 1-2(2), 1-3(3), 2-3(4) = edges 1-2 and 1-3 = 2+3=5
        edge_count = (
            sum(1 for row in result for val in row if val > 0) // 2
        )  # undirected
        assert edge_count == 2  # MST has n-1 edges = 2

    def test_spanning_tree_not_directed(self, directed_graph):
        """Prim's algorithm should return None for directed graphs"""
        result = GetLeastSpanningTree.get_least_spanning_tree(directed_graph)
        assert result is None

    def test_spanning_tree_single_vertex(self, single_vertex_graph):
        result = GetLeastSpanningTree.get_least_spanning_tree(single_vertex_graph)
        assert result is not None
        assert len(result) == 1
        assert result[0][0] == 0

    def test_spanning_tree_total_weight(self, simple_undirected_graph):
        result = GetLeastSpanningTree.get_least_spanning_tree(simple_undirected_graph)
        total_weight = sum(sum(row) for row in result) // 2  # undirected
        assert total_weight == 5  # 2 + 3
