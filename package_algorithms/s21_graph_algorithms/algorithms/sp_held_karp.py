"""Module for solving the traveling salesman problem by Held-Karp method"""

# https://compgeek.co.in/held-karp-algorithm-for-tsp/

from math import inf
from typing import List

from s21_graph.models.models import TsmResultPython
from s21_graph.s21_graph import Graph


class HeldKarpSalesmanProblem:
    """Class for solving the traveling salesman problem by Held-Karp method"""

    @staticmethod
    def solve_traveling_salesman_problem(graph: Graph) -> TsmResultPython | None:
        """Function for solving the traveling salesman problem by Held-Karp method"""

        n = graph.get_vertices_count()
        dist = graph.get_base_weighted_matrix()

        # Total number of subsets (2^n)
        total_subsets = 1 << n

        dp: List[List[TsmResultPython]] = [[] for _ in range(total_subsets)]
        for y in range(total_subsets):
            # dp.append([])
            for x in range(n):
                dp[y].append(TsmResultPython([x + 1], inf))

        # Starting point, cost is 0 to start from the first city
        dp[1][0].distance = 0

        # Iterate over all subsets of cities
        for mask in range(1, total_subsets):
            for u in range(n):
                if mask & (1 << u):
                    for v in range(n):
                        if (mask & (1 << v)) == 0:
                            new_mask = mask | (1 << v)
                            if (
                                dp[new_mask][v].distance
                                > dp[mask][u].distance + dist[u][v]
                            ):
                                dp[new_mask][v].distance = (
                                    dp[mask][u].distance + dist[u][v]
                                )
                                dp[new_mask][v].vertices = dp[mask][u].vertices.copy()
                                dp[new_mask][v].vertices.append(v + 1)

        # Find the minimum cost to complete the tour
        min_cost = inf
        res = None
        for i in range(n):
            if dp[total_subsets - 1][i].distance + dist[i][0] < min_cost:
                min_cost = dp[total_subsets - 1][i].distance + dist[i][0]

                res = dp[total_subsets - 1][i]
                res.distance += dist[i][0]
                res.vertices.append(1)
        return res
