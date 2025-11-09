"""
AXION Universal Solver
Strategies for theorem proving and symbolic computation
"""

import re
from typing import List, Dict, Optional, Set, Tuple, Any
from dataclasses import dataclass
from core.inference_kernel import (
    Expression, Proof, ProofStep, InferenceRule, InferenceKernel
)
from axioms.axiom_library import AxiomLibrary

class SolverStrategy:
    """Base class for solving strategies"""
    
    def __init__(self, kernel: InferenceKernel, library: AxiomLibrary):
        self.kernel = kernel
        self.library = library
    
    def solve(self, problem: str, theory: str = "Logic") -> Any:
        """Override in subclasses"""
        raise NotImplementedError

class TheoremProver(SolverStrategy):
    """
    Automated theorem proving using forward/backward chaining
    """
    
    def prove(self, theorem: str, theory: str = "Logic", 
              max_steps: int = 100) -> Optional[Proof]:
        """
        Attempt to prove a theorem using axioms from specified theory
        """
        theorem_expr = Expression(content=theorem)
        proof = self.kernel.create_proof(theorem_expr, theory)
        
        # Get axioms from theory
        theory_obj = self.library.get_theory(theory)
        if not theory_obj:
            print(f"Theory '{theory}' not found")
            return None
        
        # Add axioms as assumptions
        for axiom_name, axiom_statement in theory_obj.axioms.items():
            axiom_expr = Expression(content=axiom_statement)
            proof.assumptions.append(axiom_expr)
            proof.axioms_used.add(f"{theory}.{axiom_name}")
            
            # Add axiom as first step
            step = ProofStep(
                statement=axiom_expr,
                rule=InferenceRule.AXIOM_APPLICATION,
                justification=f"Axiom: {theory}.{axiom_name}"
            )
            self.kernel.add_step(proof, axiom_expr, InferenceRule.AXIOM_APPLICATION,
                                justification=f"Axiom: {theory}.{axiom_name}")
        
        # Try to derive theorem (simple forward chaining)
        derived = set(proof.assumptions)
        
        for _ in range(max_steps):
            # Check if we've proven the theorem
            if theorem_expr in derived:
                proof.is_valid = True
                proof.finalize()
                return proof
            
            # Try applying inference rules
            new_derivations = self._apply_rules(list(derived), proof)
            if not new_derivations:
                break
            derived.update(new_derivations)
        
        return proof
    
    def _apply_rules(self, statements: List[Expression], proof: Proof) -> Set[Expression]:
        """Apply inference rules to derive new statements"""
        new = set()
        
        # Try modus ponens on all pairs
        for s1 in statements:
            for s2 in statements:
                if "⟹" in s1.content:
                    result = self.kernel.modus_ponens(s1, s2)
                    if result and result not in statements:
                        self.kernel.add_step(proof, result, InferenceRule.MODUS_PONENS,
                                           premises=[s1, s2],
                                           justification="Modus ponens")
                        new.add(result)
        
        # Try universal instantiation
        for s in statements:
            if s.content.startswith("∀"):
                # Try instantiating with common terms
                for term in ["0", "1", "x", "a", "n"]:
                    result = self.kernel.universal_instantiation(s, term)
                    if result and result not in statements:
                        self.kernel.add_step(proof, result, 
                                           InferenceRule.UNIVERSAL_INSTANTIATION,
                                           premises=[s],
                                           justification=f"Universal instantiation with {term}")
                        new.add(result)
        
        return new

