"""
Shared fixtures and mocks for all tests.
"""

import sys
import os
from pathlib import Path
from typing import List

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from s21_graph.models.models import WeightedNextVertex


# -----------------------------------------------------------
# Mock the queue/stack interface for tests that don't need C++
# -----------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def mock_queue_stack():
    """
    Automatically mock s21_queue_stack to avoid dependency on .so files.
    This fixture runs once before all tests.
    """
    import types

    class MockList:
        """Simple list-based mock for s21_queue_stack"""

        def __init__(self):
            self._items = []

        def __bool__(self):
            return len(self._items) > 0

        def __len__(self):
            return len(self._items)

    class MockQueue(MockList):
        def push(self, value):
            self._items.append(value)

        def pop(self):
            if self._items:
                return self._items.pop(0)
            raise IndexError("pop from empty queue")

    class MockStack(MockList):
        def push(self, value):
            self._items.append(value)

        def pop(self):
            if self._items:
                return self._items.pop()
            raise IndexError("pop from empty stack")

    # Patch the module
    mock_module = types.ModuleType("s21_queue_stack")
    mock_module.queue = MockQueue
    mock_module.stack = MockStack

    # Also patch the interface submodule
    mock_interface = types.ModuleType("s21_queue_stack.s21_queue_stack_interface")
    mock_interface.queue = MockQueue
    mock_interface.stack = MockStack

    if "s21_queue_stack" in sys.modules:
        del sys.modules["s21_queue_stack"]
    if "s21_queue_stack.s21_queue_stack_interface" in sys.modules:
        del sys.modules["s21_queue_stack.s21_queue_stack_interface"]

    sys.modules["s21_queue_stack"] = mock_module
    sys.modules["s21_queue_stack.s21_queue_stack_interface"] = mock_interface


# -----------------------------------------------------------
# Graph fixtures
# -----------------------------------------------------------
@pytest.fixture
def simple_undirected_graph():
    """
    Simple 3-vertex undirected weighted graph:

    1 --2-- 2
    |       |
    3       4
    |       |
    3 --5-- 3

    Matrix:
        1   2   3
    1   0   2   3
    2   2   0   4
    3   3   4   0
    """
    from s21_graph.s21_graph import Graph

    g = Graph()
    # Use internal loading trick: create a temp file, load from it
    g.load_graph_from_file(
        _write_temp_graph(
            [
                "3",
                "0 2 3",
                "2 0 4",
                "3 4 0",
            ]
        )
    )
    return g


@pytest.fixture
def directed_graph():
    """
    Simple 3-vertex directed weighted graph:
    1 -> 2 (weight 5)
    1 -> 3 (weight 10)
    2 -> 3 (weight 2)

    Matrix:
        1   2   3
    1   0   5  10
    2   0   0   2
    3   0   0   0
    """
    from s21_graph.s21_graph import Graph

    g = Graph()
    g.load_graph_from_file(
        _write_temp_graph(
            [
                "3",
                "0 5 10",
                "0 0 2",
                "0 0 0",
            ]
        )
    )
    return g


@pytest.fixture
def complete_graph_4():
    """
    Complete 4-vertex undirected graph (smallest non-trivial TSP):

    Matrix:
        1   2   3   4
    1   0  10  15  20
    2  10   0  35  25
    3  15  35   0  30
    4  20  25  30   0
    """
    from s21_graph.s21_graph import Graph

    g = Graph()
    g.load_graph_from_file(
        _write_temp_graph(
            [
                "4",
                "0 10 15 20",
                "10 0 35 25",
                "15 35 0 30",
                "20 25 30 0",
            ]
        )
    )
    return g


@pytest.fixture
def uncomplete_graph_4():
    from s21_graph.s21_graph import Graph

    g = Graph()
    g.load_graph_from_file(
        _write_temp_graph(
            [
                "4",
                "0 10 0 20",
                "10 0 35 0",
                "0 35 0 30",
                "20 0 30 0",
            ]
        )
    )
    return g


@pytest.fixture
def full_graph_12():
    from s21_graph.s21_graph import Graph

    g = Graph()
    g.load_graph_from_file(
        _write_temp_graph(
            [
                "12",
                "0 65 6 62 52 35 45 29 7 17 27 11",
                "65 0 7 96 38 68 91 87 80 27 38 71",
                "6 7 0 92 23 57 13 83 59 70 75 68",
                "62 96 92 0 68 46 97 98 24 77 58 99",
                "52 38 23 68 0 26 69 68 58 43 84 26",
                "35 68 57 46 26 0 21 19 91 91 41 89",
                "45 91 13 97 69 21 0 74 9 67 18 98",
                "29 87 83 98 68 19 74 0 32 18 80 61",
                "7 80 59 24 58 91 9 32 0 36 49 85",
                "17 27 70 77 43 91 67 18 36 0 23 25",
                "27 38 75 58 84 41 18 80 49 23 0 70",
                "11 71 68 99 26 89 98 61 85 25 70 0",
            ]
        )
    )
    return g


@pytest.fixture
def dir_graph_11():
    from s21_graph.s21_graph import Graph

    g = Graph()
    g.load_graph_from_file(
        _write_temp_graph(
            [
                "11",
                "0   0   0   0   16  0   0   0   0   0   0",
                "29  0   15  29  0   0   0   0   0   41  0",
                "0   15  0   0   0   0   81  9   23  0   0",
                "0   0   15  0   4   0   0   0   0   0   25",
                "16  0   0   4   0   16  0   9   0   16  0",
                "0   40  0   0   16  0   95  0   36  0   37",
                "0   0   0   92  0   0   0   90  0   0   0",
                "0   0   0   0   0   0   0   0   15  25  0",
                "0   0   0   0   0   36  0   15  0   0   0",
                "0   41  27  0   0   0   99  0   35  0   38",
                "18  0   0   0   22  0   0   13  0   0   0",
            ]
        )
    )
    return g


@pytest.fixture
def disconnected_graph():
    """Disconnected graph: vertex 3 is isolated"""
    from s21_graph.s21_graph import Graph

    g = Graph()
    g.load_graph_from_file(
        _write_temp_graph(
            [
                "3",
                "0 1 0",
                "1 0 0",
                "0 0 0",
            ]
        )
    )
    return g


@pytest.fixture
def null_graph():
    """Graph with no edges"""
    from s21_graph.s21_graph import Graph

    g = Graph()
    g.load_graph_from_file(
        _write_temp_graph(
            [
                "3",
                "0 0 0",
                "0 0 0",
                "0 0 0",
            ]
        )
    )
    return g


@pytest.fixture
def single_vertex_graph():
    """Single vertex graph"""
    from s21_graph.s21_graph import Graph

    g = Graph()
    g.load_graph_from_file(
        _write_temp_graph(
            [
                "1",
                "0",
            ]
        )
    )
    return g


# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------
_temp_files = []


def _write_temp_graph(lines: List[str]) -> str:
    """Write a temporary graph file and return its path."""
    import tempfile

    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    )
    for line in lines:
        f.write(line + "\n")
    f.close()
    _temp_files.append(f.name)
    return f.name


def pytest_unconfigure():
    """Cleanup temp files."""
    import os

    for path in _temp_files:
        try:
            os.unlink(path)
        except OSError:
            pass
