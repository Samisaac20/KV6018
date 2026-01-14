from typing import List
from copy import deepcopy

from main import (
    Cargo,
    Container,
    Solution,
    place_cargo,
    calculate_fitness,
)


class GreedySearch:
    """
    Greedy bin-packing baseline.
    Strategy:
    - Sort items by descending diameter
    - Tie-break by descending weight
    - Place once using bottom-left heuristic
    """

    def __init__(self, cargo_items: List[Cargo], container: Container):
        self.cargo_items = deepcopy(cargo_items)
        self.container = container

    def run(self, verbose: bool = True) -> Solution:
        # Greedy ordering: largest items first
        order = sorted(
            range(len(self.cargo_items)),
            key=lambda i: (
                self.cargo_items[i].diameter,
                self.cargo_items[i].weight,
            ),
            reverse=True,
        )

        # Place cargo
        solution = place_cargo(order, self.cargo_items, self.container)

        # Evaluate fitness
        calculate_fitness(solution)

        if verbose:
            placed = sum(1 for c in solution.cargo_items if c.placed)
            print("\nGreedy Search Complete")
            print(f"Placed items: {placed}/{len(self.cargo_items)}")
            print(f"Fitness: {solution.fitness:.2f}")

        return solution
