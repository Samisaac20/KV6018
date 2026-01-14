from main import place_cargo, calculate_fitness, Solution
from typing import List


def refine_solution(
    solution: Solution,
    cargo_items,
    container,
    fine_step: float = 0.05,
) -> Solution:
    """
    Re-run placement of an existing order using a finer grid.
    """
    refined = place_cargo(
        solution.order,
        cargo_items,
        container,
        grid_step=fine_step,
    )
    calculate_fitness(refined)
    return refined