class SymbolicManipulator(SolverStrategy):
    """
    Computer Algebra System (CAS) functionality
    Symbolic manipulation, simplification, differentiation, integration
    """
    
    def __init__(self, kernel: InferenceKernel, library: AxiomLibrary):
        super().__init__(kernel, library)
        self.simplification_rules = self._load_simplification_rules()
    
    def _load_simplification_rules(self) -> List[Tuple[str, str]]:
        """Load algebraic simplification rules"""
        return [
            (r"x \+ 0", "x"),
            (r"0 \+ x", "x"),
            (r"x \* 1", "x"),
            (r"1 \* x", "x"),
            (r"x \* 0", "0"),
            (r"0 \* x", "0"),
            (r"x \- x", "0"),
            (r"x / x", "1"),
            (r"x \^ 0", "1"),
            (r"x \^ 1", "x"),
        ]
    
    def simplify(self, expr: str) -> str:
        """
        Algebraic simplification
        """
        result = expr
        
        # Apply simplification rules iteratively
        changed = True
        iterations = 0
        max_iterations = 100
        
        while changed and iterations < max_iterations:
            changed = False
            for pattern, replacement in self.simplification_rules:
                new_result = re.sub(pattern, replacement, result)
                if new_result != result:
                    result = new_result
                    changed = True
            iterations += 1
        
        return result
    
    def differentiate(self, expr: str, var: str = "x") -> str:
        """
        Symbolic differentiation using calculus axioms
        """
        expr = expr.strip()
        
        # Constant rule
        if var not in expr:
            return "0"
        
        # Variable rule: d/dx[x] = 1
        if expr == var:
            return "1"
        
        # Power rule: d/dx[x^n] = n*x^(n-1)
        power_pattern = rf"{var}\^(\d+)"
        match = re.match(power_pattern, expr)
        if match:
            n = int(match.group(1))
            if n == 0:
                return "0"
            elif n == 1:
                return "1"
            elif n == 2:
                return f"2*{var}"
            else:
                return f"{n}*{var}^{n-1}"
        
        # Polynomial terms: d/dx[c*x^n]
        poly_pattern = rf"(\d+)\*{var}\^(\d+)"
        match = re.match(poly_pattern, expr)
        if match:
            c = int(match.group(1))
            n = int(match.group(2))
            if n == 0:
                return "0"
            elif n == 1:
                return str(c)
            elif n == 2:
                return f"{c*n}*{var}"
            else:
                return f"{c*n}*{var}^{n-1}"
        
        # Sum rule: d/dx[f + g] = f' + g'
        if "+" in expr and not self._is_in_parens(expr, "+"):
            parts = expr.split("+")
            derivatives = [self.differentiate(part.strip(), var) for part in parts]
            return " + ".join(derivatives)
        
        # Product rule: d/dx[f*g] = f'*g + f*g'
        if "*" in expr and not self._is_in_parens(expr, "*"):
            parts = expr.split("*", 1)
            if len(parts) == 2:
                f, g = parts[0].strip(), parts[1].strip()
                f_prime = self.differentiate(f, var)
                g_prime = self.differentiate(g, var)
                return f"({f_prime})*({g}) + ({f})*({g_prime})"
        
        # Default: return symbolic notation
        return f"d/d{var}[{expr}]"
    
    def _is_in_parens(self, expr: str, operator: str) -> bool:
        """Check if operator is inside parentheses"""
        depth = 0
        for char in expr:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == operator and depth == 0:
                return False
        return True
    
    def integrate(self, expr: str, var: str = "x") -> str:
        """
        Symbolic integration using calculus axioms
        """
        expr = expr.strip()
        
        # Constant rule
        if var not in expr:
            return f"{expr}*{var}"
        
        # Variable rule: ∫x dx = x^2/2
        if expr == var:
            return f"{var}^2/2"
        
        # Power rule: ∫x^n dx = x^(n+1)/(n+1)
        power_pattern = rf"{var}\^(\d+)"
        match = re.match(power_pattern, expr)
        if match:
            n = int(match.group(1))
            return f"{var}^{n+1}/{n+1}"
        
        # Polynomial terms: ∫c*x^n dx
        poly_pattern = rf"(\d+)\*{var}\^(\d+)"
        match = re.match(poly_pattern, expr)
        if match:
            c = int(match.group(1))
            n = int(match.group(2))
            return f"{c}*{var}^{n+1}/{n+1}"
        
        # Linearity: ∫(f + g) dx = ∫f dx + ∫g dx
        if "+" in expr:
            parts = expr.split("+")
            integrals = [self.integrate(part.strip(), var) for part in parts]
            return " + ".join(integrals)
        
        # Default: return symbolic notation
        return f"∫{expr} d{var}"
    
    def solve_equation(self, equation: str, var: str = "x") -> List[str]:
        """
        Solve simple equations
        """
        # Very basic solver for linear equations
        if "=" not in equation:
            return []
        
        lhs, rhs = equation.split("=")
        lhs, rhs = lhs.strip(), rhs.strip()
        
        # Linear equation: ax + b = c
        pattern = rf"(\d*)\*?{var}\s*\+\s*(\d+)\s*"
        match = re.match(pattern, lhs)
        if match:
            a = int(match.group(1)) if match.group(1) else 1
            b = int(match.group(2))
            c = int(rhs)
            
            # Solve: x = (c - b) / a
            solution = (c - b) / a
            return [f"{var} = {solution}"]
        
        return [f"Solution for {equation} not implemented"]

