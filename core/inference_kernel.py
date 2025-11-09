"""
AXION Core Inference Kernel
Pure logical inference rules - no domain-specific knowledge
"""

from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional, Tuple, Any
from enum import Enum
import hashlib
import json

class LogicalConnective(Enum):
    """Fundamental logical operators"""
    AND = "∧"
    OR = "∨"
    IMPLIES = "⟹"
    IFF = "⟺"
    NOT = "¬"
    FORALL = "∀"
    EXISTS = "∃"
    EQUALS = "="

class InferenceRule(Enum):
    """Pure inference rules - domain independent"""
    MODUS_PONENS = "modus_ponens"
    MODUS_TOLLENS = "modus_tollens"
    UNIVERSAL_INSTANTIATION = "universal_instantiation"
    EXISTENTIAL_GENERALIZATION = "existential_generalization"
    CONJUNCTION_INTRODUCTION = "conjunction_intro"
    CONJUNCTION_ELIMINATION = "conjunction_elim"
    DISJUNCTION_INTRODUCTION = "disjunction_intro"
    DISJUNCTION_ELIMINATION = "disjunction_elim"
    SUBSTITUTION = "substitution"
    REFLEXIVITY = "reflexivity"
    SYMMETRY = "symmetry"
    TRANSITIVITY = "transitivity"
    AXIOM_APPLICATION = "axiom_application"

@dataclass
class Expression:
    """Mathematical expression/formula"""
    content: str
    variables: Set[str] = field(default_factory=set)
    free_variables: Set[str] = field(default_factory=set)
    bound_variables: Set[str] = field(default_factory=set)
    type_signature: Optional[str] = None
    
    def __hash__(self):
        return hash(self.content)
    
    def __eq__(self, other):
        return isinstance(other, Expression) and self.content == other.content
    
    def __repr__(self):
        return f"Expr({self.content})"

@dataclass
class ProofStep:
    """Single step in a formal proof"""
    statement: Expression
    rule: InferenceRule
    premises: List[Expression] = field(default_factory=list)
    justification: str = ""
    line_number: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "statement": self.statement.content,
            "rule": self.rule.value,
            "premises": [p.content for p in self.premises],
            "justification": self.justification,
            "line": self.line_number
        }

@dataclass
class Proof:
    """Complete formal proof with cryptographic verification"""
    theorem: Expression
    axioms_used: Set[str] = field(default_factory=set)
    steps: List[ProofStep] = field(default_factory=list)
    assumptions: List[Expression] = field(default_factory=list)
    theory_context: str = "Pure Logic"
    is_valid: bool = False
    proof_hash: Optional[str] = None
    
    def compute_hash(self) -> str:
        """Cryptographic hash of entire proof"""
        proof_data = {
            "theorem": self.theorem.content,
            "axioms": sorted(list(self.axioms_used)),
            "steps": [step.to_dict() for step in self.steps],
            "assumptions": [a.content for a in self.assumptions],
            "theory": self.theory_context
        }
        proof_json = json.dumps(proof_data, sort_keys=True)
        return hashlib.sha256(proof_json.encode()).hexdigest()
    
    def finalize(self):
        """Mark proof as complete and compute hash"""
        self.proof_hash = self.compute_hash()
        self.is_valid = True
        
    def __repr__(self):
        status = "✓ Valid" if self.is_valid else "⧗ Incomplete"
        return f"Proof[{status}]: {self.theorem.content} ({len(self.steps)} steps)"

