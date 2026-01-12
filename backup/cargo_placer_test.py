from main import Cargo, Container, place_cargo


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