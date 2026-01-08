#!/usr/bin/env python3
# debug_ga.py
"""Debug GA operators to see what's wrong."""

from main import Cargo, Container, GeneticAlgorithm, calculate_fitness, place_cargo

# Create simple test case
cargo_items = [
    Cargo(0, 3.0, 20.0),
    Cargo(1, 3.0, 20.0),
    Cargo(2, 2.0, 15.0),
    Cargo(3, 2.0, 15.0),
]
container = Container(12.0, 10.0, 150.0)

print("\n" + "=" * 70)
print("DEBUGGING GA OPERATORS")
print("=" * 70)

# Test 1: Do different orders produce different fitnesses?
print("\nTest 1: Testing if order matters...")
orders = [
    [0, 1, 2, 3],
    [3, 2, 1, 0],
    [2, 0, 3, 1],
]

fitness_values = set()
for order in orders:
    sol = place_cargo(order, cargo_items, container)
    calculate_fitness(sol)
    fitness_values.add(sol.fitness)
    print(
        f"  Order {order}: fitness={sol.fitness:.2f}, COM=({sol.get_center_of_mass()[0]:.2f}, {sol.get_center_of_mass()[1]:.2f})"
    )

if len(fitness_values) > 1:
    print(
        f"✓ Different orders produce different fitness! ({len(fitness_values)} unique values)"
    )
else:
    print(f"⚠️  WARNING: All orders produce same fitness = {fitness_values.pop():.2f}")

# Test 2: Check OX produces valid permutations
print("\nTest 2: Testing Order Crossover...")
ga = GeneticAlgorithm(cargo_items, container)

parent1 = [0, 1, 2, 3]
parent2 = [3, 2, 1, 0]

children_different = False
for i in range(5):
    child = ga.order_crossover(parent1, parent2)
    is_valid = sorted(child) == [0, 1, 2, 3]
    different = child not in [parent1, parent2]
    print(f"  Test {i + 1}: child={child}, valid={is_valid}, different={different}")
    if different:
        children_different = True

if children_different:
    print("✓ OX produces different offspring")
else:
    print("⚠️  WARNING: OX always returns same as parent!")

# Test 3: Check mutation works
print("\nTest 3: Testing Swap Mutation...")
genome = [0, 1, 2, 3]
mutations_happened = 0

for i in range(20):
    mutated = ga.swap_mutation(genome)
    if mutated != genome:
        mutations_happened += 1

mutation_rate_observed = mutations_happened / 20
print(f"  Expected mutation rate: {ga.mutation_rate} (15%)")
print(
    f"  Observed mutation rate: {mutation_rate_observed:.2f} ({mutations_happened}/20)"
)

if mutations_happened > 0:
    print(f"✓ Mutation is working")
else:
    print(f"⚠️  WARNING: Mutation never changed genome!")

# Test 4: Check population diversity
print("\nTest 4: Checking initial population diversity...")
ga2 = GeneticAlgorithm(cargo_items, container, population_size=20, generations=10)
ga2.initialize_population()

unique_genomes = set()
unique_fitness = set()

for genome, sol, fit in ga2.population:
    unique_genomes.add(tuple(genome))
    unique_fitness.add(fit)

print(f"  Population size: 20")
print(f"  Unique genomes: {len(unique_genomes)}")
print(f"  Unique fitness values: {len(unique_fitness)}")

if len(unique_genomes) > 1:
    print(f"✓ Population has diversity")
else:
    print(f"⚠️  CRITICAL: All genomes identical!")

if len(unique_fitness) > 1:
    print(f"✓ Different fitness values exist")
else:
    print(f"⚠️  CRITICAL: All fitness identical = {unique_fitness.pop():.2f}")

# Test 5: Run one generation and check if offspring differ
print("\nTest 5: Testing if evolution creates diversity...")
initial_genomes = set(tuple(ind[0]) for ind in ga2.population)
ga2.population = ga2.evolve_generation()
new_genomes = set(tuple(ind[0]) for ind in ga2.population)

genomes_changed = len(new_genomes - initial_genomes)
print(f"  Genomes before evolution: {len(initial_genomes)}")
print(f"  Genomes after evolution: {len(new_genomes)}")
print(f"  New genomes created: {genomes_changed}")

if genomes_changed > 0:
    print(f"✓ Evolution creates new genomes")
else:
    print(f"⚠️  CRITICAL: Evolution creates no new genomes!")

print("\n" + "=" * 70)
print("DEBUG COMPLETE")
print("=" * 70 + "\n")
