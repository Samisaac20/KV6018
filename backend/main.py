import math
import random
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Circle as PltCircle
from matplotlib.patches import Rectangle as PltRectangle

# DATA STRUCTURES

@dataclass
class Cargo:
    """Cylindrical cargo item to be placed in container"""
    id: int
    diameter: float
    weight: float
    x: float = 0.0
    y: float = 0.0
    placed: bool = False


@dataclass
class Container:
    """Rectangular container specifications"""
    width: float
    depth: float
    max_weight: float


@dataclass
class Solution:
    """Complete solution with placement and evaluation"""
    order: List[int]
    cargo_items: List[Cargo]
    complete: bool
    fitness: float
    violations: Dict[str, float]
    container: Container

    def get_center_of_mass(self) -> Tuple[float, float]:
        """Calculate centre of mass for placed cargo"""
        placed = [c for c in self.cargo_items if c.placed]
        if not placed:
            return (0, 0)

        total_weight = sum(c.weight for c in placed)
        weighted_x = sum(c.x * c.weight for c in placed)
        weighted_y = sum(c.y * c.weight for c in placed)

        return (weighted_x / total_weight, weighted_y / total_weight)


# CARGO PLACEMENT

# Configuration
GRID_STEP = 0.2  # Position grid resolution (units)


def place_cargo(
    order: List[int], cargo_items: List[Cargo], container: Container
) -> Solution:
    # Make copies so we don't modify originals
    cargo_copy = [deepcopy(c) for c in cargo_items]
    placed_cargo = []
    complete = True

    # Place each cargo item in the specified order
    for cargo_id in order:
        cargo = cargo_copy[cargo_id]
        radius = cargo.diameter / 2.0
        position_found = False

        # Simple bottom-left: first valid position found
        y = 0.0
        while y <= container.depth and not position_found:
            x = 0.0
            while x <= container.width and not position_found:
                center_x = x + radius
                center_y = y + radius

                if is_valid_position(
                    center_x, center_y, radius, placed_cargo, container
                ):
                    cargo.x = center_x
                    cargo.y = center_y
                    cargo.placed = True
                    placed_cargo.append(cargo)
                    position_found = True

                x += GRID_STEP
            y += GRID_STEP

        if not position_found:
            complete = False
            break

    # Create solution object
    solution = Solution(
        order=order,
        cargo_items=cargo_copy,
        complete=complete,
        fitness=0.0,  # Will be calculated by fitness function
        violations={},  # Will be filled by fitness function
        container=container,
    )

    return solution


def is_valid_position(
    x: float, y: float, radius: float, placed_cargo: List[Cargo], container: Container
) -> bool:
    # Check 1: Within container bounds
    if x - radius < 0 or x + radius > container.width:
        return False
    if y - radius < 0 or y + radius > container.depth:
        return False

    # Check 2: No overlaps with already-placed cargo
    for placed in placed_cargo:
        distance = math.sqrt((x - placed.x) ** 2 + (y - placed.y) ** 2)
        min_distance = radius + (placed.diameter / 2.0)

        if distance < min_distance:
            return False  # Overlaps!

    # All checks passed
    return True


# FITNESS EVALUATION

# Penalty weights
PENALTY_UNPLACED = 1000.0
PENALTY_WEIGHT_KG = 10.0
PENALTY_COM_DISTANCE = 100.0


