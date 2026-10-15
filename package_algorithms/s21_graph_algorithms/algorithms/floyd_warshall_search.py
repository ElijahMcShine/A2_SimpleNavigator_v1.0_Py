"""Module for search shortest paths between all verticies 
    in graph with Floyd-Warshall search algorithm"""

from typing import List

from s21_graph.s21_graph import Graph

# https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm


class GetShortestPathsBetweenAllVertices:
    """Class for search shortest paths between all verticies
    in graph with Floyd-Warshall search algorithm"""

    @staticmethod
    def get_shortest_paths_between_all_vertices(graph: Graph) -> List[List[int]] | None:
        """Function for search shortest paths between all verticies
        in graph with Floyd-Warshall search algorithm"""

        matrix = graph.get_base_weighted_matrix()
        max_len = len(matrix)
        if matrix is not None:
            for k in range(max_len):
                for i in range(max_len):
                    for j in range(max_len):
                        if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                            matrix[i][j] = matrix[i][k] + matrix[k][j]
            res: List[List[int]] = [[] for _ in range(max_len)]

            try:
                for y in range(max_len):
                    for x in range(max_len):
                        res[y].append(int(matrix[y][x]))
                return res
            except:
                return None
        else:
            return None
