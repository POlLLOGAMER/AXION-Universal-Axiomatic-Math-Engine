# AXION — Universal Axiomatic Math Engine

**A modular computer algebra system (CAS) with formal theorem proving capabilities**

AXION is a universal mathematical engine that combines:
- 🧮 **Computer Algebra System** — Symbolic manipulation, calculus, algebra
- 🔬 **Formal Theorem Prover** — Rigorous axiomatic proofs with cryptographic verification
- 📚 **Modular Theory Library** — Clean separation of mathematical domains
- 🔐 **Cryptographic Verification** — SHA-256 hashing of complete proofs

---

## 🏗️ Architecture

```
axion_project/
├── core/                   # Logical inference kernel (domain-independent)
│   ├── inference_kernel.py # Pure inference rules: modus ponens, substitution, etc.
│   └── __init__.py
│
├── axioms/                 # Mathematical theory library
│   ├── axiom_library.py    # Modular axiom collections (ZFC, Peano, Calculus, etc.)
│   └── __init__.py
│
├── solvers/                # Problem-solving strategies
│   ├── universal_solver.py # Theorem proving, symbolic computation
│   └── __init__.py
│
├── session/                # Proof history and verification
│   ├── proof_session.py    # Session management, proof database
│   └── __init__.py
│
├── README.md               # This file
└── AXION_Demo.ipynb        # Interactive Jupyter notebook
```

---

## 🚀 Quick Start

### Installation

No external dependencies required! AXION uses only Python standard library.

```bash
# Clone or download the project
cd axion_project

# Launch Jupyter notebook (recommended)
jupyter notebook AXION_Demo.ipynb

# Or use in Python scripts
python
>>> from solvers.universal_solver import UniversalSolver
>>> solver = UniversalSolver()
```

### Basic Usage

```python
from solvers.universal_solver import UniversalSolver

# Initialize the solver
solver = UniversalSolver()

# 1. SYMBOLIC COMPUTATION (CAS mode)
# Differentiate
result = solver.solve("x^2", using="Calculus", problem_type="differentiate")
print(result)  # Output: 2*x

# Integrate
result = solver.solve("x^2", using="Calculus", problem_type="integrate")
print(result)  # Output: x^3/3

# Simplify
result = solver.solve("x + 0 + x*1", problem_type="simplify")
print(result)  # Output: x + x

# 2. THEOREM PROVING (Formal proof mode)
proof = solver.solve("∀x: x = x", using="Logic", problem_type="prove")
print(proof)
print(f"Proof hash: {proof.proof_hash}")
```

---

## 📖 Step-by-Step Tutorial

### 1️⃣ **List Available Theories**

```python
solver = UniversalSolver()

# See all mathematical theories
theories = solver.list_theories()
print(theories)
# ['Logic', 'Peano', 'ZFC', 'Groups', 'Rings', 'Fields', 
#  'VectorSpaces', 'RealAnalysis', 'Calculus', 'Topology', 
#  'CategoryTheory', 'NumberTheory']
```

### 2️⃣ **Examine Axioms in a Theory**

```python
# Get all axioms from Peano arithmetic
peano_axioms = solver.get_axioms("Peano")

for name, statement in peano_axioms.items():
    print(f"{name}: {statement}")

# Output:
# zero_natural: 0 ∈ ℕ
# successor_natural: ∀n ∈ ℕ: S(n) ∈ ℕ
# zero_not_successor: ∀n ∈ ℕ: S(n) ≠ 0
# ...
```

### 3️⃣ **Solve Problems with Specific Theories**

```python
# Calculus operations
derivative = solver.solve("x^3", using="Calculus", problem_type="differentiate")
print(f"d/dx[x^3] = {derivative}")  # 3*x^2

integral = solver.solve("2*x", using="Calculus", problem_type="integrate")
print(f"∫2x dx = {integral}")  # 2*x^2/2

# Prove theorems in Peano arithmetic
proof = solver.solve("∀n: n + 0 = n", using="Peano", problem_type="prove")
print(proof)
```

### 4️⃣ **Auto-Detection of Problem Types**

```python
# AXION automatically detects what you want to do
solver.solve("x^2")                    # Auto: simplify
solver.solve("d/dx[x^2]")              # Auto: differentiate
solver.solve("∫x dx")                  # Auto: integrate
solver.solve("∀x: x = x")              # Auto: prove
solver.solve("2x + 3 = 7")             # Auto: solve equation
```

### 5️⃣ **Working with Proofs**

```python
from session.proof_session import ProofSession

# Create session to track proofs
session = ProofSession()

# Prove a theorem
proof = solver.solve("∀x: x = x", using="Logic", problem_type="prove")

# Add to session
session.add_proof(proof)

# View statistics
stats = session.statistics()
print(stats)

# Export session
session.export_session("my_proofs.json")
```

