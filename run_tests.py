import sys
import os
import traceback

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

def run_suite():
    print("=" * 70)
    print("RUNNING RAILWAY AI PLATFORM TEST SUITE")
    print("=" * 70)

    # 1. Test Contracts
    print("\n[1/3] Testing Contracts & Schemas...")
    try:
        from tests.test_contracts import (
            test_wl_contract_validation,
            test_recommender_contract,
            test_delay_contract,
            test_fare_contract,
            test_canary_config_contract
        )
        test_wl_contract_validation()
        test_recommender_contract()
        test_delay_contract()
        test_fare_contract()
        test_canary_config_contract()
        print("  ✓ All Pydantic v2 contract validations passed!")
    except Exception as e:
        print(f"  ✗ Contracts test failed: {e}")
        traceback.print_exc()
        return False

    # 2. Test Services
    print("\n[2/3] Testing Side A AI Services...")
    try:
        from tests.test_services import (
            test_wl_predictor_service,
            test_recommender_engine,
            test_delay_predictor_service,
            test_fare_predictor_service,
            test_support_assistant_rag,
            test_fraud_detector_engine
        )
        test_wl_predictor_service()
        print("  ✓ WL Predictor Service (XGBoost + SHAP + Berth Allocation) passed!")
        test_recommender_engine()
        print("  ✓ Recommender Engine (Multi-criteria Scoring) passed!")
        test_delay_predictor_service()
        print("  ✓ Delay Predictor Service (Regression + Station Congestion) passed!")
        test_fare_predictor_service()
        print("  ✓ Dynamic Fare Predictor (Progression Curve + Anomaly Detection) passed!")
        test_support_assistant_rag()
        print("  ✓ Support Assistant RAG (Multilingual + Groundedness Score) passed!")
        test_fraud_detector_engine()
        print("  ✓ Fraud & Bot Detector (Velocity + Isolation Forest) passed!")
    except Exception as e:
        print(f"  ✗ Services test failed: {e}")
        traceback.print_exc()
        return False

    # 3. Test End-to-End Governance Lifecycle
    print("\n[3/3] Testing Side B Autonomous AI Governance Lifecycle...")
    try:
        from tests.test_e2e_governance import test_full_autonomous_governance_lifecycle
        test_full_autonomous_governance_lifecycle()
        print("  ✓ Drift Detection (PSI > 0.25) -> RCA Diagnosis -> Retrain -> 5% Canary -> Auto-Rollback -> SHA-256 Audit Chain verified!")
    except Exception as e:
        print(f"  ✗ Governance test failed: {e}")
        traceback.print_exc()
        return False

    # 4. Enterprise Hard Benchmarks & Verification
    print("\n[4/4] Testing Enterprise Hard Benchmarks & Autonomous Layer...")
    import subprocess
    benchmarks = [
        ("Planner Agent (Physical Feasibility & Budget Constraints)", "scripts/test_planner_agent_queries.py"),
        ("Fraud Detection (100% Precision / 97.5% Recall Benchmark)", "scripts/test_fraud_precision_recall.py"),
        ("Agentic Supervisory Layer (Autonomous Interventions & Chain)", "scripts/test_supervisor.py"),
        ("Disaster Recovery & Backup Restore Integrity", "scripts/backup_restore.py"),
        ("High-Concurrency Latency & Throughput SLA Load Test", "scripts/load_test.py"),
        ("Resilience & Failure Injection Test Harness", "scripts/failure_injection_demo.py")
    ]
    py_exec = sys.executable
    for desc, script in benchmarks:
        print(f"  Running {desc}...")
        res = subprocess.run([py_exec, os.path.join(BASE_DIR, script)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  ✗ Benchmark failed: {script}")
            print(res.stderr or res.stdout)
            return False
        print(f"  ✓ {desc} passed!")

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED SUCCESSFULLY! (100% GREEN)")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = run_suite()
    sys.exit(0 if success else 1)
