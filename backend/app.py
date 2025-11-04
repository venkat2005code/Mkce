"""
Flask API Server for Automated Diagnostic System
Provides REST endpoints for patient data submission and diagnostic analysis
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from patient_model import (
    Patient, VitalSigns, LabResults, MedicalHistory, 
    Symptoms, Gender, BloodGroup
)
from diagnostic_engine import DiagnosticEngine
from datetime import datetime
import json

app = Flask(__name__, 
            template_folder='../frontend',
            static_folder='../frontend/static')
CORS(app)

# Initialize diagnostic engine
diagnostic_engine = DiagnosticEngine()

# In-memory storage (in production, use a database)
patients_db = {}


@app.route('/')
def index():
    """Serve main web interface"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Automated Diagnostic System",
        "version": "1.0.0"
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_patient():
    """
    Main endpoint for patient analysis
    Expects JSON with patient data
    """
    try:
        data = request.json
        
        # Create patient object from request data
        patient = _create_patient_from_json(data)
        
        # Store patient data
        patients_db[patient.patient_id] = patient
        
        # Run diagnostic analysis
        report = diagnostic_engine.analyze_patient(patient)
        
        # Convert report to JSON-serializable format
        response = _report_to_dict(report)
        
        return jsonify({
            "success": True,
            "patient_id": patient.patient_id,
            "report": response
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


@app.route('/api/patient/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient data by ID"""
    if patient_id in patients_db:
        patient = patients_db[patient_id]
        return jsonify({
            "success": True,
            "patient": patient.to_dict()
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": "Patient not found"
        }), 404


@app.route('/api/patients', methods=['GET'])
def list_patients():
    """List all patients"""
    patients_list = [
        {
            "patient_id": p.patient_id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender.value,
            "timestamp": p.timestamp.isoformat()
        }
        for p in patients_db.values()
    ]
    return jsonify({
        "success": True,
        "count": len(patients_list),
        "patients": patients_list
    }), 200


def _create_patient_from_json(data):
    """Convert JSON data to Patient object"""
    
    # Basic info
    patient_id = data.get('patient_id', f"P{datetime.now().strftime('%Y%m%d%H%M%S')}")
    name = data['name']
    age = int(data['age'])
    gender = Gender(data['gender'])
    
    blood_group = None
    if 'blood_group' in data and data['blood_group']:
        blood_group = BloodGroup(data['blood_group'])
    
    # Vital signs
    vital_signs = None
    if 'vital_signs' in data:
        vs = data['vital_signs']
        vital_signs = VitalSigns(
            temperature=float(vs.get('temperature', 37.0)),
            blood_pressure_systolic=int(vs.get('blood_pressure_systolic', 120)),
            blood_pressure_diastolic=int(vs.get('blood_pressure_diastolic', 80)),
            heart_rate=int(vs.get('heart_rate', 72)),
            respiratory_rate=int(vs.get('respiratory_rate', 16)),
            oxygen_saturation=float(vs.get('oxygen_saturation', 98)),
            weight=float(vs.get('weight', 70)),
            height=float(vs.get('height', 170))
        )
    
    # Lab results
    lab_results = None
    if 'lab_results' in data:
        lr = data['lab_results']
        lab_results = LabResults(
            hemoglobin=_get_float(lr, 'hemoglobin'),
            wbc_count=_get_float(lr, 'wbc_count'),
            platelet_count=_get_float(lr, 'platelet_count'),
            rbc_count=_get_float(lr, 'rbc_count'),
            fasting_glucose=_get_float(lr, 'fasting_glucose'),
            random_glucose=_get_float(lr, 'random_glucose'),
            hba1c=_get_float(lr, 'hba1c'),
            total_cholesterol=_get_float(lr, 'total_cholesterol'),
            ldl_cholesterol=_get_float(lr, 'ldl_cholesterol'),
            hdl_cholesterol=_get_float(lr, 'hdl_cholesterol'),
            triglycerides=_get_float(lr, 'triglycerides'),
            creatinine=_get_float(lr, 'creatinine'),
            bun=_get_float(lr, 'bun'),
            uric_acid=_get_float(lr, 'uric_acid'),
            sgot_ast=_get_float(lr, 'sgot_ast'),
            sgpt_alt=_get_float(lr, 'sgpt_alt'),
            bilirubin_total=_get_float(lr, 'bilirubin_total'),
            tsh=_get_float(lr, 'tsh'),
            t3=_get_float(lr, 't3'),
            t4=_get_float(lr, 't4'),
            sodium=_get_float(lr, 'sodium'),
            potassium=_get_float(lr, 'potassium'),
            vitamin_d=_get_float(lr, 'vitamin_d'),
            vitamin_b12=_get_float(lr, 'vitamin_b12')
        )
    
    # Medical history
    medical_history = None
    if 'medical_history' in data:
        mh = data['medical_history']
        medical_history = MedicalHistory(
            chronic_conditions=mh.get('chronic_conditions', []),
            allergies=mh.get('allergies', []),
            current_medications=mh.get('current_medications', []),
            past_surgeries=mh.get('past_surgeries', []),
            family_history=mh.get('family_history', []),
            smoking=mh.get('smoking', False),
            alcohol_consumption=mh.get('alcohol_consumption', False)
        )
    
    # Symptoms
    symptoms = None
    if 'symptoms' in data:
        s = data['symptoms']
        symptoms = Symptoms(
            chief_complaint=s.get('chief_complaint', ''),
            symptoms_list=s.get('symptoms_list', []),
            duration_days=int(s.get('duration_days', 0)),
            severity=s.get('severity', 'moderate')
        )
    
    return Patient(
        patient_id=patient_id,
        name=name,
        age=age,
        gender=gender,
        blood_group=blood_group,
        contact=data.get('contact', ''),
        vital_signs=vital_signs,
        lab_results=lab_results,
        medical_history=medical_history,
        symptoms=symptoms
    )


def _get_float(data, key):
    """Safely get float value from dict"""
    value = data.get(key)
    if value is not None and value != '':
        return float(value)
    return None


def _report_to_dict(report):
    """Convert diagnostic report to dictionary"""
    return {
        "patient_id": report.patient_id,
        "overall_risk": report.overall_risk.value,
        "summary": report.summary,
        "findings": [
            {
                "category": f.category,
                "parameter": f.parameter,
                "value": f.value,
                "normal_range": f.normal_range,
                "status": f.status.value,
                "interpretation": f.interpretation,
                "recommendations": f.recommendations
            }
            for f in report.findings
        ],
        "possible_conditions": report.possible_conditions,
        "immediate_actions": report.immediate_actions,
        "follow_up_tests": report.follow_up_tests,
        "general_recommendations": report.general_recommendations
    }


if __name__ == '__main__':
    print("=" * 60)
    print("Automated Diagnostic System - API Server")
    print("=" * 60)
    print("Server starting on http://localhost:8080")
    print("Access web interface at: http://localhost:8080")
    print("API documentation: http://localhost:8080/api/health")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=8080)
