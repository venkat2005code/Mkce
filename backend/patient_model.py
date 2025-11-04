"""
Patient Data Model
Defines the structure for patient information and lab reports
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class BloodGroup(Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


@dataclass
class VitalSigns:
    """Patient vital signs"""
    temperature: float  # Celsius
    blood_pressure_systolic: int  # mmHg
    blood_pressure_diastolic: int  # mmHg
    heart_rate: int  # bpm
    respiratory_rate: int  # breaths per minute
    oxygen_saturation: float  # percentage
    weight: float  # kg
    height: float  # cm
    
    def get_bmi(self) -> float:
        """Calculate Body Mass Index"""
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)


@dataclass
class LabResults:
    """Laboratory test results"""
    # Complete Blood Count (CBC)
    hemoglobin: Optional[float] = None  # g/dL
    wbc_count: Optional[float] = None  # cells/μL
    platelet_count: Optional[float] = None  # cells/μL
    rbc_count: Optional[float] = None  # million cells/μL
    
    # Blood Sugar
    fasting_glucose: Optional[float] = None  # mg/dL
    random_glucose: Optional[float] = None  # mg/dL
    hba1c: Optional[float] = None  # percentage
    
    # Lipid Profile
    total_cholesterol: Optional[float] = None  # mg/dL
    ldl_cholesterol: Optional[float] = None  # mg/dL
    hdl_cholesterol: Optional[float] = None  # mg/dL
    triglycerides: Optional[float] = None  # mg/dL
    
    # Kidney Function
    creatinine: Optional[float] = None  # mg/dL
    bun: Optional[float] = None  # mg/dL (Blood Urea Nitrogen)
    uric_acid: Optional[float] = None  # mg/dL
    
    # Liver Function
    sgot_ast: Optional[float] = None  # U/L
    sgpt_alt: Optional[float] = None  # U/L
    bilirubin_total: Optional[float] = None  # mg/dL
    
    # Thyroid
    tsh: Optional[float] = None  # mIU/L
    t3: Optional[float] = None  # ng/dL
    t4: Optional[float] = None  # μg/dL
    
    # Others
    sodium: Optional[float] = None  # mEq/L
    potassium: Optional[float] = None  # mEq/L
    vitamin_d: Optional[float] = None  # ng/mL
    vitamin_b12: Optional[float] = None  # pg/mL


@dataclass
class MedicalHistory:
    """Patient medical history"""
    chronic_conditions: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    current_medications: List[str] = field(default_factory=list)
    past_surgeries: List[str] = field(default_factory=list)
    family_history: List[str] = field(default_factory=list)
    smoking: bool = False
    alcohol_consumption: bool = False


@dataclass
class Symptoms:
    """Current patient symptoms"""
    chief_complaint: str
    symptoms_list: List[str] = field(default_factory=list)
    duration_days: int = 0
    severity: str = "moderate"  # mild, moderate, severe


@dataclass
class Patient:
    """Complete patient information"""
    patient_id: str
    name: str
    age: int
    gender: Gender
    blood_group: Optional[BloodGroup] = None
    contact: str = ""
    
    # Medical data
    vital_signs: Optional[VitalSigns] = None
    lab_results: Optional[LabResults] = None
    medical_history: Optional[MedicalHistory] = None
    symptoms: Optional[Symptoms] = None
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert patient data to dictionary"""
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender.value if self.gender else None,
            "blood_group": self.blood_group.value if self.blood_group else None,
            "contact": self.contact,
            "vital_signs": self.vital_signs.__dict__ if self.vital_signs else None,
            "lab_results": self.lab_results.__dict__ if self.lab_results else None,
            "medical_history": self.medical_history.__dict__ if self.medical_history else None,
            "symptoms": self.symptoms.__dict__ if self.symptoms else None,
            "timestamp": self.timestamp.isoformat()
        }