---

## 🔧 Adding Custom Axioms

### Method 1: Add Axiom to Existing Theory

```python
solver = UniversalSolver()

# Add a new axiom to Peano theory
solver.add_axiom(
    theory="Peano",
    name="commutativity_addition",
    statement="∀m,n: m + n = n + m"
)

# Verify it was added
peano_axioms = solver.get_axioms("Peano")
print(peano_axioms["commutativity_addition"])
```

### Method 2: Create a New Theory

```python
# Create a custom theory for graph theory
graph_axioms = {
    "graph_def": "G = (V, E) where V is vertex set and E ⊆ V × V",
    "edge_symmetry": "∀u,v: (u,v) ∈ E ⟹ (v,u) ∈ E",
    "no_self_loops": "∀v: (v,v) ∉ E",
    "degree_def": "deg(v) = |{u : (v,u) ∈ E}|"
}

solver.add_theory(
    name="GraphTheory",
    description="Basic undirected graph theory",
    axioms=graph_axioms
)

# Use the new theory
proof = solver.solve("∀v: deg(v) ≥ 0", using="GraphTheory", problem_type="prove")
```

### Method 3: Directly Modify Library

Edit `axioms/axiom_library.py` and add to `_initialize_standard_theories()`:

```python
# In axiom_library.py

# === YOUR NEW THEORY ===
your_theory = AxiomTheory(
    name="YourTheory",
    description="Description of your theory",
    reference="Citation or reference"
)
your_theory.add_axiom("axiom_1", "∀x: P(x)")
your_theory.add_axiom("axiom_2", "∀x,y: R(x,y) ⟹ S(x)")
self.theories["YourTheory"] = your_theory
```

---

## 📋 Category Classification Guide

### How to Choose the Right Theory Category

| **Mathematical Domain** | **Theory Name** | **Use For** |
|------------------------|----------------|------------|
| **Logic** | `Logic` | Propositional logic, quantifiers, basic reasoning |
| **Number Systems** | `Peano` | Natural numbers, arithmetic, induction |
| | `NumberTheory` | Prime numbers, divisibility, GCD |
| **Set Theory** | `ZFC` | Sets, relations, foundations |
| **Abstract Algebra** | `Groups` | Group operations, symmetries |
| | `Rings` | Rings, ideals |
| | `Fields` | Fields, algebraic structures |
| **Linear Algebra** | `VectorSpaces` | Vectors, linear transformations |
| **Analysis** | `RealAnalysis` | Real numbers, limits, continuity |
| | `Calculus` | Derivatives, integrals, differential equations |
| **Topology** | `Topology` | Open sets, continuous functions |
| **Advanced** | `CategoryTheory` | Functors, natural transformations |

### Category Selection Rules

1. **Start with the most specific theory** that contains your concepts
   - For derivatives → use `Calculus`, not `RealAnalysis`
   - For prime numbers → use `NumberTheory`, not `Peano`

2. **Check dependencies**: Some theories build on others
   - `Calculus` requires `RealAnalysis`
   - `Fields` requires `Rings` requires `Groups`

3. **For new domains**, create a new theory:
   ```python
   # Example: Probability Theory
   solver.add_theory(
       name="Probability",
       description="Probability axioms (Kolmogorov)",
       axioms={
           "non_negativity": "∀A: P(A) ≥ 0",
           "normalization": "P(Ω) = 1",
           "additivity": "P(A ∪ B) = P(A) + P(B) if A ∩ B = ∅"
       }
   )
   ```

4. **Avoid mixing unrelated theories** in a single proof
   - Don't use `Topology` axioms in `Peano` proofs
   - Keep theory contexts clean and minimal

---

## 🎯 Examples Gallery

### Example 1: Calculus Operations

```python
solver = UniversalSolver()

# Chain of derivatives
expr = "x^4"
for i in range(4):
    expr = solver.solve(expr, using="Calculus", problem_type="differentiate")
    print(f"Derivative {i+1}: {expr}")

# Output:
# Derivative 1: 4*x^3
# Derivative 2: 12*x^2
# Derivative 3: 24*x
# Derivative 4: 24
```

### Example 2: Formal Proof with Verification

```python
from session.proof_session import ProofSession

solver = UniversalSolver()
session = ProofSession()

# Prove identity axiom
proof = solver.solve("∀x: x = x", using="Logic", problem_type="prove")
session.add_proof(proof)

# Cryptographic verification
print(f"Theorem: {proof.theorem.content}")
print(f"Valid: {proof.is_valid}")
print(f"Proof hash: {proof.proof_hash}")
print(f"Steps: {len(proof.steps)}")
print(f"Axioms used: {proof.axioms_used}")
```

