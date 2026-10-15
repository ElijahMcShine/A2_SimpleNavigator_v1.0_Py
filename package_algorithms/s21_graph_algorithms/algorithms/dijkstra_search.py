"""Module for search shortest paths between two verticies 
    in graph with Dijkstra algorithm"""

from queue import PriorityQueue
from typing import List

from s21_graph.s21_graph import Graph
from s21_graph.models.models import WeightedNextVertex, TsmResultPython


# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm


class GetShortestPathBetweenVertices:
    """Class for search shortest paths between two verticies
    in graph with Dijkstra algorithm"""

    @staticmethod
    def get_shortest_path_between_vertices(
        graph: Graph, vertex1: int, vertex2: int
    ) -> TsmResultPython | None:
        """Function for search shortest paths between two verticies
        in graph with Dijkstra algorithm"""

        frontier: PriorityQueue = PriorityQueue()
        frontier.put((0, vertex1))
        came_from = {}
        cost_so_far = {}
        came_from[vertex1] = vertex1
        cost_so_far[vertex1] = 0

        while not frontier.empty():
            current = frontier.get()
            neighbors: List[WeightedNextVertex] | None = graph.next_vertices(current[1])

            if neighbors is not None:
                for next_step in neighbors:
                    new_cost = cost_so_far[current[1]] + next_step.weight
                    if (
                        next_step.second_vertex not in cost_so_far
                        or new_cost < cost_so_far[next_step.second_vertex]
                    ):
                        cost_so_far[next_step.second_vertex] = new_cost
                        priority = new_cost
                        frontier.put((priority, next_step.second_vertex))
                        came_from[next_step.second_vertex] = current[1]

            if current[1] == vertex2:
                path = []
                temp = current[1]
                while temp != vertex1:
                    path.append(temp)
                    temp = came_from[temp]
                path.append(vertex1)
                path.reverse()

                return TsmResultPython(path, cost_so_far[current[1]])
                # return cost_so_far[current[1]]

        return None
