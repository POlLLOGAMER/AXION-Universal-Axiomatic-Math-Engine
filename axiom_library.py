"""
AXION Axiom Library
Modular collections of axioms from various mathematical theories
Each theory is independent and can be loaded separately
"""

from typing import Dict, List, Set
from dataclasses import dataclass, field

@dataclass
class AxiomTheory:
    """A collection of axioms for a mathematical theory"""
    name: str
    description: str
    axioms: Dict[str, str] = field(default_factory=dict)
    dependencies: Set[str] = field(default_factory=set)
    reference: str = ""
    
    def add_axiom(self, name: str, statement: str):
        """Add an axiom to this theory"""
        self.axioms[name] = statement
    
    def get_axiom(self, name: str) -> str:
        """Retrieve axiom by name"""
        return self.axioms.get(name, "")
    
    def list_axioms(self) -> List[str]:
        """List all axiom names"""
        return list(self.axioms.keys())

class AxiomLibrary:
    """Central repository for all mathematical theories"""
    
    def __init__(self):
        self.theories: Dict[str, AxiomTheory] = {}
        self._initialize_standard_theories()
    
    def _initialize_standard_theories(self):
        """Load standard mathematical theories"""
        
        # === LOGIC ===
        logic = AxiomTheory(
            name="Logic",
            description="Classical first-order logic",
            reference="Standard logical axioms"
        )
        logic.add_axiom("excluded_middle", "∀P: P ∨ ¬P")
        logic.add_axiom("non_contradiction", "∀P: ¬(P ∧ ¬P)")
        logic.add_axiom("identity", "∀x: x = x")
        logic.add_axiom("leibniz_equality", "∀x,y: (x = y) ⟹ (∀P: P(x) ⟺ P(y))")
        self.theories["Logic"] = logic
        
        # === PEANO ARITHMETIC ===
        peano = AxiomTheory(
            name="Peano",
            description="Natural number arithmetic",
            reference="Peano (1889), Axioms for natural numbers"
        )
        peano.add_axiom("zero_natural", "0 ∈ ℕ")
        peano.add_axiom("successor_natural", "∀n ∈ ℕ: S(n) ∈ ℕ")
        peano.add_axiom("zero_not_successor", "∀n ∈ ℕ: S(n) ≠ 0")
        peano.add_axiom("successor_injective", "∀m,n ∈ ℕ: S(m) = S(n) ⟹ m = n")
        peano.add_axiom("induction", "∀P: [P(0) ∧ (∀n: P(n) ⟹ P(S(n)))] ⟹ ∀n: P(n)")
        peano.add_axiom("addition_zero", "∀n: n + 0 = n")
        peano.add_axiom("addition_successor", "∀m,n: m + S(n) = S(m + n)")
        peano.add_axiom("multiplication_zero", "∀n: n × 0 = 0")
        peano.add_axiom("multiplication_successor", "∀m,n: m × S(n) = m × n + m")
        self.theories["Peano"] = peano
        
        # === ZFC SET THEORY ===
        zfc = AxiomTheory(
            name="ZFC",
            description="Zermelo-Fraenkel Set Theory with Choice",
            reference="Standard ZFC axioms"
        )
        zfc.add_axiom("extensionality", "∀A,B: (∀x: x ∈ A ⟺ x ∈ B) ⟹ A = B")
        zfc.add_axiom("empty_set", "∃∅: ∀x: x ∉ ∅")
        zfc.add_axiom("pairing", "∀a,b: ∃P: ∀x: x ∈ P ⟺ (x = a ∨ x = b)")
        zfc.add_axiom("union", "∀F: ∃U: ∀x: x ∈ U ⟺ ∃A ∈ F: x ∈ A")
        zfc.add_axiom("power_set", "∀A: ∃P: ∀B: B ∈ P ⟺ B ⊆ A")
        zfc.add_axiom("infinity", "∃I: ∅ ∈ I ∧ (∀x ∈ I: x ∪ {x} ∈ I)")
        zfc.add_axiom("replacement", "∀A: ∀F: ∃B: ∀y: y ∈ B ⟺ ∃x ∈ A: F(x) = y")
        zfc.add_axiom("regularity", "∀A: A ≠ ∅ ⟹ ∃x ∈ A: x ∩ A = ∅")
        zfc.add_axiom("choice", "∀F: (∀A ∈ F: A ≠ ∅) ⟹ ∃f: ∀A ∈ F: f(A) ∈ A")
        self.theories["ZFC"] = zfc
        
        # === GROUP THEORY ===
        groups = AxiomTheory(
            name="Groups",
            description="Abstract group theory",
            reference="Standard group axioms"
        )
        groups.add_axiom("closure", "∀a,b ∈ G: a · b ∈ G")
        groups.add_axiom("associativity", "∀a,b,c ∈ G: (a · b) · c = a · (b · c)")
        groups.add_axiom("identity", "∃e ∈ G: ∀a ∈ G: e · a = a · e = a")
        groups.add_axiom("inverse", "∀a ∈ G: ∃a⁻¹ ∈ G: a · a⁻¹ = a⁻¹ · a = e")
        self.theories["Groups"] = groups
        
        # === RING THEORY ===
        rings = AxiomTheory(
            name="Rings",
            description="Ring theory axioms",
            dependencies={"Groups"},
            reference="Standard ring axioms"
        )
        rings.add_axiom("additive_group", "(R, +) is an abelian group")
        rings.add_axiom("multiplicative_closure", "∀a,b ∈ R: a × b ∈ R")
        rings.add_axiom("multiplicative_associativity", "∀a,b,c ∈ R: (a × b) × c = a × (b × c)")
        rings.add_axiom("distributivity_left", "∀a,b,c ∈ R: a × (b + c) = a × b + a × c")
        rings.add_axiom("distributivity_right", "∀a,b,c ∈ R: (a + b) × c = a × c + b × c")
        self.theories["Rings"] = rings
        
        # === FIELD THEORY ===
        fields = AxiomTheory(
            name="Fields",
            description="Field theory axioms",
            dependencies={"Rings"},
            reference="Standard field axioms"
        )
        fields.add_axiom("ring", "(F, +, ×) is a commutative ring")
        fields.add_axiom("multiplicative_identity", "∃1 ∈ F: 1 ≠ 0 ∧ ∀a ∈ F: 1 × a = a")
        fields.add_axiom("multiplicative_inverse", "∀a ∈ F \\{0}: ∃a⁻¹ ∈ F: a × a⁻¹ = 1")
        self.theories["Fields"] = fields
        
        # === VECTOR SPACES ===
        vector_spaces = AxiomTheory(
            name="VectorSpaces",
            description="Vector space axioms over a field",
            dependencies={"Fields"},
            reference="Standard vector space axioms"
        )
        vector_spaces.add_axiom("additive_group", "(V, +) is an abelian group")
        vector_spaces.add_axiom("scalar_multiplication", "∀c ∈ F, v ∈ V: c · v ∈ V")
        vector_spaces.add_axiom("scalar_distributivity", "∀c ∈ F, u,v ∈ V: c · (u + v) = c · u + c · v")
        vector_spaces.add_axiom("field_distributivity", "∀c,d ∈ F, v ∈ V: (c + d) · v = c · v + d · v")
        vector_spaces.add_axiom("scalar_associativity", "∀c,d ∈ F, v ∈ V: (c × d) · v = c · (d · v)")
        vector_spaces.add_axiom("scalar_identity", "∀v ∈ V: 1 · v = v")
        self.theories["VectorSpaces"] = vector_spaces
        
        # === REAL ANALYSIS ===
        real_analysis = AxiomTheory(
            name="RealAnalysis",
            description="Real number system and analysis",
            dependencies={"Fields"},
            reference="Standard real analysis axioms"
        )
        real_analysis.add_axiom("ordered_field", "ℝ is an ordered field")
        real_analysis.add_axiom("completeness", "Every non-empty bounded subset of ℝ has a supremum")
        real_analysis.add_axiom("archimedean", "∀x,y ∈ ℝ, x > 0: ∃n ∈ ℕ: nx > y")
        self.theories["RealAnalysis"] = real_analysis
        
        # === CALCULUS ===
        calculus = AxiomTheory(
            name="Calculus",
            description="Differential and integral calculus",
            dependencies={"RealAnalysis"},
            reference="Standard calculus axioms and definitions"
        )
        calculus.add_axiom("derivative_def", "f'(x) = lim[h→0] (f(x+h) - f(x))/h")
        calculus.add_axiom("integral_def", "∫[a,b] f(x)dx = lim[n→∞] Σ f(xᵢ)Δx")
        calculus.add_axiom("fundamental_theorem_1", "d/dx[∫[a,x] f(t)dt] = f(x)")
        calculus.add_axiom("fundamental_theorem_2", "∫[a,b] f'(x)dx = f(b) - f(a)")
        calculus.add_axiom("power_rule", "d/dx[xⁿ] = n·xⁿ⁻¹")
        calculus.add_axiom("chain_rule", "d/dx[f(g(x))] = f'(g(x))·g'(x)")
        calculus.add_axiom("product_rule", "d/dx[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)")
        calculus.add_axiom("linearity_derivative", "d/dx[af(x) + bg(x)] = a·f'(x) + b·g'(x)")
        calculus.add_axiom("linearity_integral", "∫[a,b] [af(x) + bg(x)]dx = a·∫[a,b]f(x)dx + b·∫[a,b]g(x)dx")
        self.theories["Calculus"] = calculus
        
        # === TOPOLOGY ===
        topology = AxiomTheory(
            name="Topology",
            description="General topology axioms",
            dependencies={"ZFC"},
            reference="Standard topological space axioms"
        )
        topology.add_axiom("empty_and_full", "∅ ∈ τ ∧ X ∈ τ")
        topology.add_axiom("arbitrary_union", "∀F ⊆ τ: ⋃F ∈ τ")
        topology.add_axiom("finite_intersection", "∀U,V ∈ τ: U ∩ V ∈ τ")
        self.theories["Topology"] = topology
        
        # === CATEGORY THEORY ===
        category_theory = AxiomTheory(
            name="CategoryTheory",
            description="Category theory axioms",
            reference="Standard category axioms"
        )
        category_theory.add_axiom("composition", "∀f: A → B, g: B → C: ∃(g ∘ f): A → C")
        category_theory.add_axiom("associativity", "∀f,g,h: (h ∘ g) ∘ f = h ∘ (g ∘ f)")
        category_theory.add_axiom("identity", "∀A: ∃idₐ: A → A: ∀f: A → B: f ∘ idₐ = f ∧ id_B ∘ f = f")
        category_theory.add_axiom("yoneda", "Nat(Hom(A,-), F) ≅ F(A)")
        self.theories["CategoryTheory"] = category_theory
        
        # === NUMBER THEORY ===
        number_theory = AxiomTheory(
            name="NumberTheory",
            description="Elementary number theory",
            dependencies={"Peano"},
            reference="Standard number theory results"
        )
        number_theory.add_axiom("division_algorithm", "∀a,b ∈ ℤ, b ≠ 0: ∃!q,r: a = bq + r ∧ 0 ≤ r < |b|")
        number_theory.add_axiom("fundamental_theorem_arithmetic", "Every n > 1 has unique prime factorization")
        number_theory.add_axiom("euclid_gcd", "gcd(a,b) = gcd(b, a mod b)")
        self.theories["NumberTheory"] = number_theory
    
    def add_theory(self, theory: AxiomTheory):
        """Add a custom theory to the library"""
        self.theories[theory.name] = theory
    
    def get_theory(self, name: str) -> AxiomTheory:
        """Retrieve a theory by name"""
        return self.theories.get(name)
    
    def list_theories(self) -> List[str]:
        """List all available theories"""
        return list(self.theories.keys())
    
    def get_axiom(self, theory_name: str, axiom_name: str) -> str:
        """Get specific axiom from a theory"""
        theory = self.get_theory(theory_name)
        if theory:
            return theory.get_axiom(axiom_name)
        return ""
    
    def add_axiom(self, theory_name: str, axiom_name: str, statement: str):
        """Add axiom to existing theory"""
        theory = self.get_theory(theory_name)
        if theory:
            theory.add_axiom(axiom_name, statement)
        else:
            # Create new theory if it doesn't exist
            new_theory = AxiomTheory(
                name=theory_name,
                description=f"Custom theory: {theory_name}"
            )
            new_theory.add_axiom(axiom_name, statement)
            self.add_theory(new_theory)