def calculate_fitness(solution: Solution) -> float:
    total_penalty = 0.0
    violations = {}

    # Unplaced cargo items 
    unplaced_count = sum(1 for c in solution.cargo_items if not c.placed)
    if unplaced_count > 0:
        penalty = unplaced_count * PENALTY_UNPLACED
        total_penalty += penalty
        violations["unplaced_items"] = unplaced_count
        violations["unplaced_penalty"] = penalty

    if not solution.complete:
        solution.fitness = total_penalty
        solution.violations = violations
        return total_penalty

    # Weight limit violations
    total_weight = sum(c.weight for c in solution.cargo_items if c.placed)
    if total_weight > solution.container.max_weight:
        excess_weight = total_weight - solution.container.max_weight
        penalty = excess_weight * PENALTY_WEIGHT_KG
        total_penalty += penalty
        violations["excess_weight_kg"] = excess_weight
        violations["weight_penalty"] = penalty

    # centre of mass outside circular safe zone
    com_x, com_y = solution.get_center_of_mass()
    center_x = solution.container.width / 2
    center_y = solution.container.depth / 2

    # safe zone radius = 60% of container
    safe_radius = 0.6 * min(solution.container.width, solution.container.depth) / 2
    com_distance_from_center = math.sqrt(
        (com_x - center_x)**2 + (com_y - center_y)**2
    )

    # distance from centre
    com_violation = 0.0
    if com_distance_from_center > safe_radius:
        com_violation = com_distance_from_center - safe_radius

    if com_violation > 0:
        penalty = com_violation * PENALTY_COM_DISTANCE
        total_penalty += penalty
        violations["com_distance_outside"] = com_violation
        violations["com_penalty"] = penalty
        violations["com_position"] = (com_x, com_y)
        violations["safe_radius"] = safe_radius

    # store results in object
    solution.fitness = total_penalty
    solution.violations = violations
    return total_penalty


# GENETIC ALGORITHM

