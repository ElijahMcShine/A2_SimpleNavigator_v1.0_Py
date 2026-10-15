"""
Unit tests for models/models.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from s21_graph.models.models import TsmResultPython, WeightedNextVertex


class TestTsmResultPython:
    def test_create_with_vertices_and_distance(self):
        result = TsmResultPython([1, 2, 3, 1], 42)
        assert result.vertices == [1, 2, 3, 1]
        assert result.distance == 42

    def test_empty_vertices_list(self):
        result = TsmResultPython([], 0)
        assert result.vertices == []
        assert result.distance == 0

    """def test_ordering_by_distance(self):
        r1 = TsmResultPython([1, 2, 1], 100)
        r2 = TsmResultPython([1, 3, 1], 50)
        r3 = TsmResultPython([1, 4, 1], 75)
        sorted_results = sorted([r1, r2, r3])
        assert sorted_results[0].distance == 50  # r2
        assert sorted_results[1].distance == 75  # r3
        assert sorted_results[2].distance == 100  # r1"""


class TestWeightedNextVertex:
    def test_create_edge(self):
        edge = WeightedNextVertex(1, 2, 10)
        assert edge.first_vertex == 1
        assert edge.second_vertex == 2
        assert edge.weight == 10

    """def test_ordering_by_weight(self):
        e1 = WeightedNextVertex(1, 2, 30)
        e2 = WeightedNextVertex(2, 3, 10)
        e3 = WeightedNextVertex(3, 4, 20)
        sorted_edges = sorted([e1, e2, e3])
        assert sorted_edges[0].weight == 10
        assert sorted_edges[1].weight == 20
        assert sorted_edges[2].weight == 30"""

    def test_negative_weight(self):
        edge = WeightedNextVertex(1, 2, -5)
        assert edge.weight == -5
