# Cargo Container Loading - Genetic Algorithm

**KV6018 Evolutionary Computing Assessment**

---

## Quick start

### 1. Files Needed

```
backend/
├── main.py
└── container_instances.py
└── genetic_cargo.py
└── randon_cargo.py
└── greedy_cargo.py
└── locacl_search.py
└── grid_refinement.py
└── run_all_instances,py
└── requirements.py
```

### 2. Install Dependencies

```
pip install matplotlib
pip install numpy
```

### 3. Run

```
cd backend/
python main.py
```

## Usage

### Select Instance

```
Available Instances:

BASIC:
  1. basic_01_three_identical
  2. basic_02_two_sizes
  3. basic_03_varied_sizes

CHALLENGING:
  4. challenge_01_tight_packing
  5. challenge_02_weight_balance
  6. challenge_03_many_small
  7. challenge_04_mixed_constraints

Select instance (1-7) or 'q' to quit: 1
```

### Select Algorithm

```
 Loaded: basic_01_three_identical
  Container: 10.0×10.0m, max 100.0kg
  Cargo: 3 items

Select Algorithm:
  1. Genetic Algorithm (GA)
  2. Random Search
  3. Greedy Seach
```

---

## 📊 Parameters

The GA uses these fixed parameters:

- **Population:**
- **Generations:**
- **Mutation Rate:**
- **Crossover Rate:**
- **Tournament Size:**
- **Elite Size:**

---

## Expected Results

The GA should solve:

- **All basic instances** to fitness = 0.0
- **Most challenging instances** to fitness = 0.0

Typical solve time: 10-60 seconds depending on instance complexity.

---

---

## Visualization

Week 7 compatible styling:

- **Yellow** - Container boundary
- **Green** - Safe zone & perfect solutions
- **Blue** - Sub-optimal solutions
- **Red** - Center of mass marker

**Results for all instances are kept in results.xlsx in /output**

---

## Troubleshooting

**Error: "No module named 'container_instances'"**

- Make sure both files are in the same directory

**Error: "No module named 'matplotlib'"**

- Run: `pip install matplotlib`

**No visualization showing**

- Type `y` when asked "Show visualization? (y/n):"

---
