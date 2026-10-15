"""
Unit tests for s21_graph/s21_graph.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import os
import tempfile
from s21_graph.s21_graph import Graph
from s21_graph.models.models import WeightedNextVertex


class TestGraphLoading:
    def test_load_valid_graph(self, simple_undirected_graph):
        assert simple_undirected_graph.get_vertices_count() == 3

    def test_load_from_file_file_not_found(self):
        g = Graph()
        result = g.load_graph_from_file("nonexistent_file_xyz.txt")
        assert result is False

    def test_load_empty_file(self):
        g = Graph()
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        f.write("")
        f.close()
        result = g.load_graph_from_file(f.name)
        os.unlink(f.name)
        assert result is False

    def test_load_invalid_first_line(self):
        g = Graph()
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        f.write("abc\n1 2\n")
        f.close()
        result = g.load_graph_from_file(f.name)
        os.unlink(f.name)
        assert result is False

    def test_load_negative_size(self):
        g = Graph()
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        f.write("-1\n")
        f.close()
        result = g.load_graph_from_file(f.name)
        os.unlink(f.name)
        assert result is False

    def test_load_size_zero(self):
        g = Graph()
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        f.write("0\n")
        f.close()
        result = g.load_graph_from_file(f.name)
        os.unlink(f.name)
        assert result is False

    def test_load_wrong_row_length(self):
        g = Graph()
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        f.write("3\n0 1 2\n0 1\n0 1 2\n")
        f.close()
        result = g.load_graph_from_file(f.name)
        os.unlink(f.name)
        assert result is False

    def test_load_not_enough_rows(self):
        g = Graph()
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        f.write("3\n0 1 2\n0 1 2\n")
        f.close()
        result = g.load_graph_from_file(f.name)
        os.unlink(f.name)
        assert result is False


class TestGraphProperties:
    def test_is_graph_directed_undirected(self, simple_undirected_graph):
        assert simple_undirected_graph.is_graph_directed() is False

    def test_is_graph_directed_directed(self, directed_graph):
        assert directed_graph.is_graph_directed() is True

    def test_is_graph_connected_connected(self, simple_undirected_graph):
        assert simple_undirected_graph.is_graph_connected() is True

    def test_is_graph_connected_dir(self, dir_graph_11):
        assert dir_graph_11.is_graph_connected() is True

    def test_is_graph_connected_disconnected(self, disconnected_graph):
        assert disconnected_graph.is_graph_connected() is False

    def test_is_null_graph_false(self, simple_undirected_graph):
        assert simple_undirected_graph.is_null_graph() is False

    def test_is_null_graph_true(self, null_graph):
        assert null_graph.is_null_graph() is True

    def test_check_graph_for_requirements_valid(self, simple_undirected_graph):
        assert simple_undirected_graph.check_graph_for_requirements() is True

    def test_check_graph_for_requirements_disconnected(self, disconnected_graph):
        assert disconnected_graph.check_graph_for_requirements() is False

    def test_get_vertices_count(self, complete_graph_4):
        assert complete_graph_4.get_vertices_count() == 4

    def test_single_vertex_count(self, single_vertex_graph):
        assert single_vertex_graph.get_vertices_count() == 1


class TestGraphOperations:
    def test_next_vertices(self, simple_undirected_graph):
        neighbors = simple_undirected_graph.next_vertices(1)
        assert neighbors is not None
        assert len(neighbors) == 2
        vertices = [(n.second_vertex, n.weight) for n in neighbors]
        assert (2, 2) in vertices
        assert (3, 3) in vertices

    def test_next_vertices_no_neighbors(self, disconnected_graph):
        neighbors = disconnected_graph.next_vertices(3)
        assert neighbors is None

    def test_get_base_weighted_matrix(self, simple_undirected_graph):
        matrix = simple_undirected_graph.get_base_weighted_matrix()
        assert matrix is not None
        assert len(matrix) == 3
        assert matrix[0][0] == 0
        assert matrix[0][1] == 2
        assert matrix[0][2] == 3
        assert matrix[1][0] == 2
        assert matrix[1][1] == 0
        assert matrix[1][2] == 4

    def test_get_all_edges_undirected(self, simple_undirected_graph):
        edges = simple_undirected_graph.get_all_edges()
        # Undirected: both directions stored in matrix
        assert len(edges) == 6  # 2 edges * 2 directions each

    def test_get_all_edges_directed(self, directed_graph):
        edges = directed_graph.get_all_edges()
        assert len(edges) == 3  # 3 directed edges

    def test_get_all_edges_null(self, null_graph):
        edges = null_graph.get_all_edges()
        assert len(edges) == 0


class TestGraphExport:
    def test_export_to_dot_undirected(self, simple_undirected_graph, tmp_path):
        dot_file = tmp_path / "test_graph.dot"
        result = simple_undirected_graph.export_graph_to_dot(str(dot_file))
        assert result is True
        assert dot_file.exists()
        content = dot_file.read_text(encoding="utf-8")
        assert "graph graphname" in content
        assert "V1 -- V2" in content

    def test_export_to_dot_directed(self, directed_graph, tmp_path):
        dot_file = tmp_path / "test_dir.dot"
        result = directed_graph.export_graph_to_dot(str(dot_file))
        assert result is True
        assert dot_file.exists()
        content = dot_file.read_text(encoding="utf-8")
        assert "digraph graphname" in content
        assert "V1 -> V2" in content

    def test_export_to_dot_disconnected(self, disconnected_graph, tmp_path):
        dot_file = tmp_path / "test_dir.dot"
        result = disconnected_graph.export_graph_to_dot(str(dot_file))
        assert result is True
        assert dot_file.exists()
        content = dot_file.read_text(encoding="utf-8")
        assert "graph graphname" in content

    def test_export_to_pdf_undirected(self, simple_undirected_graph, tmp_path):
        pdf_file = tmp_path / "test_graph.pdf"
        result = simple_undirected_graph.export_graph_to_pdf(str(pdf_file))
        assert result is True
        assert pdf_file.exists()

    def test_export_to_pdf_directed(self, directed_graph, tmp_path):
        pdf_file = tmp_path / "test_dir.pdf"
        result = directed_graph.export_graph_to_pdf(str(pdf_file))
        assert result is True
        assert pdf_file.exists()

    def test_export_to_pdf_disconnected(self, disconnected_graph, tmp_path):
        pdf_file = tmp_path / "test_dir.pdf"
        result = disconnected_graph.export_graph_to_pdf(str(pdf_file))
        assert result is True
        assert pdf_file.exists()


class TestGraphEdgeCases:
    def test_graph_with_negative_weights(self):
        """Graph with negative weights (violates requirements but still loads)"""
        import tempfile

        g = Graph()
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        f.write("3\n0 -1 2\n-1 0 3\n2 3 0\n")
        f.close()
        g.load_graph_from_file(f.name)
        os.unlink(f.name)
        assert g.check_graph_for_requirements() is False
