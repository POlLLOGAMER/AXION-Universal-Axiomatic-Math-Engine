"""
AXION Proof Session Manager
Manages proof history, theorem database, and verification
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from core.inference_kernel import Proof, Expression

@dataclass
class ProofRecord:
    """Record of a completed proof"""
    theorem: str
    theory: str
    proof_hash: str
    timestamp: str
    axioms_used: List[str]
    step_count: int
    is_valid: bool
    
    def to_dict(self) -> Dict:
        return {
            "theorem": self.theorem,
            "theory": self.theory,
            "proof_hash": self.proof_hash,
            "timestamp": self.timestamp,
            "axioms_used": self.axioms_used,
            "step_count": self.step_count,
            "is_valid": self.is_valid
        }
    
    @classmethod
    def from_proof(cls, proof: Proof) -> 'ProofRecord':
        return cls(
            theorem=proof.theorem.content,
            theory=proof.theory_context,
            proof_hash=proof.proof_hash or "",
            timestamp=datetime.now().isoformat(),
            axioms_used=list(proof.axioms_used),
            step_count=len(proof.steps),
            is_valid=proof.is_valid
        )

class ProofSession:
    """
    Session manager for AXION
    Tracks all proofs, computations, and theorems
    """
    
    def __init__(self):
        self.proof_history: List[ProofRecord] = []
        self.theorem_database: Dict[str, List[ProofRecord]] = {}
        self.current_context: str = "Logic"
        
    def add_proof(self, proof: Proof):
        """Register a completed proof"""
        record = ProofRecord.from_proof(proof)
        self.proof_history.append(record)
        
        # Add to theorem database
        theorem_key = proof.theorem.content
        if theorem_key not in self.theorem_database:
            self.theorem_database[theorem_key] = []
        self.theorem_database[theorem_key].append(record)
    
    def get_proof_by_hash(self, proof_hash: str) -> Optional[ProofRecord]:
        """Retrieve proof by its cryptographic hash"""
        for record in self.proof_history:
            if record.proof_hash == proof_hash:
                return record
        return None
    
    def list_proofs(self, theory: Optional[str] = None) -> List[ProofRecord]:
        """List all proofs, optionally filtered by theory"""
        if theory:
            return [p for p in self.proof_history if p.theory == theory]
        return self.proof_history
    
    def verify_proof(self, proof_hash: str) -> bool:
        """Verify a proof exists and is valid"""
        record = self.get_proof_by_hash(proof_hash)
        return record is not None and record.is_valid
    
    def get_theorems(self, theory: Optional[str] = None) -> List[str]:
        """Get all proven theorems"""
        theorems = set()
        for record in self.proof_history:
            if record.is_valid:
                if theory is None or record.theory == theory:
                    theorems.add(record.theorem)
        return list(theorems)
    
    def export_session(self, filepath: str):
        """Export session to JSON"""
        data = {
            "session_info": {
                "export_time": datetime.now().isoformat(),
                "proof_count": len(self.proof_history),
                "context": self.current_context
            },
            "proofs": [p.to_dict() for p in self.proof_history]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_session(self, filepath: str):
        """Import session from JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for proof_dict in data.get("proofs", []):
            record = ProofRecord(
                theorem=proof_dict["theorem"],
                theory=proof_dict["theory"],
                proof_hash=proof_dict["proof_hash"],
                timestamp=proof_dict["timestamp"],
                axioms_used=proof_dict["axioms_used"],
                step_count=proof_dict["step_count"],
                is_valid=proof_dict["is_valid"]
            )
            self.proof_history.append(record)
            
            # Rebuild theorem database
            if record.theorem not in self.theorem_database:
                self.theorem_database[record.theorem] = []
            self.theorem_database[record.theorem].append(record)
    
    def statistics(self) -> Dict:
        """Get session statistics"""
        theories_used = set(p.theory for p in self.proof_history)
        valid_proofs = sum(1 for p in self.proof_history if p.is_valid)
        
        axiom_usage = {}
        for proof in self.proof_history:
            for axiom in proof.axioms_used:
                axiom_usage[axiom] = axiom_usage.get(axiom, 0) + 1
        
        return {
            "total_proofs": len(self.proof_history),
            "valid_proofs": valid_proofs,
            "theories_used": list(theories_used),
            "unique_theorems": len(self.theorem_database),
            "most_used_axioms": sorted(axiom_usage.items(), 
                                      key=lambda x: x[1], 
                                      reverse=True)[:5]
        }
    
    def clear_history(self):
        """Clear all session history"""
        self.proof_history.clear()
        self.theorem_database.clear()
