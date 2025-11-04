# 🏥 Automated Diagnostic System

An intelligent medical diagnostic system that automatically analyzes patient information and lab reports to provide diagnostic insights, risk assessment, and treatment recommendations.

## 🎯 Problem Statement

In hospitals and clinics, patient information and lab reports are often checked manually by doctors or staff to identify health issues. This process can be:
- ⏰ Time-consuming
- ❌ Prone to human errors
- 📉 Causes delays in diagnosis
- 💼 Increases workload on medical staff

## 💡 Solution

The **Automated Diagnostic System** solves these problems by:
- ✅ Automatically analyzing patient data and lab results
- 🔍 Identifying abnormal values and health risks
- 📊 Generating comprehensive diagnostic reports
- ⚡ Providing immediate risk assessment
- 💊 Suggesting follow-up tests and recommendations
- 🎯 Reducing manual effort and speeding up diagnosis

## 🌟 Features

### Core Capabilities
- **Vital Signs Analysis**: Temperature, blood pressure, heart rate, oxygen saturation, BMI
- **Lab Report Analysis**: Complete blood count, blood sugar, lipid profile, kidney/liver function, thyroid
- **Disease Detection**: Diabetes, hypertension, anemia, thyroid disorders, cardiovascular risks
- **Risk Assessment**: Normal, Low, Moderate, High, Critical risk levels
- **Intelligent Recommendations**: Personalized treatment suggestions and lifestyle modifications
- **Symptom Correlation**: Links symptoms with lab findings for better diagnosis

### Technical Features
- **Web-based Interface**: User-friendly form for data input
- **REST API**: JSON-based API for integration with other systems
- **Real-time Analysis**: Instant diagnostic reports
- **Comprehensive Reports**: Detailed findings with interpretations
- **Multiple Test Support**: CBC, metabolic panel, lipid profile, thyroid panel, vitamins

## 🏗️ Project Structure

```
Mkce/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── patient_model.py          # Data models for patient information
│   └── diagnostic_engine.py      # Core diagnostic analysis engine
├── frontend/
│   └── index.html                # Web interface
├── data/
│   ├── sample_patient_diabetic.json
│   └── sample_patient_anemia_thyroid.json
├── tests/
│   └── test_diagnostic_engine.py # Test suite
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/venkat2005code/Mkce.git
cd Mkce
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the server**
```bash
cd backend
python app.py
```

4. **Access the application**
Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage

### Web Interface

1. **Open** the web interface at `http://localhost:5000`
2. **Fill in** patient information:
   - Basic Information (name, age, gender)
   - Vital Signs (temperature, blood pressure, heart rate, etc.)
   - Lab Results (glucose, cholesterol, hemoglobin, etc.)
   - Symptoms (complaints and symptom list)
3. **Click** "Analyze Patient Data"
4. **View** the comprehensive diagnostic report with:
   - Overall risk assessment
   - Detailed findings
   - Possible conditions
   - Immediate actions
   - Follow-up test recommendations
   - General health recommendations

### API Usage

**Endpoint**: `POST /api/analyze`

**Request Body**:
```json
{
  "name": "John Doe",
  "age": 45,
  "gender": "male",
  "vital_signs": {
    "temperature": 37.2,
    "blood_pressure_systolic": 145,
    "blood_pressure_diastolic": 92,
    "heart_rate": 78,
    "oxygen_saturation": 97.5,
    "weight": 85.5,
    "height": 175
  },
  "lab_results": {
    "fasting_glucose": 135,
    "hba1c": 6.8,
    "total_cholesterol": 245,
    "hemoglobin": 13.2
  }
}
```

**Response**:
```json
{
  "success": true,
  "patient_id": "P20251104123456",
  "report": {
    "overall_risk": "high",
    "findings": [...],
    "possible_conditions": [...],
    "immediate_actions": [...],
    "recommendations": [...]
  }
}
```

### Using Sample Data

Test the system with provided sample data:

```bash
# Test with diabetic patient
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d @data/sample_patient_diabetic.json

# Test with anemia/thyroid patient
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d @data/sample_patient_anemia_thyroid.json
```

## 🧪 Testing

Run the automated test suite:

```bash
cd tests
python test_diagnostic_engine.py
```

The test suite includes:
- ✓ Diabetes detection
- ✓ Hypertension detection
- ✓ Anemia detection
- ✓ Normal patient verification
- ✓ Critical condition detection

## 📊 Detection Capabilities

### Conditions Detected
- **Diabetes Mellitus**: Based on fasting glucose and HbA1c levels
- **Prediabetes**: Impaired fasting glucose
- **Hypertension**: Stage 1, Stage 2, and Hypertensive Crisis
- **Hyperlipidemia**: Elevated cholesterol and triglycerides
- **Anemia**: Low hemoglobin levels
- **Thyroid Disorders**: Hypothyroidism and Hyperthyroidism
- **Kidney Disease**: Based on creatinine levels
- **Liver Disease**: Elevated liver enzymes
- **Vitamin Deficiencies**: Vitamin D and B12
- **Infections**: Elevated WBC count
- **Obesity/Underweight**: BMI-based assessment
- **Cardiovascular Risk**: Multiple risk factors

### Risk Levels
- 🟢 **Normal**: All parameters within normal range
- 🟡 **Low**: Minor abnormalities requiring monitoring
- 🟠 **Moderate**: Requires lifestyle changes and follow-up
- 🔴 **High**: Requires medical attention and treatment
- ⚫ **Critical**: Immediate medical attention required

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/health` | GET | Health check |
| `/api/analyze` | POST | Analyze patient data |
| `/api/patient/<id>` | GET | Get patient by ID |
| `/api/patients` | GET | List all patients |

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Processing**: Custom diagnostic algorithms
- **API**: RESTful JSON API
- **Architecture**: Rule-based expert system with pattern recognition

## 📈 Future Enhancements

- [ ] Machine Learning models for improved accuracy
- [ ] Integration with Electronic Health Records (EHR)
- [ ] PDF report generation
- [ ] Email notifications for critical conditions
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Doctor dashboard for multiple patients
- [ ] Historical trend analysis
- [ ] Drug interaction checking
- [ ] Imaging analysis (X-rays, CT scans)

## ⚠️ Disclaimer

**IMPORTANT**: This is an automated preliminary analysis tool designed to assist healthcare professionals. It should NOT be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for proper medical care.

## 👨‍💻 Development

### Adding New Tests
Add new lab parameters in `backend/patient_model.py`:
```python
class LabResults:
    new_parameter: Optional[float] = None
```

### Adding New Diagnostic Rules
Extend the diagnostic engine in `backend/diagnostic_engine.py`:
```python
def _analyze_labs(self, labs: LabResults, age: int, gender: str):
    # Add your diagnostic logic here
    pass
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for better healthcare**
