#!/usr/bin/env python3
# main.py

import random
import math
from typing import List, Tuple, Dict
from dataclasses import dataclass
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as PltCircle
from matplotlib.patches import Rectangle as PltRectangle

# ============================================================================
# DATA STRUCTURES
# ============================================================================

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