class GeneticAlgorithm:
    def __init__(
        self,
        cargo_items: List[Cargo],
        container: Container,
        population_size: int = 200,
        generations: int = 500,
        mutation_rate: float = 0.15,
        crossover_rate: float = 0.8,
        tournament_size: int = 3,
        elite_size: int = 5,
        stagnation_limit: int = 100
    ):
        self.cargo_items = cargo_items
        self.container = container
        self.num_items = len(cargo_items)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.elite_size = elite_size
        self.stagnation_limit = stagnation_limit
        self.population = []
        self.best_solution = None
        self.best_fitness = float("inf")
        self.best_generation = 0
        self.fitness_history = []

    def _evaluate(self, genome: List[int]) -> tuple:
        """Evaluate a genome and return (genome, solution, fitness)."""
        solution = place_cargo(genome, self.cargo_items, self.container)
        calculate_fitness(solution)
        return (genome, solution, solution.fitness)

    def _update_best(self, solution, fitness, generation: int):
        """Update best solution if fitness improved."""
        if fitness < self.best_fitness:
            self.best_fitness = fitness
            self.best_solution = solution
            self.best_generation = generation
            return True
        return False

    def initialise_population(self):
        for _ in range(self.population_size):
            genome = list(range(self.num_items))
            random.shuffle(genome)
            solution = place_cargo(genome, self.cargo_items, self.container)
            calculate_fitness(solution)
            self.population.append((genome, solution, solution.fitness))

            if solution.fitness < self.best_fitness:
                self.best_fitness = solution.fitness
                self.best_solution = solution
                self.best_generation = 0

    def tournament_selection(self) -> List[int]:
        tournament = random.sample(self.population, self.tournament_size)
        return min(tournament, key=lambda ind: ind[2])[0].copy()

    def order_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        size = len(parent1)
        p1, p2 = sorted(random.sample(range(size), 2))

        child = [-1] * size
        child[p1 : p2 + 1] = parent1[p1 : p2 + 1]

        segment = set(child[p1 : p2 + 1])
        remaining = iter(x for x in parent2 if x not in segment)
        return [next(remaining) if x == -1 else x for x in child]

    def swap_mutation(self, genome: List[int]) -> List[int]:
        if random.random() >= self.mutation_rate:
            return genome
        mutated = genome.copy()
        p1, p2 = random.sample(range(len(mutated)), 2)
        mutated[p1], mutated[p2] = mutated[p2], mutated[p1]
        return mutated

    def evolve_generation(self) -> List:
        # Keep elites
        sorted_pop = sorted(self.population, key=lambda ind: ind[2])
        new_population = sorted_pop[: self.elite_size]

        # Generate offspring
        while len(new_population) < self.population_size:
            parent1, parent2 = self.tournament_selection(), self.tournament_selection()
            child = (
                self.order_crossover(parent1, parent2)
                if random.random() < self.crossover_rate
                else parent1.copy()
            )
            child = self.swap_mutation(child)
            new_population.append(self._evaluate(child))

        return new_population

    def run(self, verbose: bool = False):
        if verbose:
            print(f"\n{'=' * 70}\nGENETIC ALGORITHM\n{'=' * 70}")
            print(
                f"\nPopulation: {self.population_size}, Generations: {self.generations}"
            )
            print(f"Mutation: {self.mutation_rate}, Crossover: {self.crossover_rate}")

        self.initialise_population()
        self.fitness_history.append(self.best_fitness)

        if verbose:
            print(f"\nInitial best fitness: {self.best_fitness:.2f}\n")

        stagnant_count = 0
        original_mutation_rate = self.mutation_rate 

        for gen in range(1, self.generations + 1):
            self.population = self.evolve_generation()

            improved = False

            for genome, solution, fitness in self.population:
                if fitness < self.best_fitness:
                    self.best_fitness = fitness
                    self.best_solution = solution
                    self.best_generation = gen
                    improved = True
                    stagnant_count = 0
                    self.mutation_rate = original_mutation_rate
                    if verbose:
                        print(f"Generation {gen}: New best = {fitness:.2f}")
            
            if not improved:
                stagnant_count += 1
                if stagnant_count >= self.stagnation_limit:
                    if verbose:
                        print(f"\n No improvement for {self.stagnation_limit} generations")
                        print(f"Stopping early at generation {gen}")
                    break

            if stagnant_count > 30:
                # Temporarily increase mutation
                original_mut = self.mutation_rate
                self.mutation_rate = min(0.5, self.mutation_rate * 1.5)
                if verbose and stagnant_count == 21:
                    print(f"  Increasing mutation to {self.mutation_rate:.2f}")
    
            self.fitness_history.append(self.best_fitness)

            if self.best_fitness == 0.0:
                if verbose:
                    print(
                        f"\n{'=' * 70}\n✓ PERFECT SOLUTION FOUND!\nGeneration: {gen}/{self.generations}\n{'=' * 70}"
                    )
                break

            if verbose and gen % 100 == 0:
                avg = sum(ind[2] for ind in self.population) / len(self.population)
                print(f"Generation {gen}: Best={self.best_fitness:.2f}, Avg={avg:.2f}")

        if verbose:
            print(f"\n{'=' * 70}\nEVOLUTION COMPLETE\n{'=' * 70}")
            print(
                f"Best fitness: {self.best_fitness:.2f}\nFound in generation: {self.best_generation}"
            )

        return self.best_solution

    def get_statistics(self) -> dict:
        return {
            "best_fitness": self.best_fitness,
            "best_generation": self.best_generation,
            "generations_run": len(self.fitness_history) - 1,
            "fitness_history": self.fitness_history,
            "population_size": self.population_size,
        }


# VISUALISATION

