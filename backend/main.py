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
        """Calculate center of mass for placed cargo"""
        placed = [c for c in self.cargo_items if c.placed]
        if not placed:
            return (0, 0)

        total_weight = sum(c.weight for c in placed)
        weighted_x = sum(c.x * c.weight for c in placed)
        weighted_y = sum(c.y * c.weight for c in placed)

        return (weighted_x / total_weight, weighted_y / total_weight)


# CARGO PLACEMENT

# Configuration
GRID_STEP = 0.1  # Position grid resolution (units)


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

        # Try to find a valid position
        position_found = False

        # Scan from back-left (0,0) moving right then forward
        y = 0.0
        while y <= container.depth and not position_found:
            x = 0.0
            while x <= container.width and not position_found:
                # Calculate center position
                center_x = x + radius
                center_y = y + radius

                # Check if this position is valid
                if is_valid_position(
                    center_x, center_y, radius, placed_cargo, container
                ):
                    # Place the cargo here
                    cargo.x = center_x
                    cargo.y = center_y
                    cargo.placed = True
                    placed_cargo.append(cargo)
                    position_found = True

                x += GRID_STEP
            y += GRID_STEP

        # If we couldn't place this cargo item, solution is incomplete
        if not position_found:
            complete = False
            break  # Stop trying to place remaining items

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
PENALTY_UNPLACED = 1000.0  # Per unplaced cargo item
PENALTY_WEIGHT_KG = 10.0  # Per kg over weight limit
PENALTY_COM_DISTANCE = 100.0  # Per unit distance outside safe zone


def calculate_fitness(solution) -> float:
    total_penalty = 0.0
    violations = {}

    # Penalty 1: Unplaced cargo items
    unplaced_count = sum(1 for c in solution.cargo_items if not c.placed)
    if unplaced_count > 0:
        penalty = unplaced_count * PENALTY_UNPLACED
        total_penalty += penalty
        violations["unplaced_items"] = unplaced_count
        violations["unplaced_penalty"] = penalty

    # If solution is incomplete, skip other checks
    if not solution.complete:
        solution.fitness = total_penalty
        solution.violations = violations
        return total_penalty

    # Penalty 2: Weight limit violation
    total_weight = sum(c.weight for c in solution.cargo_items if c.placed)
    if total_weight > solution.container.max_weight:
        excess_weight = total_weight - solution.container.max_weight
        penalty = excess_weight * PENALTY_WEIGHT_KG
        total_penalty += penalty
        violations["excess_weight_kg"] = excess_weight
        violations["weight_penalty"] = penalty

    # Penalty 3: Center of mass outside safe zone
    com_x, com_y = solution.get_center_of_mass()

    # Safe zone is central 60% of container
    safe_x_min = solution.container.width * 0.2
    safe_x_max = solution.container.width * 0.8
    safe_y_min = solution.container.depth * 0.2
    safe_y_max = solution.container.depth * 0.8

    # Calculate distance outside safe zone
    com_violation = 0.0

    if com_x < safe_x_min:
        com_violation += safe_x_min - com_x
    elif com_x > safe_x_max:
        com_violation += com_x - safe_x_max

    if com_y < safe_y_min:
        com_violation += safe_y_min - com_y
    elif com_y > safe_y_max:
        com_violation += com_y - safe_y_max

    if com_violation > 0:
        penalty = com_violation * PENALTY_COM_DISTANCE
        total_penalty += penalty
        violations["com_distance_outside"] = com_violation
        violations["com_penalty"] = penalty
        violations["com_position"] = (com_x, com_y)
        violations["safe_zone"] = {
            "x_range": (safe_x_min, safe_x_max),
            "y_range": (safe_y_min, safe_y_max),
        }

    # Store results in solution object
    solution.fitness = total_penalty
    solution.violations = violations

    return total_penalty


# GENETIC ALGORITHM


