# AXION — Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Navigate to Project
```bash
cd axion_project
```

### Step 2: Launch Jupyter Notebook (Recommended)
```bash
jupyter notebook AXION_Demo.ipynb
```

### Step 3: OR Use Python Directly
```python
from solvers.universal_solver import UniversalSolver

solver = UniversalSolver()

# Differentiate
print(solver.solve("x^2", using="Calculus", problem_type="differentiate"))
# Output: 2*x

# Integrate
print(solver.solve("x^2", using="Calculus", problem_type="integrate"))
# Output: x^3/3

# Prove theorem
proof = solver.solve("∀x: x = x", using="Logic", problem_type="prove")
print(f"Valid: {proof.is_valid}, Hash: {proof.proof_hash}")
```

## 📚 File Structure

```
axion_project/
├── core/                   # Logical inference kernel
│   └── inference_kernel.py # Pure inference rules
├── axioms/                 # Mathematical theories
│   └── axiom_library.py    # 12 standard theories
├── solvers/                # Problem solving
│   └── universal_solver.py # CAS + theorem prover
├── session/                # Proof management
│   └── proof_session.py    # History & verification
├── examples/               # Usage examples
│   ├── custom_theory_example.py
│   └── test_suite.py
├── AXION_Demo.ipynb        # Interactive tutorial
├── README.md               # Full documentation
└── CONTRIBUTING.md         # Contribution guide
```

## 🎯 Common Tasks

### List Available Theories
```python
solver = UniversalSolver()
print(solver.list_theories())
# ['Logic', 'Peano', 'ZFC', 'Groups', 'Rings', 'Fields', ...]
```

### Get Axioms from a Theory
```python
axioms = solver.get_axioms("Peano")
for name, statement in axioms.items():
    print(f"{name}: {statement}")
```

### Add Custom Axiom
```python
solver.add_axiom("Peano", "commutativity", "∀m,n: m+n = n+m")
```

### Create New Theory
```python
solver.add_theory(
    name="GraphTheory",
    description="Graph theory axioms",
    axioms={
        "graph_def": "G = (V, E)",
        "degree": "deg(v) = |{u : (v,u) ∈ E}|"
    }
)
```

### Run Tests
```bash
cd examples
python test_suite.py
```

### Run Examples
```bash
cd examples
python custom_theory_example.py
```

## 📖 Next Steps

1. **Read README.md** — Complete documentation
2. **Open AXION_Demo.ipynb** — Interactive tutorial
3. **Run test_suite.py** — Verify installation
4. **Read CONTRIBUTING.md** — Add your own theories

## 🆘 Quick Help

**Problem**: Import errors
**Solution**: Make sure you're in the project directory

**Problem**: Want to add axioms permanently
**Solution**: Edit `axioms/axiom_library.py`

**Problem**: Want to understand the architecture
**Solution**: Read README.md section "Architecture"

**Problem**: Want to contribute
**Solution**: Read CONTRIBUTING.md

## 🎓 Learning Path

1. **Beginner**: Use AXION_Demo.ipynb
2. **Intermediate**: Run custom_theory_example.py
3. **Advanced**: Read source code in core/, axioms/, solvers/
4. **Expert**: Contribute new theories and solvers

---

**AXION — Where formal proofs meet symbolic computation** 🎯