class CargoVisualiser:
    """Week 7 compatible visualisation"""

    def __init__(self, solution: Solution):
        self.solution = solution
        self.container = solution.container

    def draw(self, title="Cargo Container Loading", show_com=True, show_safe_zone=True):
        """Draw solution using Week 7 visualisation style"""
        fig, ax = plt.subplots(figsize=(12, 10))

        # Draw container rectangle
        container_rect = PltRectangle(
            (0, 0),
            self.container.width,
            self.container.depth,
            fill=False,
            edgecolor="#F4BA02",
            linewidth=3,
            linestyle="-",
            label="Container boundary",
        )
        ax.add_patch(container_rect)

        # Draw safe zone (central 60%)
        if show_safe_zone:
            center_x = self.container.width / 2
            center_y = self.container.depth / 2

            safe_radius = 0.6 * min(self.container.width, self.container.depth) / 2

            safe_circle = PltCircle(
                (center_x, center_y),
                safe_radius,
                fill=False,
                edgecolor="#F4BA02",
                linewidth=2,
                linestyle=":",
                alpha=0.7,
                label="Safe zone (60%)",
            )
            ax.add_patch(safe_circle)

        # Draw cargo items
        for cargo in self.solution.cargo_items:
            if cargo.placed:
                radius = cargo.diameter / 2.0

                # Color based on solution quality
                if self.solution.fitness == 0:
                    edge_color = "#4CAF50"  # Green for perfect
                    fill_color = "#4CAF50"
                else:
                    edge_color = "#99D9DD"  # Blue for searching
                    fill_color = "#99D9DD"

                cargo_patch = PltCircle(
                    (cargo.x, cargo.y),
                    radius,
                    fill=True,
                    facecolor=fill_color,
                    alpha=0.3,
                    edgecolor=edge_color,
                    linewidth=2,
                )
                ax.add_patch(cargo_patch)

                # centre point
                ax.plot(cargo.x, cargo.y, "o", color=edge_color, markersize=6)

                # Label with ID
                ax.text(
                    cargo.x,
                    cargo.y,
                    f"{cargo.id}",
                    ha="center",
                    va="center",
                    color="#F7F8F9",
                    fontsize=11,
                    weight="bold",
                )

                # Weight below
                ax.text(
                    cargo.x,
                    cargo.y + radius + 0.3,
                    f"{int(cargo.weight)}kg",
                    ha="center",
                    va="top",
                    color="#F7F8F9",
                    fontsize=8,
                    style="italic",
                )

        # Draw centre of mass
        if show_com and self.solution.complete:
            com_x, com_y = self.solution.get_center_of_mass()

            # COM marker with crosshair
            ax.plot(
                com_x,
                com_y,
                "x",
                color="#FF0000",
                markersize=15,
                markeredgewidth=3,
                label="center of Mass",
            )

            # Draw reference lines
            ax.plot(
                [com_x, com_x],
                [0, com_y],
                color="#FF0000",
                linewidth=1,
                alpha=0.3,
                linestyle=":",
            )
            ax.plot(
                [0, com_x],
                [com_y, com_y],
                color="#FF0000",
                linewidth=1,
                alpha=0.3,
                linestyle=":",
            )

        # Draw origin marker
        ax.plot(
            0,
            0,
            "x",
            color="#F4BA02",
            markersize=12,
            markeredgewidth=3,
            label="Origin (rear left)",
        )

        # Set up axes
        ax.set_aspect("equal")
        margin = 0.1
        ax.set_xlim(-margin, self.container.width + margin)
        ax.set_ylim(-margin, self.container.depth + margin)

        # Week 7 styling
        ax.grid(True, alpha=0.3, color="#F7F8F9")
        ax.set_facecolor("#01364C")
        fig.patch.set_facecolor("#01364C")
        ax.tick_params(colors="#F7F8F9")
        for spine in ax.spines.values():
            spine.set_color("#F7F8F9")

        # Title with fitness info
        fitness_text = (
            "PERFECT SOLUTION ✓"
            if self.solution.fitness == 0
            else f"Fitness: {self.solution.fitness:.2f}"
        )
        com_x, com_y = self.solution.get_center_of_mass()

        title_text = f"{title}\n{fitness_text} | COM: ({com_x:.2f}, {com_y:.2f})"
        ax.set_title(title_text, color="#F7F8F9", fontsize=14, pad=20, weight="bold")

        ax.legend(
            loc="upper right",
            facecolor="#01364C",
            edgecolor="#F7F8F9",
            labelcolor="#F7F8F9",
            framealpha=0.9,
            fontsize=9,
        )

        ax.set_xlabel("Width (m)", color="#F7F8F9", fontsize=10)
        ax.set_ylabel("Depth (m)", color="#F7F8F9", fontsize=10)

        plt.tight_layout()
        return fig, ax


