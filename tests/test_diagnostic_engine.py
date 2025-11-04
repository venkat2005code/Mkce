"""
Test Suite for Automated Diagnostic System
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from patient_model import Patient, VitalSigns, LabResults, Gender, Symptoms
from diagnostic_engine import DiagnosticEngine, RiskLevel


def test_diabetes_detection():
    """Test diabetes detection from elevated glucose levels"""
    print("\n" + "="*60)
    print("TEST 1: Diabetes Detection")
    print("="*60)
    
    engine = DiagnosticEngine()
    
    patient = Patient(
        patient_id="TEST001",
        name="Test Patient Diabetes",
        age=45,
        gender=Gender.MALE,
        vital_signs=VitalSigns(
            temperature=37.0,
            blood_pressure_systolic=130,
            blood_pressure_diastolic=85,
            heart_rate=75,
            respiratory_rate=16,
            oxygen_saturation=98,
            weight=80,
            height=175
        ),
        lab_results=LabResults(
            fasting_glucose=140,
            hba1c=7.2
        ),
        symptoms=Symptoms(
            chief_complaint="Increased thirst and urination",
            symptoms_list=["polyuria", "polydipsia", "fatigue"]
        )
    )
    
    report = engine.analyze_patient(patient)
    
    print(f"Overall Risk: {report.overall_risk.value}")
    print(f"Number of findings: {len(report.findings)}")
    print(f"Possible conditions detected: {len(report.possible_conditions)}")
    
    # Check if diabetes was detected
    diabetes_detected = any(
        "diabetes" in cond["condition"].lower() 
        for cond in report.possible_conditions
    )
    
    print(f"Diabetes detected: {diabetes_detected}")
    
    if diabetes_detected:
        print("✓ TEST PASSED: Diabetes correctly identified")
    else:
        print("✗ TEST FAILED: Diabetes not detected")
    
    return diabetes_detected


def test_hypertension_detection():
    """Test hypertension detection from blood pressure"""
    print("\n" + "="*60)
    print("TEST 2: Hypertension Detection")
    print("="*60)
    
    engine = DiagnosticEngine()
    
    patient = Patient(
        patient_id="TEST002",
        name="Test Patient Hypertension",
        age=55,
        gender=Gender.FEMALE,
        vital_signs=VitalSigns(
            temperature=37.0,
            blood_pressure_systolic=165,
            blood_pressure_diastolic=98,
            heart_rate=72,
            respiratory_rate=16,
            oxygen_saturation=98,
            weight=75,
            height=165
        )
    )
    
    report = engine.analyze_patient(patient)
    
    print(f"Overall Risk: {report.overall_risk.value}")
    
    # Check for blood pressure findings
    bp_findings = [
        f for f in report.findings 
        if "blood pressure" in f.parameter.lower()
    ]
    
    print(f"Blood pressure findings: {len(bp_findings)}")
    
    if bp_findings:
        print(f"Interpretation: {bp_findings[0].interpretation}")
        print("✓ TEST PASSED: Hypertension correctly identified")
        return True
    else:
        print("✗ TEST FAILED: Hypertension not detected")
        return False


def test_anemia_detection():
    """Test anemia detection from low hemoglobin"""
    print("\n" + "="*60)
    print("TEST 3: Anemia Detection")
    print("="*60)
    
    engine = DiagnosticEngine()
    
    patient = Patient(
        patient_id="TEST003",
        name="Test Patient Anemia",
        age=32,
        gender=Gender.FEMALE,
        vital_signs=VitalSigns(
            temperature=37.0,
            blood_pressure_systolic=110,
            blood_pressure_diastolic=70,
            heart_rate=72,
            respiratory_rate=16,
            oxygen_saturation=98,
            weight=60,
            height=165
        ),
        lab_results=LabResults(
            hemoglobin=9.5
        ),
        symptoms=Symptoms(
            chief_complaint="Weakness and fatigue",
            symptoms_list=["fatigue", "weakness", "dizziness"]
        )
    )
    
    report = engine.analyze_patient(patient)
    
    print(f"Overall Risk: {report.overall_risk.value}")
    
    # Check if anemia was detected
    anemia_detected = any(
        "anemia" in cond["condition"].lower() 
        for cond in report.possible_conditions
    )
    
    print(f"Anemia detected: {anemia_detected}")
    
    if anemia_detected:
        print("✓ TEST PASSED: Anemia correctly identified")
    else:
        print("✗ TEST FAILED: Anemia not detected")
    
    return anemia_detected


def test_normal_patient():
    """Test normal patient with no abnormalities"""
    print("\n" + "="*60)
    print("TEST 4: Normal Patient (No Abnormalities)")
    print("="*60)
    
    engine = DiagnosticEngine()
    
    patient = Patient(
        patient_id="TEST004",
        name="Test Patient Normal",
        age=30,
        gender=Gender.MALE,
        vital_signs=VitalSigns(
            temperature=37.0,
            blood_pressure_systolic=118,
            blood_pressure_diastolic=78,
            heart_rate=72,
            respiratory_rate=16,
            oxygen_saturation=98,
            weight=70,
            height=175
        ),
        lab_results=LabResults(
            hemoglobin=15.0,
            fasting_glucose=90,
            total_cholesterol=180
        )
    )
    
    report = engine.analyze_patient(patient)
    
    print(f"Overall Risk: {report.overall_risk.value}")
    print(f"Number of findings: {len(report.findings)}")
    
    if report.overall_risk == RiskLevel.NORMAL and len(report.findings) == 0:
        print("✓ TEST PASSED: Normal patient correctly identified")
        return True
    else:
        print("✗ TEST FAILED: Normal patient incorrectly flagged")
        return False


def test_critical_condition():
    """Test critical condition detection"""
    print("\n" + "="*60)
    print("TEST 5: Critical Condition Detection")
    print("="*60)
    
    engine = DiagnosticEngine()
    
    patient = Patient(
        patient_id="TEST005",
        name="Test Patient Critical",
        age=65,
        gender=Gender.MALE,
        vital_signs=VitalSigns(
            temperature=39.5,
            blood_pressure_systolic=190,
            blood_pressure_diastolic=125,
            heart_rate=110,
            respiratory_rate=24,
            oxygen_saturation=88,
            weight=75,
            height=170
        )
    )
    
    report = engine.analyze_patient(patient)
    
    print(f"Overall Risk: {report.overall_risk.value}")
    print(f"Immediate actions: {len(report.immediate_actions)}")
    
    if report.overall_risk == RiskLevel.CRITICAL:
        print("✓ TEST PASSED: Critical condition correctly identified")
        print("\nImmediate Actions:")
        for action in report.immediate_actions:
            print(f"  - {action}")
        return True
    else:
        print("✗ TEST FAILED: Critical condition not detected")
        return False


def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*60)
    print("AUTOMATED DIAGNOSTIC SYSTEM - TEST SUITE")
    print("="*60)
    
    tests = [
        test_diabetes_detection,
        test_hypertension_detection,
        test_anemia_detection,
        test_normal_patient,
        test_critical_condition
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ TEST ERROR: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
