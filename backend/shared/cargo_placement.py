# placement.py
"""
Bottom-left placement heuristic for cargo packing.
Used by all algorithms to convert genome (order) into positions.
"""

import math
from typing import List, Tuple
from copy import deepcopy
from main import Cargo, Container, Solution

# Configuration
GRID_STEP = 0.1  # Position grid resolution (units)


def place_cargo(order: List[int], 
                cargo_items: List[Cargo], 
                container: Container) -> Solution:
    """
    Place cargo items using bottom-left heuristic.
    
    Args:
        order: List of cargo IDs in placement order [0,1,2,...]
        cargo_items: List of Cargo objects (unplaced)
        container: Container with dimensions and weight limit
        
    Returns:
        Solution object with placed cargo and fitness
    """
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
    """
    Check if a cargo item can be placed at position (x, y).
    
    Args:
        x, y: Center coordinates of cargo item
        radius: Radius of cargo item to place
        placed_cargo: List of already-placed cargo items
        container: Container dimensions
        
    Returns:
        True if position is valid (no overlaps, within bounds)
    """
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