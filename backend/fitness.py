from typing import Dict, Tuple
from main import Solution

# Penalty weights
PENALTY_UNPLACED = 1000.0      # Per unplaced cargo item
PENALTY_WEIGHT = 10.0           # Per kg over limit
PENALTY_COM = 100.0             # Per unit distance outside safe zone

def calculate_fitness(solution: Solution) -> Tuple[float, Dict[str, float]]:
    """
    Evaluate solution quality and return fitness score.
    
    Args:
        solution: Solution object with placed cargo
        
    Returns:
        Tuple of (fitness_score, violations_dict)
        - fitness_score: 0.0 = perfect, higher = worse
        - violations_dict: Details of what constraints were violated
    """
    fitness = 0.0
    violations = {}
    
    # Check 1: All cargo placed?
    unplaced_count = sum(1 for c in solution.cargo_items if not c.placed)
    if unplaced_count > 0:
        fitness += unplaced_count * PENALTY_UNPLACED
        violations['unplaced'] = unplaced_count
        # If cargo can't be placed, other checks are meaningless
        return fitness, violations
    
    # Check 2: Total weight within limit?
    total_weight = sum(c.weight for c in solution.cargo_items if c.placed)
    if total_weight > solution.container.max_weight:
        excess_weight = total_weight - solution.container.max_weight
        fitness += excess_weight * PENALTY_WEIGHT
        violations['weight_excess'] = excess_weight
    
    # Check 3: Center of mass in safe zone?
    com_x, com_y = solution.get_center_of_mass()
    
    # Calculate safe zone boundaries (central 60%)
    safe_x_min = solution.container.width * 0.2
    safe_x_max = solution.container.width * 0.8
    safe_y_min = solution.container.depth * 0.2
    safe_y_max = solution.container.depth * 0.8
    
    # Calculate distance from safe zone (0 if inside)
    com_violation = 0.0
    
    if com_x < safe_x_min:
        com_violation += (safe_x_min - com_x)
    elif com_x > safe_x_max:
        com_violation += (com_x - safe_x_max)
    
    if com_y < safe_y_min:
        com_violation += (safe_y_min - com_y)
    elif com_y > safe_y_max:
        com_violation += (com_y - safe_y_max)
    
    if com_violation > 0:
        fitness += com_violation * PENALTY_COM
        violations['com_violation'] = com_violation
    
    return fitness, violations

