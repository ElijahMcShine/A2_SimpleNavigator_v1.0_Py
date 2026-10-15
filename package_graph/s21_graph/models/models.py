""" Base models for graphs algorithmis """

from dataclasses import dataclass
from typing import List


@dataclass(order=True)
class TsmResultPython:
    """Data structure for paths"""

    vertices: List[int]
    distance: int


@dataclass(order=True)
class WeightedNextVertex:
    """Data structure for edge"""

    first_vertex: int
    second_vertex: int
    weight: int
