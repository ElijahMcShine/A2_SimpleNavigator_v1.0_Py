""" Module with Graph class for work with graphs """

from collections import deque
from math import inf
from typing import List
import graphviz
from s21_graph.models.models import WeightedNextVertex


class Graph:
    """Graph class for work with graphs"""

    def __init__(self):
        self.__graph_size: int = 1
        self.__graph_matrix: List[List[int]] = [[0]]

    def load_graph_from_file(self, filename: str) -> bool:
        """Loads graph as adjacency matrix from file"""

        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if len(lines) == 0:
                    raise ValueError("Error message. Empty file")

            temp_size = int(lines[0])
            if temp_size < 1:
                raise ValueError("Error message. Wrong file format")

            if len(lines) < temp_size + 1:
                raise ValueError("Error message. Wrong file format")
            temp_matrix = []

            for i in range(1, temp_size + 1):
                temp = lines[i].split()
                if len(temp) != temp_size:
                    raise ValueError("Error message. Wrong file format")

                temp_matrix.append(list(map(int, temp)))

            self.__graph_size = temp_size
            self.__graph_matrix = temp_matrix
            return True

        except ValueError as e:
            print(e)
            return False
        except FileNotFoundError:
            print("Error message. File " + filename + " not found.")
            return False
        except Exception as e:
            print(e)
            return False

    def export_graph_to_dot(self, filename: str) -> bool:
        """To save graph to file in DOT format"""

        try:
            with open(filename, "w", encoding="utf-8") as file:
                text: str = ""
                if self.is_graph_directed():
                    text += "digraph graphname {\n"
                else:
                    text += "graph graphname {\n"

                for i in range(self.__graph_size):
                    text += "\tV" + str(i + 1) + ";\n"

                text += self.__get_graph_str() + "}"

                file.write(text)
            return True

        except Exception as e:
            print(e)
            return False

    def export_graph_to_pdf(self, filename: str) -> bool:
        """To save graph to file in PDF format"""

        try:
            text: str = ""
            if self.is_graph_directed():
                text += "digraph graphname {\n"
            else:
                text += "graph graphname {\n"

            for i in range(self.__graph_size):
                text += "\tV" + str(i + 1) + ";\n"

            text += self.__get_graph_str() + "}"

            dot = graphviz.Source(text)
            dot.render(filename, format="pdf", view=False)
            return True
        except Exception as e:
            print(e)
            return False

    def __get_graph_str(self) -> str:
        """Auxiliary function for converting a graph to a string"""

        res: str = ""
        for y in range(self.__graph_size):
            if self.is_graph_directed():
                start = 0
            else:
                start = y + 1
            for x in range(start, self.__graph_size):
                if self.__graph_matrix[y][x] != 0:
                    res += "\tV" + str(y + 1)
                    if self.is_graph_directed():
                        res += " -> V" + str(x + 1)
                    else:
                        res += " -- V" + str(x + 1)
                    if self.__is_graph_weighted():
                        res += (
                            ' [style="solid", label="'
                            + str(self.__graph_matrix[y][x])
                            + '"];\n'
                        )
                    else:
                        res += ";\n"
        return res

    def next_vertices(self, current_vertex: int) -> List[WeightedNextVertex] | None:
        """The function returns the edges of the graph
        along which further movement is possible"""

        if current_vertex < 1 or current_vertex > self.__graph_size:
            return None
        res = []
        for i in range(self.__graph_size):
            if self.__graph_matrix[current_vertex - 1][i] != 0:
                res.append(
                    WeightedNextVertex(
                        current_vertex,
                        i + 1,
                        self.__graph_matrix[current_vertex - 1][i],
                    )
                )
        if not res:
            return None

        return res

    def get_base_weighted_matrix(self) -> List[List[int]] | None:
        """Returns the adjacency matrix of the graph,
        replacing the cost of impossible paths with infinity"""

        res = []
        for y in range(self.__graph_size):
            res.append([])
            for x in range(self.__graph_size):
                if x == y:
                    res[y].append(0)
                elif self.__graph_matrix[y][x] == 0:
                    res[y].append(inf)
                else:
                    res[y].append(self.__graph_matrix[y][x])
        if len(res) == 0:
            return None

        return res

    def get_vertices_count(self) -> int:
        """Returns the size of the graph"""
        return self.__graph_size

    def get_all_edges(self) -> List[WeightedNextVertex]:
        """Checking for graph weight"""

        res: List[WeightedNextVertex] = []
        for y in range(self.__graph_size):
            for x in range(self.__graph_size):
                if self.__graph_matrix[y][x] != 0:
                    res.append(
                        WeightedNextVertex(y + 1, x + 1, self.__graph_matrix[y][x])
                    )
        return res

    def __is_graph_weighted(self) -> bool:
        """Checking for graph is weighted"""

        for y in range(self.__graph_size):
            for value in self.__graph_matrix[y]:
                if value < 0 or value > 1:
                    return True
        return False

    def is_graph_directed(self) -> bool:
        """Checking for graph is dericted"""

        for y in range(self.__graph_size):
            for x in range(self.__graph_size):
                if self.__graph_matrix[y][x] != self.__graph_matrix[x][y]:
                    return True
        return False

    def is_graph_connected(self) -> bool:
        """Checking for graph is fully connected"""

        if self.is_graph_directed():
            iteration = self.__graph_size
        else:
            iteration = 1

        for i in range(iteration):
            vertex_queue = deque([i + 1])
            res: List[int] = []

            while vertex_queue:
                current = vertex_queue.popleft()
                if current not in res:
                    res.append(current)

                    neighbors: List[WeightedNextVertex] | None = self.next_vertices(
                        current
                    )

                    if neighbors is not None:
                        for neighbor in neighbors:
                            if neighbor.second_vertex not in res:
                                vertex_queue.append(neighbor.second_vertex)

            if len(res) != self.__graph_size:
                return False
        return True

    def is_null_graph(self) -> bool:
        """Checking for graph is null graph"""

        for y in range(self.__graph_size):
            for x in range(self.__graph_size):
                if self.__graph_matrix[y][x] != 0:
                    return False
        return True

    def check_graph_for_requirements(self) -> bool:
        """Verifying that the graph meets the requirements of the assignment"""

        if not self.is_graph_connected():
            return False
        for y in range(self.__graph_size):
            for x in range(self.__graph_size):
                if self.__graph_matrix[y][x] < 0:
                    return False
        return True
