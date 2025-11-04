"""
Diagnostic Engine
Analyzes patient data and generates diagnostic insights
"""

from typing import List, Dict, Tuple
from patient_model import Patient, VitalSigns, LabResults
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    NORMAL = "normal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DiagnosticFinding:
    """Individual diagnostic finding"""
    category: str
    parameter: str
    value: float
    normal_range: str
    status: RiskLevel
    interpretation: str
    recommendations: List[str]


@dataclass
class DiagnosticReport:
    """Complete diagnostic report"""
    patient_id: str
    findings: List[DiagnosticFinding]
    possible_conditions: List[Dict[str, str]]
    overall_risk: RiskLevel
    immediate_actions: List[str]
    follow_up_tests: List[str]
    general_recommendations: List[str]
    summary: str


class DiagnosticEngine:
    """Main diagnostic analysis engine"""
    
    def __init__(self):
        self.findings = []
        
    def analyze_patient(self, patient: Patient) -> DiagnosticReport:
        """
        Comprehensive patient analysis
        """
        self.findings = []
        possible_conditions = []
        immediate_actions = []
        follow_up_tests = []
        
        # Analyze vital signs
        if patient.vital_signs:
            self._analyze_vitals(patient.vital_signs, patient.age)
        
        # Analyze lab results
        if patient.lab_results:
            conditions = self._analyze_labs(patient.lab_results, patient.age, patient.gender.value)
            possible_conditions.extend(conditions)
        
        # Analyze symptoms correlation
        if patient.symptoms:
            symptom_conditions = self._analyze_symptoms(patient.symptoms, patient.lab_results)
            possible_conditions.extend(symptom_conditions)
        
        # Determine overall risk
        overall_risk = self._calculate_overall_risk()
        
        # Generate immediate actions for high-risk findings
        immediate_actions = self._generate_immediate_actions()
        
        # Recommend follow-up tests
        follow_up_tests = self._recommend_followup_tests()
        
        # General recommendations
        general_recommendations = self._generate_recommendations(patient)
        
        # Create summary
        summary = self._generate_summary(patient, overall_risk)
        
        return DiagnosticReport(
            patient_id=patient.patient_id,
            findings=self.findings,
            possible_conditions=possible_conditions,
            overall_risk=overall_risk,
            immediate_actions=immediate_actions,
            follow_up_tests=follow_up_tests,
            general_recommendations=general_recommendations,
            summary=summary
        )
    
    def _analyze_vitals(self, vitals: VitalSigns, age: int):
        """Analyze vital signs"""
        
        # Temperature
        if vitals.temperature > 38.0:
            self.findings.append(DiagnosticFinding(
                category="Vital Signs",
                parameter="Body Temperature",
                value=vitals.temperature,
                normal_range="36.5-37.5°C",
                status=RiskLevel.HIGH if vitals.temperature > 39.0 else RiskLevel.MODERATE,
                interpretation="Fever detected - possible infection or inflammatory condition",
                recommendations=["Monitor temperature regularly", "Stay hydrated", "Consider antipyretics if >38.5°C"]
            ))
        
        # Blood Pressure
        bp_status = self._assess_blood_pressure(vitals.blood_pressure_systolic, vitals.blood_pressure_diastolic)
        if bp_status[0] != RiskLevel.NORMAL:
            self.findings.append(DiagnosticFinding(
                category="Vital Signs",
                parameter="Blood Pressure",
                value=float(f"{vitals.blood_pressure_systolic}"),
                normal_range="90-120/60-80 mmHg",
                status=bp_status[0],
                interpretation=bp_status[1],
                recommendations=bp_status[2]
            ))
        
        # Heart Rate
        if vitals.heart_rate < 60 or vitals.heart_rate > 100:
            status = RiskLevel.MODERATE if 50 <= vitals.heart_rate <= 110 else RiskLevel.HIGH
            interpretation = "Bradycardia" if vitals.heart_rate < 60 else "Tachycardia"
            self.findings.append(DiagnosticFinding(
                category="Vital Signs",
                parameter="Heart Rate",
                value=float(vitals.heart_rate),
                normal_range="60-100 bpm",
                status=status,
                interpretation=f"{interpretation} detected",
                recommendations=["Monitor heart rate", "ECG recommended", "Check for underlying causes"]
            ))
        
        # Oxygen Saturation
        if vitals.oxygen_saturation < 95:
            status = RiskLevel.CRITICAL if vitals.oxygen_saturation < 90 else RiskLevel.HIGH
            self.findings.append(DiagnosticFinding(
                category="Vital Signs",
                parameter="Oxygen Saturation",
                value=vitals.oxygen_saturation,
                normal_range="95-100%",
                status=status,
                interpretation="Low oxygen levels - possible respiratory issue",
                recommendations=["Oxygen therapy may be needed", "Chest X-ray recommended", "Monitor breathing"]
            ))
        
        # BMI
        bmi = vitals.get_bmi()
        bmi_status = self._assess_bmi(bmi)
        if bmi_status[0] != RiskLevel.NORMAL:
            self.findings.append(DiagnosticFinding(
                category="Vital Signs",
                parameter="BMI",
                value=bmi,
                normal_range="18.5-24.9",
                status=bmi_status[0],
                interpretation=bmi_status[1],
                recommendations=bmi_status[2]
            ))
    
    def _analyze_labs(self, labs: LabResults, age: int, gender: str) -> List[Dict[str, str]]:
        """Analyze laboratory results"""
        conditions = []
        
        # Diabetes screening
        if labs.fasting_glucose and labs.fasting_glucose >= 100:
            status = RiskLevel.HIGH if labs.fasting_glucose >= 126 else RiskLevel.MODERATE
            interpretation = "Diabetes Mellitus" if labs.fasting_glucose >= 126 else "Prediabetes (Impaired Fasting Glucose)"
            self.findings.append(DiagnosticFinding(
                category="Blood Sugar",
                parameter="Fasting Glucose",
                value=labs.fasting_glucose,
                normal_range="70-99 mg/dL",
                status=status,
                interpretation=interpretation,
                recommendations=["HbA1c test recommended", "Lifestyle modifications", "Consult endocrinologist"]
            ))
            conditions.append({
                "condition": interpretation,
                "confidence": "High" if labs.fasting_glucose >= 126 else "Moderate",
                "description": "Elevated blood sugar levels indicate glucose metabolism issues"
            })
        
        # HbA1c
        if labs.hba1c and labs.hba1c >= 5.7:
            status = RiskLevel.HIGH if labs.hba1c >= 6.5 else RiskLevel.MODERATE
            interpretation = "Diabetes Mellitus" if labs.hba1c >= 6.5 else "Prediabetes"
            self.findings.append(DiagnosticFinding(
                category="Blood Sugar",
                parameter="HbA1c",
                value=labs.hba1c,
                normal_range="<5.7%",
                status=status,
                interpretation=interpretation,
                recommendations=["Blood sugar monitoring", "Dietary changes", "Regular exercise"]
            ))
        
        # Lipid Profile - Cardiovascular Risk
        if labs.total_cholesterol and labs.total_cholesterol >= 200:
            status = RiskLevel.HIGH if labs.total_cholesterol >= 240 else RiskLevel.MODERATE
            self.findings.append(DiagnosticFinding(
                category="Lipid Profile",
                parameter="Total Cholesterol",
                value=labs.total_cholesterol,
                normal_range="<200 mg/dL",
                status=status,
                interpretation="Hypercholesterolemia - increased cardiovascular risk",
                recommendations=["Low-fat diet", "Regular exercise", "Statin therapy consideration"]
            ))
            conditions.append({
                "condition": "Hyperlipidemia",
                "confidence": "High",
                "description": "Elevated cholesterol increases risk of heart disease and stroke"
            })
        
        # LDL Cholesterol
        if labs.ldl_cholesterol and labs.ldl_cholesterol >= 130:
            status = RiskLevel.HIGH if labs.ldl_cholesterol >= 160 else RiskLevel.MODERATE
            self.findings.append(DiagnosticFinding(
                category="Lipid Profile",
                parameter="LDL Cholesterol",
                value=labs.ldl_cholesterol,
                normal_range="<100 mg/dL",
                status=status,
                interpretation="Elevated 'bad' cholesterol",
                recommendations=["Reduce saturated fats", "Increase fiber intake", "Consider medication"]
            ))
        
        # HDL Cholesterol (protective)
        if labs.hdl_cholesterol and labs.hdl_cholesterol < 40:
            self.findings.append(DiagnosticFinding(
                category="Lipid Profile",
                parameter="HDL Cholesterol",
                value=labs.hdl_cholesterol,
                normal_range=">40 mg/dL (men), >50 mg/dL (women)",
                status=RiskLevel.MODERATE,
                interpretation="Low 'good' cholesterol - reduced cardiovascular protection",
                recommendations=["Increase physical activity", "Omega-3 fatty acids", "Quit smoking if applicable"]
            ))
        
        # Anemia detection
        if labs.hemoglobin:
            low_hb = (gender == "male" and labs.hemoglobin < 13.5) or \
                     (gender == "female" and labs.hemoglobin < 12.0)
            if low_hb:
                status = RiskLevel.HIGH if labs.hemoglobin < 10 else RiskLevel.MODERATE
                self.findings.append(DiagnosticFinding(
                    category="Complete Blood Count",
                    parameter="Hemoglobin",
                    value=labs.hemoglobin,
                    normal_range="13.5-17.5 g/dL (men), 12.0-15.5 g/dL (women)",
                    status=status,
                    interpretation="Anemia detected",
                    recommendations=["Iron-rich diet", "Iron supplements", "Check for bleeding sources"]
                ))
                conditions.append({
                    "condition": "Anemia",
                    "confidence": "High",
                    "description": "Low hemoglobin can cause fatigue and weakness"
                })
        
        # Kidney Function
        if labs.creatinine:
            elevated = (gender == "male" and labs.creatinine > 1.3) or \
                      (gender == "female" and labs.creatinine > 1.1)
            if elevated:
                status = RiskLevel.HIGH if labs.creatinine > 2.0 else RiskLevel.MODERATE
                self.findings.append(DiagnosticFinding(
                    category="Kidney Function",
                    parameter="Creatinine",
                    value=labs.creatinine,
                    normal_range="0.7-1.3 mg/dL (men), 0.6-1.1 mg/dL (women)",
                    status=status,
                    interpretation="Possible kidney dysfunction",
                    recommendations=["Kidney function tests", "Monitor hydration", "Nephrology consultation"]
                ))
                conditions.append({
                    "condition": "Chronic Kidney Disease (suspected)",
                    "confidence": "Moderate",
                    "description": "Elevated creatinine may indicate impaired kidney function"
                })
        
        # Liver Function
        if labs.sgot_ast and labs.sgot_ast > 40:
            status = RiskLevel.HIGH if labs.sgot_ast > 100 else RiskLevel.MODERATE
            self.findings.append(DiagnosticFinding(
                category="Liver Function",
                parameter="SGOT/AST",
                value=labs.sgot_ast,
                normal_range="10-40 U/L",
                status=status,
                interpretation="Elevated liver enzymes",
                recommendations=["Liver ultrasound", "Avoid alcohol", "Hepatology consultation"]
            ))
        
        if labs.sgpt_alt and labs.sgpt_alt > 41:
            status = RiskLevel.HIGH if labs.sgpt_alt > 100 else RiskLevel.MODERATE
            self.findings.append(DiagnosticFinding(
                category="Liver Function",
                parameter="SGPT/ALT",
                value=labs.sgpt_alt,
                normal_range="7-41 U/L",
                status=status,
                interpretation="Liver stress or damage",
                recommendations=["Repeat liver function tests", "Viral hepatitis screening", "Avoid hepatotoxic drugs"]
            ))
            conditions.append({
                "condition": "Liver Disease (suspected)",
                "confidence": "Moderate",
                "description": "Elevated liver enzymes suggest liver inflammation or damage"
            })
        
        # Thyroid
        if labs.tsh:
            if labs.tsh < 0.4:
                self.findings.append(DiagnosticFinding(
                    category="Thyroid Function",
                    parameter="TSH",
                    value=labs.tsh,
                    normal_range="0.4-4.0 mIU/L",
                    status=RiskLevel.MODERATE,
                    interpretation="Hyperthyroidism (overactive thyroid)",
                    recommendations=["Thyroid hormone levels (T3, T4)", "Endocrinology referral", "Thyroid ultrasound"]
                ))
                conditions.append({
                    "condition": "Hyperthyroidism",
                    "confidence": "Moderate",
                    "description": "Low TSH suggests overactive thyroid"
                })
            elif labs.tsh > 4.0:
                status = RiskLevel.MODERATE if labs.tsh < 10 else RiskLevel.HIGH
                self.findings.append(DiagnosticFinding(
                    category="Thyroid Function",
                    parameter="TSH",
                    value=labs.tsh,
                    normal_range="0.4-4.0 mIU/L",
                    status=status,
                    interpretation="Hypothyroidism (underactive thyroid)",
                    recommendations=["Thyroid hormone replacement", "Repeat TSH in 6-8 weeks", "Monitor symptoms"]
                ))
                conditions.append({
                    "condition": "Hypothyroidism",
                    "confidence": "High" if labs.tsh > 10 else "Moderate",
                    "description": "Elevated TSH indicates underactive thyroid"
                })
        
        # Infection markers
        if labs.wbc_count:
            if labs.wbc_count > 11000:
                status = RiskLevel.HIGH if labs.wbc_count > 15000 else RiskLevel.MODERATE
                self.findings.append(DiagnosticFinding(
                    category="Complete Blood Count",
                    parameter="WBC Count",
                    value=labs.wbc_count,
                    normal_range="4,000-11,000 cells/μL",
                    status=status,
                    interpretation="Leukocytosis - possible infection or inflammation",
                    recommendations=["Identify infection source", "Blood culture if fever present", "Monitor closely"]
                ))
            elif labs.wbc_count < 4000:
                self.findings.append(DiagnosticFinding(
                    category="Complete Blood Count",
                    parameter="WBC Count",
                    value=labs.wbc_count,
                    normal_range="4,000-11,000 cells/μL",
                    status=RiskLevel.MODERATE,
                    interpretation="Leukopenia - reduced white blood cells",
                    recommendations=["Check for bone marrow issues", "Review medications", "Hematology consultation"]
                ))
        
        # Vitamin deficiencies
        if labs.vitamin_d and labs.vitamin_d < 20:
            status = RiskLevel.MODERATE if labs.vitamin_d < 12 else RiskLevel.LOW
            self.findings.append(DiagnosticFinding(
                category="Vitamins",
                parameter="Vitamin D",
                value=labs.vitamin_d,
                normal_range="20-50 ng/mL",
                status=status,
                interpretation="Vitamin D deficiency",
                recommendations=["Vitamin D supplementation", "Sunlight exposure", "Calcium intake"]
            ))
        
        if labs.vitamin_b12 and labs.vitamin_b12 < 200:
            self.findings.append(DiagnosticFinding(
                category="Vitamins",
                parameter="Vitamin B12",
                value=labs.vitamin_b12,
                normal_range="200-900 pg/mL",
                status=RiskLevel.MODERATE,
                interpretation="Vitamin B12 deficiency",
                recommendations=["B12 supplementation (oral or injections)", "Check for pernicious anemia", "Dietary assessment"]
            ))
        
        return conditions
    
    def _analyze_symptoms(self, symptoms, labs: LabResults) -> List[Dict[str, str]]:
        """Correlate symptoms with lab findings"""
        conditions = []
        symptom_text = symptoms.chief_complaint.lower() + " " + " ".join(symptoms.symptoms_list).lower()
        
        # Diabetes symptoms
        if any(word in symptom_text for word in ["thirst", "urination", "frequent urination", "hunger", "fatigue"]):
            if labs and labs.fasting_glucose and labs.fasting_glucose > 100:
                conditions.append({
                    "condition": "Diabetes Mellitus",
                    "confidence": "High",
                    "description": "Classic diabetic symptoms with elevated blood sugar"
                })
        
        # Thyroid symptoms
        if any(word in symptom_text for word in ["weight loss", "anxiety", "tremor", "palpitation"]):
            conditions.append({
                "condition": "Hyperthyroidism",
                "confidence": "Moderate",
                "description": "Symptoms consistent with overactive thyroid - TSH test needed"
            })
        
        if any(word in symptom_text for word in ["weight gain", "cold intolerance", "constipation", "fatigue"]):
            conditions.append({
                "condition": "Hypothyroidism",
                "confidence": "Moderate",
                "description": "Symptoms consistent with underactive thyroid - TSH test needed"
            })
        
        # Anemia symptoms
        if any(word in symptom_text for word in ["fatigue", "weakness", "pale", "dizziness", "shortness of breath"]):
            if labs and labs.hemoglobin and labs.hemoglobin < 12:
                conditions.append({
                    "condition": "Anemia",
                    "confidence": "High",
                    "description": "Fatigue and weakness with low hemoglobin"
                })
        
        # Cardiac symptoms
        if any(word in symptom_text for word in ["chest pain", "breathlessness", "palpitation"]):
            conditions.append({
                "condition": "Cardiovascular Disease (suspected)",
                "confidence": "Moderate",
                "description": "Cardiac symptoms - ECG and cardiac markers recommended"
            })
        
        return conditions
    
    def _assess_blood_pressure(self, systolic: int, diastolic: int) -> Tuple[RiskLevel, str, List[str]]:
        """Assess blood pressure status"""
        if systolic >= 180 or diastolic >= 120:
            return (
                RiskLevel.CRITICAL,
                "Hypertensive Crisis - immediate medical attention required",
                ["Seek emergency care immediately", "May need hospitalization", "Risk of stroke/heart attack"]
            )
        elif systolic >= 140 or diastolic >= 90:
            return (
                RiskLevel.HIGH,
                "Hypertension (High Blood Pressure) - Stage 2",
                ["Antihypertensive medication needed", "Low sodium diet", "Regular monitoring"]
            )
        elif systolic >= 130 or diastolic >= 80:
            return (
                RiskLevel.MODERATE,
                "Hypertension (High Blood Pressure) - Stage 1",
                ["Lifestyle modifications", "Monitor regularly", "Consider medication"]
            )
        elif systolic < 90 or diastolic < 60:
            return (
                RiskLevel.MODERATE,
                "Hypotension (Low Blood Pressure)",
                ["Increase fluid intake", "Avoid sudden position changes", "Monitor symptoms"]
            )
        return (RiskLevel.NORMAL, "Normal blood pressure", [])
    
    def _assess_bmi(self, bmi: float) -> Tuple[RiskLevel, str, List[str]]:
        """Assess BMI status"""
        if bmi < 18.5:
            return (
                RiskLevel.MODERATE,
                "Underweight",
                ["Increase caloric intake", "Nutritionist consultation", "Rule out underlying conditions"]
            )
        elif 25 <= bmi < 30:
            return (
                RiskLevel.LOW,
                "Overweight",
                ["Balanced diet", "Regular exercise", "Weight management program"]
            )
        elif bmi >= 30:
            status = RiskLevel.HIGH if bmi >= 35 else RiskLevel.MODERATE
            return (
                status,
                f"Obesity {'(Class II or higher)' if bmi >= 35 else '(Class I)'}",
                ["Weight loss program", "Dietitian consultation", "Exercise regimen", "Screen for metabolic syndrome"]
            )
        return (RiskLevel.NORMAL, "Normal weight", [])
    
    def _calculate_overall_risk(self) -> RiskLevel:
        """Calculate overall risk level based on all findings"""
        if not self.findings:
            return RiskLevel.NORMAL
        
        risk_scores = {
            RiskLevel.NORMAL: 0,
            RiskLevel.LOW: 1,
            RiskLevel.MODERATE: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4
        }
        
        max_risk = max([risk_scores[f.status] for f in self.findings])
        
        for level, score in risk_scores.items():
            if score == max_risk:
                return level
        
        return RiskLevel.NORMAL
    
    def _generate_immediate_actions(self) -> List[str]:
        """Generate immediate action items"""
        actions = []
        
        critical_findings = [f for f in self.findings if f.status == RiskLevel.CRITICAL]
        high_findings = [f for f in self.findings if f.status == RiskLevel.HIGH]
        
        if critical_findings:
            actions.append("⚠️ IMMEDIATE MEDICAL ATTENTION REQUIRED")
            for finding in critical_findings:
                actions.append(f"• Address {finding.parameter}: {finding.interpretation}")
        
        if high_findings:
            actions.append("High-priority items requiring prompt attention:")
            for finding in high_findings[:3]:  # Top 3 high-risk items
                actions.append(f"• {finding.parameter}: {finding.recommendations[0]}")
        
        return actions if actions else ["No immediate actions required"]
    
    def _recommend_followup_tests(self) -> List[str]:
        """Recommend follow-up tests based on findings"""
        tests = set()
        
        for finding in self.findings:
            if "diabetes" in finding.interpretation.lower() or "glucose" in finding.parameter.lower():
                tests.add("HbA1c test (if not done)")
                tests.add("Oral Glucose Tolerance Test")
            
            if "kidney" in finding.interpretation.lower():
                tests.add("Complete Metabolic Panel")
                tests.add("Urinalysis")
                tests.add("Kidney Ultrasound")
            
            if "liver" in finding.interpretation.lower():
                tests.add("Complete Liver Function Panel")
                tests.add("Viral Hepatitis Screening")
                tests.add("Liver Ultrasound")
            
            if "thyroid" in finding.interpretation.lower():
                tests.add("Complete Thyroid Panel (TSH, T3, T4)")
                tests.add("Thyroid Antibodies")
            
            if "anemia" in finding.interpretation.lower():
                tests.add("Iron Studies (Serum Iron, Ferritin, TIBC)")
                tests.add("Peripheral Blood Smear")
            
            if "heart" in finding.interpretation.lower() or "cardiac" in finding.interpretation.lower():
                tests.add("ECG (Electrocardiogram)")
                tests.add("Echocardiogram")
                tests.add("Cardiac Enzyme Tests")
        
        return list(tests) if tests else ["Regular health checkup in 6 months"]
    
    def _generate_recommendations(self, patient: Patient) -> List[str]:
        """Generate general health recommendations"""
        recommendations = []
        
        # Based on age
        if patient.age > 40:
            recommendations.append("Annual comprehensive health screening recommended")
        
        # Based on BMI
        if patient.vital_signs:
            bmi = patient.vital_signs.get_bmi()
            if bmi >= 25:
                recommendations.append("Weight management program with diet and exercise")
        
        # Based on findings
        has_diabetes_risk = any("diabetes" in f.interpretation.lower() for f in self.findings)
        has_cardiac_risk = any("cardio" in f.interpretation.lower() or "cholesterol" in f.interpretation.lower() for f in self.findings)
        
        if has_diabetes_risk or has_cardiac_risk:
            recommendations.extend([
                "Mediterranean or DASH diet recommended",
                "30 minutes of moderate exercise 5 days/week",
                "Stress management and adequate sleep (7-8 hours)"
            ])
        
        # Medical history considerations
        if patient.medical_history:
            if patient.medical_history.smoking:
                recommendations.append("Smoking cessation program strongly recommended")
            if patient.medical_history.alcohol_consumption:
                recommendations.append("Limit alcohol consumption")
        
        recommendations.append("Regular follow-up with primary care physician")
        recommendations.append("Maintain hydration (8-10 glasses of water daily)")
        
        return recommendations
    
    def _generate_summary(self, patient: Patient, overall_risk: RiskLevel) -> str:
        """Generate executive summary"""
        critical_count = len([f for f in self.findings if f.status == RiskLevel.CRITICAL])
        high_count = len([f for f in self.findings if f.status == RiskLevel.HIGH])
        moderate_count = len([f for f in self.findings if f.status == RiskLevel.MODERATE])
        
        summary = f"Diagnostic Analysis for Patient {patient.name} (ID: {patient.patient_id})\n\n"
        summary += f"Overall Risk Level: {overall_risk.value.upper()}\n\n"
        
        if critical_count > 0:
            summary += f"⚠️ CRITICAL: {critical_count} critical finding(s) requiring immediate attention.\n"
        if high_count > 0:
            summary += f"⚠️ HIGH: {high_count} high-priority finding(s) requiring prompt medical attention.\n"
        if moderate_count > 0:
            summary += f"⚠️ MODERATE: {moderate_count} finding(s) requiring monitoring and lifestyle modifications.\n"
        
        if not self.findings:
            summary += "No significant abnormalities detected. All parameters within normal ranges.\n"
        else:
            summary += f"\nTotal findings: {len(self.findings)}\n"
            summary += "Key areas of concern: " + ", ".join(set([f.category for f in self.findings])) + "\n"
        
        summary += "\nThis is an automated preliminary analysis. Please consult with a healthcare professional for proper diagnosis and treatment."
        
        return summary
