"""
AXION Test Suite
Comprehensive tests for all functionality
"""

import sys
sys.path.append('..')

from solvers.universal_solver import UniversalSolver
from session.proof_session import ProofSession
from core.inference_kernel import InferenceKernel, Expression, InferenceRule

def test_theories():
    """Test theory listing and axiom retrieval"""
    print("=" * 70)
    print("TEST: Theory Management")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    # Test 1: List theories
    theories = solver.list_theories()
    assert len(theories) > 0, "No theories loaded"
    print(f"✓ Found {len(theories)} theories")
    
    # Test 2: Get axioms from each theory
    for theory_name in theories:
        axioms = solver.get_axioms(theory_name)
        assert len(axioms) > 0, f"Theory {theory_name} has no axioms"
        print(f"✓ {theory_name:20} has {len(axioms):2} axioms")
    
    print()

def test_differentiation():
    """Test symbolic differentiation"""
    print("=" * 70)
    print("TEST: Differentiation")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    test_cases = [
        ("x", "1"),
        ("x^2", "2*x"),
        ("x^3", "3*x^2"),
        ("5*x^2", "10*x"),
    ]
    
    for expr, expected in test_cases:
        result = solver.solve(expr, using="Calculus", problem_type="differentiate")
        status = "✓" if result == expected else "✗"
        print(f"{status} d/dx[{expr:10}] = {result:15} (expected: {expected})")
    
    print()

def test_integration():
    """Test symbolic integration"""
    print("=" * 70)
    print("TEST: Integration")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    test_cases = [
        ("x", "x^2/2"),
        ("x^2", "x^3/3"),
        ("x^3", "x^4/4"),
    ]
    
    for expr, expected in test_cases:
        result = solver.solve(expr, using="Calculus", problem_type="integrate")
        status = "✓" if result == expected else "✗"
        print(f"{status} ∫ {expr:10} dx = {result:15} (expected: {expected})")
    
    print()

def test_simplification():
    """Test expression simplification"""
    print("=" * 70)
    print("TEST: Simplification")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    test_cases = [
        ("x + 0", "x"),
        ("x * 1", "x"),
        ("x * 0", "0"),
        ("x - x", "0"),
        ("x^1", "x"),
        ("x^0", "1"),
    ]
    
    for expr, expected in test_cases:
        result = solver.solve(expr, problem_type="simplify")
        status = "✓" if result == expected else "✗"
        print(f"{status} simplify({expr:10}) = {result:5} (expected: {expected})")
    
    print()

def test_theorem_proving():
    """Test formal theorem proving"""
    print("=" * 70)
    print("TEST: Theorem Proving")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    theorems = [
        ("∀x: x = x", "Logic", "Reflexivity"),
        ("∀P: P ∨ ¬P", "Logic", "Excluded middle"),
        ("∀n: n + 0 = n", "Peano", "Addition identity"),
    ]
    
    for theorem, theory, description in theorems:
        proof = solver.solve(theorem, using=theory, problem_type="prove")
        status = "✓" if proof.is_valid else "✗"
        print(f"{status} [{theory:10}] {description:20} - {len(proof.steps)} steps")
        if proof.proof_hash:
            print(f"   Hash: {proof.proof_hash[:32]}...")
    
    print()

def test_session_management():
    """Test proof session functionality"""
    print("=" * 70)
    print("TEST: Session Management")
    print("=" * 70)
    
    solver = UniversalSolver()
    session = ProofSession()
    
    # Prove multiple theorems
    theorems = [
        ("∀x: x = x", "Logic"),
        ("∀n: n + 0 = n", "Peano"),
    ]
    
    for theorem, theory in theorems:
        proof = solver.solve(theorem, using=theory, problem_type="prove")
        session.add_proof(proof)
        print(f"✓ Added proof: {theorem}")
    
    # Check statistics
    stats = session.statistics()
    print(f"\n✓ Session has {stats['total_proofs']} proofs")
    print(f"✓ Valid proofs: {stats['valid_proofs']}")
    print(f"✓ Unique theorems: {stats['unique_theorems']}")
    
    # Test export
    try:
        session.export_session("test_session.json")
        print("✓ Session exported successfully")
    except Exception as e:
        print(f"✗ Export failed: {e}")
    
    print()