# INSATNCE LOADER

def get_instance(instance_name: str) -> Tuple[List[Cargo], Container]:
    """Get instance from container_instances.py"""
    from container_instances import create_basic_instances, create_challenging_instances

    all_instances = create_basic_instances() + create_challenging_instances()

    for instance in all_instances:
        if instance.name == instance_name:
            # Create container
            container = Container(
                width=instance.container.width,
                depth=instance.container.depth,
                max_weight=instance.container.max_weight,
            )

            # Create cargo items
            cargo_items = []
            for idx, cyl in enumerate(instance.cylinders):
                cargo = Cargo(id=idx, diameter=cyl.diameter, weight=cyl.weight)
                cargo_items.append(cargo)

            return cargo_items, container

    raise ValueError(f"Instance '{instance_name}' not found")


def list_instances() -> List[str]:
    """List all available instances"""
    from container_instances import create_basic_instances, create_challenging_instances

    instances = create_basic_instances() + create_challenging_instances()
    return [inst.name for inst in instances]


# MENU SYSTEM

def main_menu():
    print("\n" + "=" * 70)
    print("CARGO CONTAINER LOADING - GENETIC ALGORITHM")
    print("KV6018 Evolutionary Computing")
    print("=" * 70)

    while True:
        print("\nAvailable Instances:")
        print("-" * 70)
        instances = list_instances()
        basic = [i for i in instances if "basic" in i]
        challenging = [i for i in instances if "challenge" in i]

        print("\nBASIC:")
        for idx, name in enumerate(basic, 1):
            print(f"  {idx}. {name}")
        print("\nCHALLENGING:")
        for idx, name in enumerate(challenging, len(basic) + 1):
            print(f"  {idx}. {name}")

        print("\n" + "-" * 70)
        choice = input(
            f"\nSelect instance (1-{len(instances)}) or 'q' to quit: "
        ).strip()

        if choice.lower() == "q":
            print("\nGoodbye!")
            break

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(instances):
                instance_name = instances[choice_num - 1]
                cargo_items, container = get_instance(instance_name)

                print(f"\n Loaded: {instance_name}")
                print(
                    f"  Container: {container.width}×{container.depth}m, max {container.max_weight}kg"
                )
                print(f"  Cargo: {len(cargo_items)} items")

                # Run GA with default parameters
                print("\n" + "=" * 70)
                print("RUNNING GENETIC ALGORITHM")
                print("=" * 70)
                print("Parameters: Population=100, Generations=500, Mutation=0.15")

                ga = GeneticAlgorithm(cargo_items, container)
                solution = ga.run(verbose=True)

                print("\n" + "=" * 70)
                print("RESULTS")
                print("=" * 70)
                print(f"\nFitness: {solution.fitness:.2f}")
                print(f"Order: {solution.order}")
                if solution.complete:
                    com_x, com_y = solution.get_center_of_mass()
                    print(f"COM: ({com_x:.2f}, {com_y:.2f})")

                show_vis = input("\nSave visualisation? (y/n): ").strip().lower()
                if show_vis == "y":
                    vis = CargoVisualiser(solution)
                    vis.draw(title=instance_name)
                    
                    # Ensure output directory exists
                    import os
                    os.makedirs('./output', exist_ok=True)
                    
                    filename = f'./output/{instance_name}_fitness_{solution.fitness:.2f}.png'
                    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#01364C')
                    plt.close()

                    print(f"\nVisualisation saved to: {filename}")

                cont = input("\nSolve another? (y/n): ").strip().lower()
                if cont != "y":
                    print("\nGoodbye!")
                    break
            else:
                print(f"Enter 1-{len(instances)}")
        except ValueError:
            print("Invalid input")
        except Exception as e:
            print(f"Error: {e}")
            import traceback

            traceback.print_exc()


# MAIN ENTRY POINT

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
