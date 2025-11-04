# System Architecture

## Overview
The Automated Diagnostic System uses a 3-tier architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                   (Web Browser)                             │
│                                                             │
│  • Patient Data Input Forms                                │
│  • Real-time Diagnostic Reports                            │
│  • Risk Assessment Visualization                           │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/JSON
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                    API LAYER                                │
│                  (Flask Server)                             │
│                                                             │
│  • REST Endpoints                                           │
│  • Request Validation                                       │
│  • Response Formatting                                      │
│  • Patient Data Management                                  │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                 BUSINESS LOGIC                              │
│              (Diagnostic Engine)                            │
│                                                             │
│  ┌─────────────────────────────────────────────┐          │
│  │  Patient Data Model                         │          │
│  │  • VitalSigns                               │          │
│  │  • LabResults                               │          │
│  │  • MedicalHistory                           │          │
│  │  • Symptoms                                 │          │
│  └─────────────────────────────────────────────┘          │
│                                                             │
│  ┌─────────────────────────────────────────────┐          │
│  │  Diagnostic Engine                          │          │
│  │  • Vital Signs Analyzer                     │          │
│  │  • Lab Results Analyzer                     │          │
│  │  • Symptom Correlator                       │          │
│  │  • Risk Calculator                          │          │
│  │  • Recommendation Generator                 │          │
│  └─────────────────────────────────────────────┘          │
│                                                             │
│  ┌─────────────────────────────────────────────┐          │
│  │  Detection Rules                            │          │
│  │  • Diabetes                                 │          │
│  │  • Hypertension                             │          │
│  │  • Anemia                                   │          │
│  │  • Thyroid Disorders                        │          │
│  │  • Cardiovascular Risk                      │          │
│  │  • Kidney/Liver Disease                     │          │
│  └─────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (User Interface)
- **Technology**: HTML5, CSS3, JavaScript
- **Features**:
  - Responsive form-based interface
  - Real-time input validation
  - Animated results display
  - Risk level color coding
  - Mobile-friendly design

### 2. API Layer (Flask Server)
- **Technology**: Python Flask, Flask-CORS
- **Endpoints**:
  - `GET /` - Web interface
  - `GET /api/health` - Health check
  - `POST /api/analyze` - Main diagnostic endpoint
  - `GET /api/patient/<id>` - Get patient data
  - `GET /api/patients` - List all patients
- **Features**:
  - JSON request/response
  - CORS enabled
  - Error handling
  - Request validation

### 3. Business Logic (Diagnostic Engine)
- **Technology**: Python 3.8+
- **Components**:
  
  **a) Patient Data Model**
  - Structured data classes for patient information
  - Type safety with Python dataclasses
  - Enum-based gender and blood group types
  
  **b) Diagnostic Engine**
  - Rule-based expert system
  - Multi-parameter analysis
  - Pattern recognition
  - Risk stratification
  
  **c) Analysis Modules**:
  - **Vital Signs Analyzer**: Temperature, BP, HR, SpO2, BMI
  - **Lab Analyzer**: CBC, metabolic panel, lipid profile, thyroid
  - **Symptom Correlator**: Links symptoms with lab findings
  - **Risk Calculator**: Determines overall patient risk
  - **Recommendation Generator**: Personalized health advice

## Data Flow

```
1. User Input
   ↓
2. Frontend Form Submission (JSON)
   ↓
3. Flask API receives POST /api/analyze
   ↓
4. Request validation
   ↓
5. Create Patient object from JSON
   ↓
6. Pass to Diagnostic Engine
   ↓
7. Analyze Vital Signs
   ↓
8. Analyze Lab Results
   ↓
9. Correlate Symptoms
   ↓
10. Calculate Risk Level
   ↓
11. Generate Recommendations
   ↓
12. Create Diagnostic Report
   ↓
13. Convert to JSON response
   ↓
14. Return to frontend
   ↓
15. Display formatted results
```

## Diagnostic Logic Flow