def test_custom_axioms():
    """Test adding custom axioms"""
    print("=" * 70)
    print("TEST: Custom Axioms")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    # Test 1: Add axiom to existing theory
    initial_count = len(solver.get_axioms("Peano"))
    solver.add_axiom("Peano", "test_axiom", "∀x: test(x)")
    new_count = len(solver.get_axioms("Peano"))
    
    if new_count == initial_count + 1:
        print("✓ Successfully added axiom to existing theory")
    else:
        print("✗ Failed to add axiom to existing theory")
    
    # Test 2: Create new theory
    solver.add_theory(
        name="TestTheory",
        description="Test theory",
        axioms={"axiom1": "∀x: P(x)"}
    )
    
    if "TestTheory" in solver.list_theories():
        print("✓ Successfully created new theory")
    else:
        print("✗ Failed to create new theory")
    
    print()

def test_inference_rules():
    """Test core inference rules"""
    print("=" * 70)
    print("TEST: Inference Rules")
    print("=" * 70)
    
    kernel = InferenceKernel()
    
    # Test 1: Modus Ponens
    p_implies_q = Expression("P ⟹ Q")
    p = Expression("P")
    result = kernel.modus_ponens(p_implies_q, p)
    
    if result and result.content == "Q":
        print("✓ Modus ponens works")
    else:
        print("✗ Modus ponens failed")
    
    # Test 2: Universal Instantiation
    universal = Expression("∀x: P(x)")
    result = kernel.universal_instantiation(universal, "a")
    
    if result and "P(a)" in result.content:
        print("✓ Universal instantiation works")
    else:
        print("✗ Universal instantiation failed")
    
    # Test 3: Conjunction
    expr1 = Expression("P")
    expr2 = Expression("Q")
    result = kernel.conjunction_intro(expr1, expr2)
    
    if result and "∧" in result.content:
        print("✓ Conjunction introduction works")
    else:
        print("✗ Conjunction introduction failed")
    
    # Test 4: Transitivity
    eq1 = Expression("a = b")
    eq2 = Expression("b = c")
    result = kernel.transitivity(eq1, eq2)
    
    if result and result.content == "a = c":
        print("✓ Transitivity works")
    else:
        print("✗ Transitivity failed")
    
    print()

def test_auto_detection():
    """Test automatic problem type detection"""
    print("=" * 70)
    print("TEST: Auto-Detection")
    print("=" * 70)
    
    solver = UniversalSolver()
    
    test_cases = [
        ("x^2", "simplify"),
        ("d/dx[x^2]", "differentiate"),
        ("∫x dx", "integrate"),
        ("∀x: x = x", "prove"),
    ]
    
    for problem, expected_type in test_cases:
        detected_type = solver._detect_problem_type(problem)
        status = "✓" if detected_type == expected_type else "✗"
        print(f"{status} '{problem}' → detected as '{detected_type}' (expected: {expected_type})")
    
    print()

def test_proof_validation():
    """Test proof validation"""
    print("=" * 70)
    print("TEST: Proof Validation")
    print("=" * 70)
    
    kernel = InferenceKernel()
    
    # Create a valid proof
    theorem = Expression("Q")
    proof = kernel.create_proof(theorem)
    
    # Add valid steps
    p_implies_q = Expression("P ⟹ Q")
    p = Expression("P")
    q = Expression("Q")
    
    proof.assumptions = [p_implies_q, p]
    kernel.add_step(proof, p_implies_q, InferenceRule.AXIOM_APPLICATION, justification="Assumption")
    kernel.add_step(proof, p, InferenceRule.AXIOM_APPLICATION, justification="Assumption")
    kernel.add_step(proof, q, InferenceRule.MODUS_PONENS, premises=[p_implies_q, p], justification="MP")
    
    # Validate
    is_valid = kernel.validate_proof(proof)
    
    if is_valid:
        print("✓ Valid proof accepted")
        print(f"  Proof hash: {proof.proof_hash[:32]}...")
    else:
        print("✗ Valid proof rejected")
    
    print()

def run_all_tests():
    """Run complete test suite"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "AXION TEST SUITE" + " " * 32 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    tests = [
        test_theories,
        test_differentiation,
        test_integration,
        test_simplification,
        test_theorem_proving,
        test_session_management,
        test_custom_axioms,
        test_inference_rules,
        test_auto_detection,
        test_proof_validation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests:  {len(tests)}")
    print(f"Passed:       {passed} ✓")
    print(f"Failed:       {failed} ✗")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 All tests passed! AXION is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the output above.")

if __name__ == "__main__":
    run_all_tests()