### Example 3: Building a Proof Library

```python
solver = UniversalSolver()
session = ProofSession()

# Prove multiple theorems
theorems = [
    ("∀x: x = x", "Logic"),
    ("∀n: n + 0 = n", "Peano"),
    ("∀x,y: x + y = y + x", "Peano"),
]

for theorem, theory in theorems:
    proof = solver.solve(theorem, using=theory, problem_type="prove")
    session.add_proof(proof)
    print(f"✓ Proved: {theorem}")

# Export all proofs
session.export_session("theorem_library.json")

# View statistics
print(session.statistics())
```

### Example 4: Custom Theory for Linear Algebra

```python
solver = UniversalSolver()

# Define linear algebra axioms
linalg_axioms = {
    "matrix_multiplication": "∀A,B: (AB)ij = Σk Aik·Bkj",
    "identity_matrix": "∀A: AI = IA = A",
    "transpose_property": "∀A,B: (AB)ᵀ = BᵀAᵀ",
    "determinant_product": "∀A,B: det(AB) = det(A)·det(B)"
}

solver.add_theory(
    name="LinearAlgebra",
    description="Matrix operations and linear transformations",
    axioms=linalg_axioms
)

# Use the theory
axioms = solver.get_axioms("LinearAlgebra")
for name, statement in axioms.items():
    print(f"{name}: {statement}")
```

---

## 🔬 Advanced Features

### Proof Validation

```python
from core.inference_kernel import InferenceKernel, Expression, InferenceRule

kernel = InferenceKernel()

# Create a proof manually
proof = kernel.create_proof(Expression("Q"), theory="Logic")

# Add steps
p = Expression("P")
p_implies_q = Expression("P ⟹ Q")

kernel.add_step(proof, p_implies_q, InferenceRule.AXIOM_APPLICATION,
                justification="Assume P ⟹ Q")
kernel.add_step(proof, p, InferenceRule.AXIOM_APPLICATION,
                justification="Assume P")
kernel.add_step(proof, Expression("Q"), InferenceRule.MODUS_PONENS,
                premises=[p_implies_q, p],
                justification="Modus ponens on P and P⟹Q")

# Validate the proof
is_valid = kernel.validate_proof(proof)
print(f"Proof valid: {is_valid}")
print(f"Proof hash: {proof.proof_hash}")
```

### Theory Dependencies

```python
# Some theories depend on others
solver = UniversalSolver()

# Check theory dependencies
theory = solver.library.get_theory("Calculus")
print(f"Theory: {theory.name}")
print(f"Dependencies: {theory.dependencies}")
print(f"Description: {theory.description}")
```

---

## 🛡️ Important Restrictions

### ⚠️ What AXION Does NOT Do

1. **No automatic axiom generation** — All axioms must be explicitly defined
2. **No unproven conjectures as axioms** — Riemann Hypothesis, Hodge Conjecture, BSD, etc. are NOT included
3. **No guessing** — Only formal inference rules are used
4. **No numerical approximation** — This is symbolic mathematics only

### ✅ Consistency Guarantees

- All axioms are from established mathematical literature
- Proof steps use only valid inference rules
- Every proof has a cryptographic hash for verification
- No circular reasoning — dependency tracking prevents axiom conflicts

---

## 📚 Theory Reference

### Available Theories (Default)

| Theory | Axiom Count | Description |
|--------|-------------|-------------|
| Logic | 4 | Classical first-order logic |
| Peano | 9 | Natural numbers and arithmetic |
| ZFC | 9 | Zermelo-Fraenkel set theory + Choice |
| Groups | 4 | Abstract group axioms |
| Rings | 5 | Ring theory |
| Fields | 3 | Field theory |
| VectorSpaces | 6 | Vector spaces over fields |
| RealAnalysis | 3 | Real number system |
| Calculus | 9 | Derivatives and integrals |
| Topology | 3 | Topological spaces |
| CategoryTheory | 4 | Categories and functors |
| NumberTheory | 3 | Elementary number theory |

---

## 🧪 Testing AXION

```python
# Run a comprehensive test suite
solver = UniversalSolver()

# Test 1: List all theories
print("Available theories:", solver.list_theories())

# Test 2: Test each problem type
tests = [
    ("x^2", "differentiate", "Calculus"),
    ("x", "integrate", "Calculus"),
    ("x + 0", "simplify", "Logic"),
    ("∀x: x = x", "prove", "Logic"),
]

for problem, ptype, theory in tests:
    result = solver.solve(problem, using=theory, problem_type=ptype)
    print(f"{ptype}({problem}) = {result}")

# Test 3: Session management
from session.proof_session import ProofSession
session = ProofSession()
proof = solver.solve("∀x: x = x", using="Logic", problem_type="prove")
session.add_proof(proof)
print("Session stats:", session.statistics())
```