```
┌─────────────────┐
│  Patient Data   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vital Signs    │──────► Temperature Analysis
│  Analysis       │──────► Blood Pressure Analysis
└────────┬────────┘──────► Heart Rate Analysis
         │                 Oxygen Saturation Analysis
         │                 BMI Calculation
         ▼
┌─────────────────┐
│  Lab Results    │──────► Blood Sugar (Diabetes)
│  Analysis       │──────► Lipid Profile (Cardiovascular)
└────────┬────────┘──────► CBC (Anemia, Infection)
         │                 Kidney Function
         │                 Liver Function
         │                 Thyroid Function
         ▼
┌─────────────────┐
│   Symptom       │──────► Match symptoms with findings
│  Correlation    │──────► Identify patterns
└────────┬────────┘──────► Increase diagnostic confidence
         │
         ▼
┌─────────────────┐
│     Risk        │──────► Count critical findings
│  Calculation    │──────► Count high-risk findings
└────────┬────────┘──────► Determine overall risk
         │
         ▼
┌─────────────────┐
│ Recommendation  │──────► Immediate actions
│   Generation    │──────► Follow-up tests
└────────┬────────┘──────► Lifestyle modifications
         │                 Medical referrals
         ▼
┌─────────────────┐
│  Final Report   │
└─────────────────┘
```

## Risk Stratification

The system uses a 5-level risk classification:

| Risk Level | Criteria | Action Required |
|------------|----------|----------------|
| **Normal** | All parameters within normal range | Routine follow-up |
| **Low** | Minor deviations | Monitoring recommended |
| **Moderate** | Significant abnormalities | Lifestyle changes + follow-up |
| **High** | Multiple risk factors | Medical attention required |
| **Critical** | Life-threatening values | Immediate emergency care |

## Detection Algorithms

### Diabetes Detection
```
IF fasting_glucose >= 126 mg/dL OR hba1c >= 6.5%
THEN diagnosis = "Diabetes Mellitus"
     risk = HIGH
ELSE IF fasting_glucose >= 100 mg/dL OR hba1c >= 5.7%
THEN diagnosis = "Prediabetes"
     risk = MODERATE
```

### Hypertension Detection
```
IF systolic >= 180 OR diastolic >= 120
THEN diagnosis = "Hypertensive Crisis"
     risk = CRITICAL
ELSE IF systolic >= 140 OR diastolic >= 90
THEN diagnosis = "Hypertension Stage 2"
     risk = HIGH
ELSE IF systolic >= 130 OR diastolic >= 80
THEN diagnosis = "Hypertension Stage 1"
     risk = MODERATE
```

### Anemia Detection
```
IF (gender == MALE AND hemoglobin < 13.5) OR
   (gender == FEMALE AND hemoglobin < 12.0)
THEN diagnosis = "Anemia"
     IF hemoglobin < 10
     THEN risk = HIGH
     ELSE risk = MODERATE
```

## Scalability Considerations

### Current Implementation
- In-memory patient storage (dictionary)
- Synchronous request processing
- Single-threaded Flask server

### Production Recommendations
- **Database**: PostgreSQL/MongoDB for persistent storage
- **Caching**: Redis for faster lookups
- **Queue**: Celery for async processing
- **Load Balancer**: Nginx for multiple instances
- **Container**: Docker for easy deployment
- **Orchestration**: Kubernetes for scaling

## Security Considerations

### Data Protection
- Patient data is sensitive PHI (Protected Health Information)
- Implement HIPAA compliance measures:
  - Encryption at rest and in transit
  - Access control and authentication
  - Audit logging
  - Data anonymization for reports

### API Security
- Add authentication (JWT tokens)
- Rate limiting
- Input validation and sanitization
- SQL injection prevention
- XSS protection

## Future Architecture Enhancements

1. **Machine Learning Integration**
   - Train ML models on historical data
   - Improve prediction accuracy
   - Pattern discovery

2. **Microservices Architecture**
   - Separate services for different analyses
   - Independent scaling
   - Better fault isolation

3. **Real-time Updates**
   - WebSocket for live updates
   - Push notifications
   - Streaming analytics

4. **Integration Layer**
   - HL7/FHIR for EHR integration
   - DICOM for medical imaging
   - Lab equipment interfaces
