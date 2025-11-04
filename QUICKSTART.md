# Quick Reference Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
cd backend
python app.py
```

### Step 3: Open Browser
Navigate to: `http://localhost:5000`

---

## 📝 Common Use Cases

### Analyzing a New Patient

1. **Fill Basic Info**: Name, age, gender
2. **Enter Vital Signs**: BP, temperature, heart rate, etc.
3. **Add Lab Results**: Blood sugar, cholesterol, hemoglobin, etc.
4. **Describe Symptoms**: Chief complaint and symptom list
5. **Click "Analyze"**: Get instant diagnostic report

### Using the API

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Patient Name",
    "age": 45,
    "gender": "male",
    "vital_signs": {
      "blood_pressure_systolic": 140,
      "blood_pressure_diastolic": 90
    },
    "lab_results": {
      "fasting_glucose": 130
    }
  }'
```

---

## 🔬 Normal Lab Values Reference

### Vital Signs
| Parameter | Normal Range |
|-----------|-------------|
| Temperature | 36.5-37.5°C |
| Blood Pressure | 90-120/60-80 mmHg |
| Heart Rate | 60-100 bpm |
| Oxygen Saturation | 95-100% |
| BMI | 18.5-24.9 |

### Complete Blood Count (CBC)
| Parameter | Normal Range |
|-----------|-------------|
| Hemoglobin (Male) | 13.5-17.5 g/dL |
| Hemoglobin (Female) | 12.0-15.5 g/dL |
| WBC Count | 4,000-11,000 cells/μL |
| Platelet Count | 150,000-400,000 cells/μL |

### Blood Sugar
| Parameter | Normal Range |
|-----------|-------------|
| Fasting Glucose | 70-99 mg/dL |
| Random Glucose | <140 mg/dL |
| HbA1c | <5.7% |

### Lipid Profile
| Parameter | Normal Range |
|-----------|-------------|
| Total Cholesterol | <200 mg/dL |
| LDL Cholesterol | <100 mg/dL |
| HDL Cholesterol | >40 mg/dL (men), >50 mg/dL (women) |
| Triglycerides | <150 mg/dL |

### Kidney Function
| Parameter | Normal Range |
|-----------|-------------|
| Creatinine (Male) | 0.7-1.3 mg/dL |
| Creatinine (Female) | 0.6-1.1 mg/dL |
| BUN | 7-20 mg/dL |

### Liver Function
| Parameter | Normal Range |
|-----------|-------------|
| SGOT/AST | 10-40 U/L |
| SGPT/ALT | 7-41 U/L |
| Bilirubin | 0.1-1.2 mg/dL |

### Thyroid Function
| Parameter | Normal Range |
|-----------|-------------|
| TSH | 0.4-4.0 mIU/L |
| T3 | 80-200 ng/dL |
| T4 | 5-12 μg/dL |

---

## 🎯 Risk Level Interpretation

| Risk Level | Meaning | Action |
|------------|---------|--------|
| 🟢 Normal | All values within range | Routine checkup |
| 🟡 Low | Minor issues | Monitor |
| 🟠 Moderate | Needs attention | Lifestyle changes + follow-up |
| 🔴 High | Serious concern | Medical treatment required |
| ⚫ Critical | Emergency | Immediate medical attention |

---

## 🩺 Common Conditions Detected

### Diabetes
- **Indicators**: Fasting glucose ≥126 mg/dL or HbA1c ≥6.5%
- **Symptoms**: Increased thirst, frequent urination, fatigue
- **Action**: Endocrinologist consultation, lifestyle modifications

### Hypertension
- **Indicators**: BP ≥130/80 mmHg
- **Symptoms**: Often asymptomatic, headache, dizziness
- **Action**: Low sodium diet, medication, regular monitoring

### Anemia
- **Indicators**: Hemoglobin <13.5 (men) or <12.0 (women) g/dL
- **Symptoms**: Fatigue, weakness, pale skin, shortness of breath
- **Action**: Iron supplementation, dietary changes, find cause

### Hyperlipidemia
- **Indicators**: Total cholesterol ≥200 mg/dL or LDL ≥130 mg/dL
- **Symptoms**: Usually asymptomatic
- **Action**: Low-fat diet, exercise, statin therapy

### Thyroid Disorders
- **Hypothyroidism**: TSH >4.0 mIU/L
  - Symptoms: Fatigue, weight gain, cold intolerance
- **Hyperthyroidism**: TSH <0.4 mIU/L
  - Symptoms: Weight loss, anxiety, palpitations

---

## 🧪 Recommended Follow-up Tests

Based on findings, the system may recommend:

- **For Diabetes**: Oral Glucose Tolerance Test, Insulin levels
- **For Kidney Issues**: Complete Metabolic Panel, Urinalysis, Kidney ultrasound
- **For Liver Issues**: Viral Hepatitis screening, Liver ultrasound
- **For Thyroid**: Complete Thyroid Panel, Thyroid antibodies, Thyroid ultrasound
- **For Anemia**: Iron studies, Vitamin B12, Folate levels
- **For Cardiac Risk**: ECG, Echocardiogram, Cardiac enzyme tests

---

## 🛠️ Troubleshooting

### Server Won't Start
```bash
# Check if Python is installed
python3 --version