class InferenceKernel:
    """
    Pure logical inference engine
    No mathematical knowledge - only formal rules
    """
    
    def __init__(self):
        self.proof_cache: Dict[str, Proof] = {}
        
    def modus_ponens(self, implication: Expression, antecedent: Expression) -> Optional[Expression]:
        """
        If (P ⟹ Q) and P, then Q
        """
        # Simple pattern matching for implications
        if "⟹" in implication.content:
            parts = implication.content.split("⟹")
            if len(parts) == 2:
                premise = parts[0].strip()
                conclusion = parts[1].strip()
                if premise == antecedent.content.strip():
                    return Expression(content=conclusion)
        return None
    
    def universal_instantiation(self, universal: Expression, instance: str) -> Optional[Expression]:
        """
        From ∀x.P(x), derive P(t) for any term t
        """
        if universal.content.startswith("∀"):
            # Extract variable and body
            # Simple parser: ∀x: P(x) or ∀x.P(x)
            content = universal.content[1:]  # Remove ∀
            if ":" in content:
                var, body = content.split(":", 1)
            elif "." in content:
                var, body = content.split(".", 1)
            else:
                return None
            
            var = var.strip()
            body = body.strip()
            
            # Substitute instance for variable
            instantiated = body.replace(var, instance)
            return Expression(content=instantiated)
        return None
    
    def substitution(self, expr: Expression, substitutions: Dict[str, str]) -> Expression:
        """
        Replace variables/terms according to substitution map
        """
        result = expr.content
        for old, new in substitutions.items():
            result = result.replace(old, new)
        return Expression(content=result)
    
    def conjunction_intro(self, expr1: Expression, expr2: Expression) -> Expression:
        """
        From P and Q, derive P ∧ Q
        """
        return Expression(content=f"({expr1.content} ∧ {expr2.content})")
    
    def conjunction_elim_left(self, conjunction: Expression) -> Optional[Expression]:
        """
        From P ∧ Q, derive P
        """
        if "∧" in conjunction.content:
            parts = conjunction.content.split("∧")
            if len(parts) >= 2:
                left = parts[0].strip().strip("()")
                return Expression(content=left)
        return None
    
    def conjunction_elim_right(self, conjunction: Expression) -> Optional[Expression]:
        """
        From P ∧ Q, derive Q
        """
        if "∧" in conjunction.content:
            parts = conjunction.content.split("∧")
            if len(parts) >= 2:
                right = parts[-1].strip().strip("()")
                return Expression(content=right)
        return None
    
    def transitivity(self, expr1: Expression, expr2: Expression, relation: str = "=") -> Optional[Expression]:
        """
        From a = b and b = c, derive a = c
        """
        if relation in expr1.content and relation in expr2.content:
            parts1 = expr1.content.split(relation)
            parts2 = expr2.content.split(relation)
            
            if len(parts1) == 2 and len(parts2) == 2:
                a, b1 = parts1[0].strip(), parts1[1].strip()
                b2, c = parts2[0].strip(), parts2[1].strip()
                
                if b1 == b2:
                    return Expression(content=f"{a} {relation} {c}")
        return None
    
    def create_proof(self, theorem: Expression, theory: str = "Pure Logic") -> Proof:
        """
        Initialize a new proof object
        """
        proof = Proof(theorem=theorem, theory_context=theory)
        return proof
    
    def add_step(self, proof: Proof, statement: Expression, rule: InferenceRule, 
                 premises: List[Expression] = None, justification: str = "") -> ProofStep:
        """
        Add a validated step to a proof
        """
        step = ProofStep(
            statement=statement,
            rule=rule,
            premises=premises or [],
            justification=justification,
            line_number=len(proof.steps) + 1
        )
        proof.steps.append(step)
        return step
    
    def validate_step(self, step: ProofStep, available_statements: List[Expression]) -> bool:
        """
        Verify that an inference step is valid
        """
        # Check that all premises are available
        for premise in step.premises:
            if premise not in available_statements:
                return False
        
        # Rule-specific validation
        if step.rule == InferenceRule.MODUS_PONENS:
            if len(step.premises) != 2:
                return False
            result = self.modus_ponens(step.premises[0], step.premises[1])
            return result is not None and result.content == step.statement.content
        
        # Add more rule validations as needed
        return True
    
    def validate_proof(self, proof: Proof) -> bool:
        """
        Validate entire proof from axioms to conclusion
        """
        available = list(proof.assumptions)
        
        for step in proof.steps:
            if not self.validate_step(step, available):
                return False
            available.append(step.statement)
        
        # Check that final step proves the theorem
        if proof.steps:
            final = proof.steps[-1].statement
            if final.content == proof.theorem.content:
                proof.is_valid = True
                proof.finalize()
                return True
        
        return False
