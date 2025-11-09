"""
AXION Custom Theory Example
Demonstrates how to create and use custom mathematical theories
"""

import sys
sys.path.append('..')

from solvers.universal_solver import UniversalSolver
from axioms.axiom_library import AxiomTheory

def example_1_add_axiom_to_existing_theory():
    """Example 1: Add an axiom to an existing theory"""
    print("=" * 70)
    print("EXAMPLE 1: Adding Axiom to Existing Theory")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    # Add commutativity axiom to Peano arithmetic
    solver.add_axiom(
        theory="Peano",
        name="commutativity_multiplication",
        statement="∀m,n ∈ ℕ: m × n = n × m"
    )
    
    print("\n✓ Added commutativity_multiplication to Peano")
    
    # Verify it was added
    peano_axioms = solver.get_axioms("Peano")
    print(f"\nPeano now has {len(peano_axioms)} axioms")
    print(f"\nNew axiom:")
    print(f"  {peano_axioms['commutativity_multiplication']}")

def example_2_create_probability_theory():
    """Example 2: Create a probability theory from scratch"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Creating Probability Theory (Kolmogorov Axioms)")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    # Define Kolmogorov axioms for probability
    probability_axioms = {
        "non_negativity": "∀A ⊆ Ω: P(A) ≥ 0",
        "normalization": "P(Ω) = 1",
        "additivity": "∀A,B ⊆ Ω: A ∩ B = ∅ ⟹ P(A ∪ B) = P(A) + P(B)",
        "monotonicity": "∀A,B ⊆ Ω: A ⊆ B ⟹ P(A) ≤ P(B)",
        "complement": "∀A ⊆ Ω: P(Ā) = 1 - P(A)",
    }
    
    solver.add_theory(
        name="Probability",
        description="Kolmogorov probability axioms",
        axioms=probability_axioms
    )
    
    print("\n✓ Created Probability theory")
    print("\nAxioms:")
    for name, statement in probability_axioms.items():
        print(f"  {name}: {statement}")
    
    # Verify it's available
    theories = solver.list_theories()
    print(f"\n✓ Probability is now in theory list: {'Probability' in theories}")

def example_3_create_graph_theory():
    """Example 3: Create a graph theory"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Creating Graph Theory")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    graph_axioms = {
        "graph_def": "G = (V, E) where V is vertex set and E ⊆ V × V",
        "edge_symmetry": "∀u,v ∈ V: (u,v) ∈ E ⟹ (v,u) ∈ E",
        "no_self_loops": "∀v ∈ V: (v,v) ∉ E",
        "degree_def": "∀v ∈ V: deg(v) = |{u ∈ V : (v,u) ∈ E}|",
        "handshaking_lemma": "Σ_{v∈V} deg(v) = 2|E|",
        "path_def": "Path from u to v: sequence of vertices u=v₀,v₁,...,vₙ=v with (vᵢ,vᵢ₊₁) ∈ E",
        "connectivity": "G connected ⟺ ∀u,v ∈ V: ∃ path from u to v",
    }
    
    solver.add_theory(
        name="GraphTheory",
        description="Undirected simple graph theory",
        axioms=graph_axioms
    )
    
    print("\n✓ Created GraphTheory")
    print(f"\nTheory has {len(graph_axioms)} axioms:")
    for name, statement in graph_axioms.items():
        print(f"\n  {name}:")
        print(f"    {statement}")

