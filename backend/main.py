import random
import math
from typing import List, Tuple, Dict
from dataclasses import dataclass
from copy import deepcopy
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


def place_cargo(order: List[int], 
                cargo_items: List[Cargo], 
                container: Container) -> Solution:
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
                if is_valid_position(center_x, center_y, radius, 
                                    placed_cargo, container):
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
        container=container
    )
    
    return solution


def is_valid_position(x: float, y: float, radius: float,
                     placed_cargo: List[Cargo],
                     container: Container) -> bool:
    # Check 1: Within container bounds
    if x - radius < 0 or x + radius > container.width:
        return False
    if y - radius < 0 or y + radius > container.depth:
        return False
    
    # Check 2: No overlaps with already-placed cargo
    for placed in placed_cargo:
        distance = math.sqrt((x - placed.x)**2 + (y - placed.y)**2)
        min_distance = radius + (placed.diameter / 2.0)
        
        if distance < min_distance:
            return False  # Overlaps!
    
    # All checks passed
    return True



def test_simple_placement():
    """Test with 3 simple cargo items"""
    
    # Create test cargo
    cargo_items = [
        Cargo(id=0, diameter=2.0, weight=10.0),
        Cargo(id=1, diameter=2.0, weight=10.0),
        Cargo(id=2, diameter=2.0, weight=10.0),
    ]
    
    # Create container
    container = Container(width=10.0, depth=10.0, max_weight=100.0)
    
    # Test order
    order = [0, 1, 2]
    
    # Place cargo
    solution = place_cargo(order, cargo_items, container)
    
    # Check results
    print(f"Complete: {solution.complete}")
    print(f"Placed cargo items:")
    for cargo in solution.cargo_items:
        if cargo.placed:
            print(f"  Cargo {cargo.id}: ({cargo.x:.1f}, {cargo.y:.1f})")
    
    # Expected: All three should place without overlap
    assert solution.complete, "Should place all cargo"
    assert all(c.placed for c in solution.cargo_items), "All should be marked placed"
    
    print("\nTest passed!")


if __name__ == "__main__":
    test_simple_placement()