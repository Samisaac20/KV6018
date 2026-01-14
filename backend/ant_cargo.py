# aco_cargo.py

import random
from copy import deepcopy
from typing import List

from local_search import LocalSearch
from grid_refinement import refine_solution

from main import (
    Cargo,
    Container,
    Solution,
    place_cargo,
    calculate_fitness,
)


class AntColonyOptimisation:
    """
    Ant Colony Optimisation for cargo ordering.
    Each ant constructs a permutation of cargo indices.
    """

    def __init__(
        self,
        cargo_items: List[Cargo],
        container: Container,
        n_ants: int = 20,
        n_iterations: int = 100,
        alpha: float = 1.0,
        beta: float = 2.0,
        evaporation: float = 0.5,
        q: float = 100.0,
    ):
        self.cargo_items = deepcopy(cargo_items)
        self.container = container
        self.n_items = len(cargo_items)

        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.q = q

        self.tau = [[1.0 for _ in range(self.n_items)] for _ in range(self.n_items)]

    # ------------------------------------------------------------------

    def _heuristic(self, item_idx: int) -> float:
        item = self.cargo_items[item_idx]
        return item.diameter * item.weight

    # ------------------------------------------------------------------

    def _construct_solution(self) -> List[int]:
        unvisited = set(range(self.n_items))
        order = []

        current = random.choice(list(unvisited))
        order.append(current)
        unvisited.remove(current)

        while unvisited:
            values = []
            total = 0.0

            for j in unvisited:
                v = (self.tau[current][j] ** self.alpha) * (
                    self._heuristic(j) ** self.beta
                )
                values.append((j, v))
                total += v

            r = random.random()
            acc = 0.0
            next_item = None

            for j, v in values:
                acc += v / total
                if r <= acc:
                    next_item = j
                    break

            if next_item is None:
                next_item = random.choice(list(unvisited))

            order.append(next_item)
            unvisited.remove(next_item)
            current = next_item

        return order

    def _update_pheromones(self, solutions: List[Solution]):
        for i in range(self.n_items):
            for j in range(self.n_items):
                self.tau[i][j] *= (1.0 - self.evaporation)

        for sol in solutions:
            if sol.fitness <= 0:
                continue

            deposit = self.q / sol.fitness
            for i in range(len(sol.order) - 1):
                a = sol.order[i]
                b = sol.order[i + 1]
                self.tau[a][b] += deposit


    def run(self, verbose: bool = True) -> Solution:
        best_solution = None
        ls = LocalSearch(self.cargo_items, self.container)

        for iteration in range(1, self.n_iterations + 1):
            solutions = []

            for _ in range(self.n_ants):
                order = self._construct_solution()
                sol = place_cargo(order, self.cargo_items, self.container)
                calculate_fitness(sol)

                # LOCAL SEARCH REFINEMENT
                sol = ls.improve(sol)

                solutions.append(sol)

                if best_solution is None or sol.fitness < best_solution.fitness:
                    best_solution = sol

            self._update_pheromones(solutions)

            if verbose and iteration % 10 == 0:
                print(
                    f"Iteration {iteration:3d} | "
                    f"Best fitness: {best_solution.fitness:.2f}"
                )

            if best_solution.fitness == 0:
                break

        if verbose:
            print("\nACO Complete")
            print(f"Best fitness: {best_solution.fitness:.2f}")

        # FINAL GRID REFINEMENT
        best_solution = refine_solution(
            best_solution,
            self.cargo_items,
            self.container,
            fine_step=0.1,
        )

        return best_solution