def example_4_create_linear_algebra():
    """Example 4: Create a linear algebra theory"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Creating Linear Algebra Theory")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    linalg_axioms = {
        "matrix_def": "Matrix A ∈ ℝᵐˣⁿ is m×n array of real numbers",
        "matrix_addition": "∀A,B ∈ ℝᵐˣⁿ: (A+B)ᵢⱼ = Aᵢⱼ + Bᵢⱼ",
        "matrix_multiplication": "∀A ∈ ℝᵐˣⁿ, B ∈ ℝⁿˣᵖ: (AB)ᵢⱼ = Σₖ Aᵢₖ·Bₖⱼ",
        "identity_matrix": "∀A ∈ ℝⁿˣⁿ: AI = IA = A where I is n×n identity",
        "transpose_def": "∀A ∈ ℝᵐˣⁿ: (Aᵀ)ᵢⱼ = Aⱼᵢ",
        "transpose_product": "∀A,B: (AB)ᵀ = BᵀAᵀ",
        "determinant_product": "∀A,B ∈ ℝⁿˣⁿ: det(AB) = det(A)·det(B)",
        "invertible_def": "A invertible ⟺ ∃A⁻¹: AA⁻¹ = A⁻¹A = I",
        "rank_def": "rank(A) = dimension of column space of A",
        "eigenvalue_def": "λ is eigenvalue of A ⟺ ∃v≠0: Av = λv",
    }
    
    solver.add_theory(
        name="LinearAlgebra",
        description="Matrix operations and linear transformations",
        axioms=linalg_axioms
    )
    
    print("\n✓ Created LinearAlgebra theory")
    print(f"\nAxiom count: {len(linalg_axioms)}")
    print("\nSample axioms:")
    for name in ["matrix_multiplication", "determinant_product", "eigenvalue_def"]:
        print(f"  {name}: {linalg_axioms[name]}")

def example_5_create_differential_equations():
    """Example 5: Create a differential equations theory"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Creating Differential Equations Theory")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    de_axioms = {
        "ode_def": "ODE: F(x, y, y', y'', ..., y⁽ⁿ⁾) = 0",
        "first_order_linear": "y' + p(x)y = q(x)",
        "separable": "dy/dx = f(x)g(y) ⟹ ∫dy/g(y) = ∫f(x)dx",
        "existence_uniqueness": "y' = f(x,y), y(x₀) = y₀ has unique solution if f is Lipschitz",
        "linear_superposition": "If y₁, y₂ solve homogeneous linear ODE, then c₁y₁ + c₂y₂ also solves it",
        "variation_of_parameters": "Particular solution via y_p = u₁y₁ + u₂y₂",
        "characteristic_equation": "For y'' + ay' + by = 0, solve r² + ar + b = 0",
    }
    
    solver.add_theory(
        name="DifferentialEquations",
        description="Ordinary differential equations",
        axioms=de_axioms
    )
    
    print("\n✓ Created DifferentialEquations theory")
    print("\nAxioms:")
    for name, statement in de_axioms.items():
        print(f"  {name}: {statement}")

def example_6_direct_library_modification():
    """Example 6: Directly modify axiom_library.py (template)"""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Template for Modifying axiom_library.py")
    print("=" * 70)
    
    template = '''
# Add this to axioms/axiom_library.py in _initialize_standard_theories():

# === YOUR THEORY NAME ===
your_theory = AxiomTheory(
    name="YourTheoryName",
    description="Brief description of your theory",
    dependencies={"DependentTheory1", "DependentTheory2"},  # Optional
    reference="Citation or source reference"
)
your_theory.add_axiom("axiom_1_name", "∀x: P(x)")
your_theory.add_axiom("axiom_2_name", "∀x,y: R(x,y) ⟹ S(x)")
your_theory.add_axiom("axiom_3_name", "Definition or theorem statement")
self.theories["YourTheoryName"] = your_theory
'''
    
    print("\nTo add a theory permanently, edit axiom_library.py:")
    print(template)
    
    print("\n" + "=" * 70)
    print("CATEGORY CLASSIFICATION:")
    print("=" * 70)
    print("""
    Logic & Foundations → Logic, ZFC
    Number Theory       → Peano, NumberTheory
    Algebra            → Groups, Rings, Fields, VectorSpaces
    Analysis           → RealAnalysis, Calculus
    Topology           → Topology
    Advanced           → CategoryTheory
    Custom Domains     → Create new theory with dependencies
    """)

def run_all_examples():
    """Run all examples"""
    example_1_add_axiom_to_existing_theory()
    example_2_create_probability_theory()
    example_3_create_graph_theory()
    example_4_create_linear_algebra()
    example_5_create_differential_equations()
    example_6_direct_library_modification()
    
    print("\n" + "=" * 70)
    print("✓ All examples completed!")
    print("=" * 70)

if __name__ == "__main__":
    run_all_examples()