# Install dependencies
pip3 install flask flask-cors

# Try running with python instead of python3
python backend/app.py
```

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or change port in app.py:
# app.run(debug=True, host='0.0.0.0', port=5001)
```

### Import Errors
```bash
# Make sure you're in the correct directory
cd backend
python app.py

# Or run from root with proper path
cd "hack chennai"
python backend/app.py
```

---

## 📊 API Response Example

```json
{
  "success": true,
  "patient_id": "P20251104123456",
  "report": {
    "overall_risk": "high",
    "summary": "Diagnostic Analysis for Patient...",
    "findings": [
      {
        "category": "Blood Sugar",
        "parameter": "Fasting Glucose",
        "value": 135,
        "normal_range": "70-99 mg/dL",
        "status": "high",
        "interpretation": "Diabetes Mellitus",
        "recommendations": [
          "HbA1c test recommended",
          "Lifestyle modifications",
          "Consult endocrinologist"
        ]
      }
    ],
    "possible_conditions": [
      {
        "condition": "Diabetes Mellitus",
        "confidence": "High",
        "description": "Elevated blood sugar levels indicate glucose metabolism issues"
      }
    ],
    "immediate_actions": [
      "High-priority items requiring prompt attention:",
      "• Fasting Glucose: HbA1c test recommended"
    ],
    "follow_up_tests": [
      "HbA1c test (if not done)",
      "Oral Glucose Tolerance Test"
    ],
    "general_recommendations": [
      "Mediterranean or DASH diet recommended",
      "30 minutes of moderate exercise 5 days/week",
      "Regular follow-up with primary care physician"
    ]
  }
}
```

---

## 💡 Pro Tips

1. **Complete Data = Better Analysis**: The more information provided, the more accurate the diagnosis
2. **Use Sample Data**: Test with provided JSON files in `data/` folder
3. **Run Tests First**: Always run `python tests/test_diagnostic_engine.py` to verify system
4. **Check Normal Ranges**: Refer to the normal values table when entering data
5. **Follow Recommendations**: The system provides actionable next steps
6. **Consult Doctors**: This is a tool to assist, not replace medical professionals

---

## 📞 Need Help?

- **Documentation**: Check README.md and ARCHITECTURE.md
- **Issues**: Open an issue on GitHub
- **Tests**: Run test suite for debugging: `python tests/test_diagnostic_engine.py`

---

**Remember**: This system is a diagnostic aid. Always consult qualified healthcare professionals for medical decisions.
