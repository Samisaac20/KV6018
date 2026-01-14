from main import place_cargo, calculate_fitness, Solution

def refine_solution(solution: Solution, cargo_items, container, fine_step=0.05):
    """
    Re-run placement for a given order with finer grid to allow tight packing.
    """
    refined = place_cargo(solution.order, cargo_items, container, grid_step=fine_step)
    calculate_fitness(refined)
    return refined
