# load json
# allow user to pick algorithm
# greedy/ GA ect
# placement algorithm
# run selected algorithm
# output results

import random
import math
import time
import json
import sys
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as PltCircle
from matplotlib.patches import Rectangle as PltRectangle

# ============================================================================
# PROBLEM DEFINITION
# ============================================================================

@dataclass
class Cargo:
    id: int
    diameter: float
    weight: float
    x: float = 0.0
    y: float = 0.0
    placed: bool = False

@dataclass
class Container:
    width: float
    depth: float
    max_weight: float

@dataclass
class Solution:
    order: List[int]
    cargo_items: List[Cargo]
    complete: bool
    fitness: float
    violations: Dict[str, float]
    container: Container
    
    def get_center_of_mass(self) -> Tuple[float, float]:
        placed = [c for c in self.cargo_items if c.placed]
        if not placed:
            return (0, 0)
        
        total_weight = sum(c.weight for c in placed)
        weighted_x = sum(c.x * c.weight for c in placed)
        weighted_y = sum(c.y * c.weight for c in placed)
        
        return (weighted_x / total_weight, weighted_y / total_weight)