---

## 🤝 Contributing

### Adding New Axioms

1. Determine the correct theory category (see classification guide above)
2. Add axiom using `solver.add_axiom()` or edit `axiom_library.py`
3. Document the axiom with proper mathematical notation
4. Include citation/reference if from literature

### Adding New Inference Rules

Edit `core/inference_kernel.py`:

```python
def your_new_rule(self, expr1: Expression, expr2: Expression) -> Optional[Expression]:
    """
    Your inference rule documentation
    """
    # Implementation
    pass
```

### Adding New Solvers

Edit `solvers/universal_solver.py` or create new strategy class:

```python
class YourSolver(SolverStrategy):
    def solve(self, problem: str, theory: str = "Logic") -> Any:
        # Your solving strategy
        pass
```

---

## 📖 Mathematical Notation Guide

| Symbol | Meaning | LaTeX | Usage |
|--------|---------|-------|-------|
| ∀ | For all | `\forall` | `∀x: P(x)` |
| ∃ | Exists | `\exists` | `∃x: P(x)` |
| ∧ | And | `\land` | `P ∧ Q` |
| ∨ | Or | `\lor` | `P ∨ Q` |
| ⟹ | Implies | `\implies` | `P ⟹ Q` |
| ⟺ | If and only if | `\iff` | `P ⟺ Q` |
| ¬ | Not | `\neg` | `¬P` |
| ∈ | Element of | `\in` | `x ∈ A` |
| ⊆ | Subset | `\subseteq` | `A ⊆ B` |
| ∅ | Empty set | `\emptyset` | `∅` |
| ℕ | Natural numbers | `\mathbb{N}` | `n ∈ ℕ` |
| ℤ | Integers | `\mathbb{Z}` | `n ∈ ℤ` |
| ℝ | Real numbers | `\mathbb{R}` | `x ∈ ℝ` |

---

## 🎓 Learning Resources

### Understanding AXION's Architecture

1. **Kernel** (`core/`) — Pure logic, no math knowledge
   - Implements inference rules (modus ponens, substitution, etc.)
   - Validates proof steps
   - Manages proof objects

2. **Axioms** (`axioms/`) — Mathematical knowledge base
   - Collections of axioms for each theory
   - Modular and independent
   - Based on established literature

3. **Solvers** (`solvers/`) — Problem-solving strategies
   - Theorem proving (forward/backward chaining)
   - Symbolic manipulation (CAS functionality)
   - Auto-detection of problem types

4. **Session** (`session/`) — Proof management
   - Tracks all proofs and theorems
   - Cryptographic verification
   - Export/import functionality

### Recommended Workflow

1. **Start simple**: Use built-in theories and auto-detection
2. **Explore axioms**: Understand what axioms are available
3. **Build proofs**: Use theorem prover for formal verification
4. **Extend**: Add custom axioms for your domain
5. **Verify**: Always check proof hashes and validity

---

## 📄 License

AXION is released under MIT License.

---

## 🙋 FAQ

**Q: Can AXION solve the Millennium Problems?**
A: AXION is a universal solver architecture.
Its goal is not to search blindly for proofs but to formalize the entire mathematical universe so that the proofs become derivable.

AXION doesn’t guess proofs —
it derives them from axioms using inference rules.

Once the Millennium Problems are fully encoded as formal theories inside AXION, the system can:

expand axioms,

apply inference,

generate proof trees,

verify correctness automatically.

Thus, their resolution becomes a matter of definition completion, not feasibility.

**Q: Why are Hodge Conjecture / Riemann Hypothesis not included as axioms?**  
A: These are *unproven conjectures*. AXION only includes accepted axioms from established mathematics.

**Q: Can I add numerical computation (like NumPy)?**  
A: AXION focuses on *symbolic* mathematics. For numerical work, integrate with NumPy/SciPy separately.

**Q: How do I cite AXION?**  
A: AXION is a proof-of-concept universal math engine. Each proof includes axiom citations and cryptographic hashes for verification.

**Q: Can AXION replace Coq / Lean / Isabelle?**  
A: No. AXION is a lightweight educational/research tool. Industrial proof assistants have much more sophisticated type systems and tactics.

---

## 🚀 Next Steps

1. Open `AXION_Demo.ipynb` for interactive examples
2. Try proving simple theorems in different theories
3. Add your own axioms and theories
4. Build a proof library for your research domain
5. Explore the source code in `core/`, `axioms/`, `solvers/`

---

**AXION — Universal Axiomatic Math Engine**  
*Where formal proofs meet symbolic computation* 🎯
