# local_search.py

import random
from copy import deepcopy
from typing import List

from main import (
    Cargo,
    Container,
    Solution,
    place_cargo,
    calculate_fitness,
)


class LocalSearch:
    """
    Deterministic local improvement over cargo orderings.
    Uses swap and insertion neighbourhoods.
    """

    def __init__(
        self,
        cargo_items: List[Cargo],
        container: Container,
        max_iterations: int = 500,
        patience: int = 50,
    ):
        self.cargo_items = cargo_items
        self.container = container
        self.max_iterations = max_iterations
        self.patience = patience


    def _swap(self, order: List[int]) -> List[int]:
        i, j = random.sample(range(len(order)), 2)
        new_order = order[:]
        new_order[i], new_order[j] = new_order[j], new_order[i]
        return new_order

    def _insert(self, order: List[int]) -> List[int]:
        i, j = random.sample(range(len(order)), 2)
        new_order = order[:]
        item = new_order.pop(i)
        new_order.insert(j, item)
        return new_order


    def improve(self, solution: Solution, verbose: bool = False) -> Solution:
        """
        Improve a given solution by local search.
        """
        best = solution
        best_fitness = solution.fitness

        no_improve = 0

        for iteration in range(self.max_iterations):
            if no_improve >= self.patience:
                break

            # Choose neighbourhood operator
            if random.random() < 0.5:
                candidate_order = self._swap(best.order)
            else:
                candidate_order = self._insert(best.order)

            candidate = place_cargo(
                candidate_order,
                self.cargo_items,
                self.container,
            )
            calculate_fitness(candidate)

            if candidate.fitness < best_fitness:
                best = candidate
                best_fitness = candidate.fitness
                no_improve = 0

                if verbose:
                    print(
                        f"Local search improved: "
                        f"{best_fitness:.2f} (iter {iteration})"
                    )

                if best_fitness == 0:
                    break
            else:
                no_improve += 1

        return best