class GeneticAlgorithm:
    def __init__(
        self,
        cargo_items: List,
        container,
        population_size: int = 50,
        generations: int = 100,
        mutation_rate: float = 0.2,
    ):
        self.cargo_items = cargo_items
        self.container = container
        self.num_items = len(cargo_items)

        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

        self.population = []
        self.best_solution = None
        self.best_fitness = float("inf")

    def init_population(self):
        from cargo_placement import place_cargo
        from fitness import calculate_fitness

        for _ in range(self.population_size):
            gnome = list(range(slef.num_items))
            random.shuffle(gnome)

            solution = place_cargo(gnome, self.cargo_items, self.container)
            fitness = calculate_fitness(solution)

            self.population.append((gnome, solution, fitness))

            if fitness < self.best.fitness:
                self.best_fitness = fitness
                self.best_solution = solution

    def select_parent(self) -> List[int]:
        individual = random.choice(self.population)
        return individual[0].copy()

    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        size = len(parent1)
        point = random.randint(1, size - 1)

        child = parent1[:point].copy()

        for gene in parent2:
            if gene not in child:
                child.append(gene)

        return child

    def mutate(self, genome: List[int]) -> List[int]:
        """Swap two random positions."""
        if random.random() < self.mutation_rate:
            mutated = genome.copy()
            pos1 = random.randint(0, len(mutated) - 1)
            pos2 = random.randint(0, len(mutated) - 1)
            mutated[pos1], mutated[pos2] = mutated[pos2], mutated[pos1]
            return mutated
        return genome

    def run(self, verbose: bool = False):
        """Run the genetic algorithm."""
        from cargo_placement import place_cargo
        from fitness import calculate_fitness

        if verbose:
            print("\nRunning basic GA...")
            print(
                f"Population: {self.population_size}, Generations: {self.generations}"
            )

        # Initialize
        self.initialize_population()

        if verbose:
            print(f"Initial best fitness: {self.best_fitness:.2f}")

        # Evolution loop
        for generation in range(self.generations):
            new_population = []

            # Create new generation
            for _ in range(self.population_size):
                # Select parents
                parent1 = self.select_parent()
                parent2 = self.select_parent()

                # Create child
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)

                # Evaluate
                solution = place_cargo(child, self.cargo_items, self.container)
                fitness = calculate_fitness(solution)

                new_population.append((child, solution, fitness))

                # Track best
                if fitness < self.best_fitness:
                    self.best_fitness = fitness
                    self.best_solution = solution
                    if verbose:
                        print(f"Generation {generation}: New best = {fitness:.2f}")

            self.population = new_population

            # Early stopping
            if self.best_fitness == 0.0:
                if verbose:
                    print(f"\nPerfect solution found at generation {generation}!")
                break

        if verbose:
            print(f"\nFinal best fitness: {self.best_fitness:.2f}")

        return self.best_solution

    def get_statistics(self) -> dict:
        """Get basic statistics."""
        return {
            "best_fitness": self.best_fitness,
            "population_size": self.population_size,
        }


# VISUALISATION


class CargoVisualizer:
    """Week 7 compatible visualization"""

    def __init__(self, solution: Solution):
        self.solution = solution
        self.container = solution.container

    def draw(self, title="Cargo Container Loading", show_com=True, show_safe_zone=True):
        """Draw solution using Week 7 visualization style"""
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
            safe_x = self.container.width * 0.2
            safe_y = self.container.depth * 0.2
            safe_w = self.container.width * 0.6
            safe_h = self.container.depth * 0.6

            safe_zone = PltRectangle(
                (safe_x, safe_y),
                safe_w,
                safe_h,
                fill=False,
                edgecolor="#4CAF50",
                linewidth=2,
                linestyle="--",
                alpha=0.7,
                label="Safe zone (60%)",
            )
            ax.add_patch(safe_zone)

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

                # Center point
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

        # Draw center of mass
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
                label="Center of Mass",
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
        margin = max(self.container.width, self.container.depth) * 0.1
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
