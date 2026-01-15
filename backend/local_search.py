import random
from main import place_cargo, calculate_fitness, Solution

class LocalSearch:
    """
    Local search improvement for cargo orderings.
    Swap, insertion, and adjustable iterations for challenging instances.
    """

    def __init__(self, cargo_items, container, max_iterations=2000, patience=200):
        self.cargo_items = cargo_items
        self.container = container
        self.max_iterations = max_iterations
        self.patience = patience

    # Swap two items
    def _swap(self, order):
        i, j = random.sample(range(len(order)), 2)
        new_order = order[:]
        new_order[i], new_order[j] = new_order[j], new_order[i]
        return new_order

    # Remove and insert an item at new position
    def _insert(self, order):
        i, j = random.sample(range(len(order)), 2)
        new_order = order[:]
        item = new_order.pop(i)
        new_order.insert(j, item)
        return new_order

    def improve(self, solution: Solution, verbose=False):
        best = solution
        best_fitness = solution.fitness
        no_improve = 0

        for iteration in range(self.max_iterations):
            if no_improve >= self.patience:
                break

            if random.random() < 0.5:
                candidate_order = self._swap(best.order)
            else:
                candidate_order = self._insert(best.order)

            candidate = place_cargo(candidate_order, self.cargo_items, self.container)
            calculate_fitness(candidate)

            if candidate.fitness < best_fitness:
                best = candidate
                best_fitness = candidate.fitness
                no_improve = 0

                if verbose:
                    print(f"Local search improved: {best_fitness:.2f} (iter {iteration})")

                if best_fitness == 0:
                    break
            else:
                no_improve += 1

        return best