class UniversalSolver:
    """
    Main interface for AXION solver
    Dispatches to appropriate strategy based on problem type
    """
    
    def __init__(self):
        self.kernel = InferenceKernel()
        self.library = AxiomLibrary()
        self.prover = TheoremProver(self.kernel, self.library)
        self.manipulator = SymbolicManipulator(self.kernel, self.library)
        
    def solve(self, problem: str, using: str = "Logic", 
              problem_type: str = "auto") -> Any:
        """
        Universal problem solver
        
        Args:
            problem: The mathematical problem/theorem to solve
            using: Theory to use (Logic, Peano, Calculus, etc.)
            problem_type: 'prove', 'differentiate', 'integrate', 'simplify', 'auto'
        
        Returns:
            Solution (proof, symbolic result, etc.)
        """
        
        # Auto-detect problem type
        if problem_type == "auto":
            problem_type = self._detect_problem_type(problem)
        
        if problem_type == "prove":
            return self.prover.prove(problem, theory=using)
        
        elif problem_type == "differentiate":
            # Extract expression to differentiate
            if "d/dx" in problem or "'" in problem:
                expr = self._extract_expression(problem)
            else:
                expr = problem
            return self.manipulator.differentiate(expr)
        
        elif problem_type == "integrate":
            # Extract expression to integrate
            if "∫" in problem:
                expr = self._extract_expression(problem)
            else:
                expr = problem
            return self.manipulator.integrate(expr)
        
        elif problem_type == "simplify":
            return self.manipulator.simplify(problem)
        
        elif problem_type == "solve":
            return self.manipulator.solve_equation(problem)
        
        else:
            return f"Unknown problem type: {problem_type}"
    
    def _detect_problem_type(self, problem: str) -> str:
        """Auto-detect what kind of problem this is"""
        problem_lower = problem.lower()
        
        if "∫" in problem or "integrate" in problem_lower:
            return "integrate"
        elif "d/dx" in problem or "derivative" in problem_lower or "'" in problem:
            return "differentiate"
        elif "simplify" in problem_lower:
            return "simplify"
        elif "=" in problem and not any(q in problem for q in ["∀", "∃", "⟹"]):
            return "solve"
        elif any(q in problem for q in ["∀", "∃", "⟹", "prove", "show that"]):
            return "prove"
        else:
            return "simplify"
    
    def _extract_expression(self, problem: str) -> str:
        """Extract the core expression from a problem statement"""
        # Remove common keywords
        expr = problem.replace("differentiate", "").replace("integrate", "")
        expr = expr.replace("d/dx", "").replace("∫", "").replace("dx", "")
        expr = expr.replace("[", "").replace("]", "")
        return expr.strip()
    
    def list_theories(self) -> List[str]:
        """List all available mathematical theories"""
        return self.library.list_theories()
    
    def get_axioms(self, theory: str) -> Dict[str, str]:
        """Get all axioms from a theory"""
        theory_obj = self.library.get_theory(theory)
        if theory_obj:
            return theory_obj.axioms
        return {}
    
    def add_axiom(self, theory: str, name: str, statement: str):
        """Add a custom axiom to a theory"""
        self.library.add_axiom(theory, name, statement)
    
    def add_theory(self, name: str, description: str, axioms: Dict[str, str]):
        """Create a new theory"""
        from axioms.axiom_library import AxiomTheory
        theory = AxiomTheory(name=name, description=description)
        for axiom_name, axiom_statement in axioms.items():
            theory.add_axiom(axiom_name, axiom_statement)
        self.library.add_theory(theory)
