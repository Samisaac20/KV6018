# fitness.py
"""
Fitness evaluation for cargo container loading solutions.
Lower fitness = better. Perfect solution has fitness = 0.0
"""

# Penalty weights
PENALTY_UNPLACED = 1000.0      # Per unplaced cargo item
PENALTY_WEIGHT_KG = 10.0       # Per kg over weight limit
PENALTY_COM_DISTANCE = 100.0   # Per unit distance outside safe zone


def calculate_fitness(solution) -> float:

    total_penalty = 0.0
    violations = {}
    
    # Penalty 1: Unplaced cargo items
    unplaced_count = sum(1 for c in solution.cargo_items if not c.placed)
    if unplaced_count > 0:
        penalty = unplaced_count * PENALTY_UNPLACED
        total_penalty += penalty
        violations['unplaced_items'] = unplaced_count
        violations['unplaced_penalty'] = penalty
    
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
        violations['excess_weight_kg'] = excess_weight
        violations['weight_penalty'] = penalty
    
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
        com_violation += (safe_x_min - com_x)
    elif com_x > safe_x_max:
        com_violation += (com_x - safe_x_max)
    
    if com_y < safe_y_min:
        com_violation += (safe_y_min - com_y)
    elif com_y > safe_y_max:
        com_violation += (com_y - safe_y_max)
    
    if com_violation > 0:
        penalty = com_violation * PENALTY_COM_DISTANCE
        total_penalty += penalty
        violations['com_distance_outside'] = com_violation
        violations['com_penalty'] = penalty
        violations['com_position'] = (com_x, com_y)
        violations['safe_zone'] = {
            'x_range': (safe_x_min, safe_x_max),
            'y_range': (safe_y_min, safe_y_max)
        }
    
    # Store results in solution object
    solution.fitness = total_penalty
    solution.violations = violations
    
    return total_penalty