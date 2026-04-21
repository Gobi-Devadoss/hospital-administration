from os import name

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List

app = FastAPI(title="Hospital API", version = "1.0.0")

doctors_db = []
patients_db = []

class Doctor(BaseModel):
    name: str
    email: EmailStr
    specialization: str
    is_active: bool = True


class DoctorResponse(Doctor):
    id: int


class Patient(BaseModel):
    name: str
    age: int = Field(..., gt=0, description = "Age must be greater than 0")
    phone: str

class PatientResponse(Patient):
    id: int



@app.post("/doctors/", response_model=DoctorResponse)
def create_doctor(doctor: Doctor):
    new_doctor = {
        "name": doctor.name,
        "email": doctor.email,
        "specialization": doctor.specialization,
        "is_active": doctor.is_active
    }
    doctors_db.append(new_doctor)
    return new_doctor


@app.post("/patients/", response_model=PatientResponse)
def create_patient(patient: Patient):
    new_patient = {
        "name": patient.name,
        "age": patient.age,
        "phone": patient.phone
    }
    patients_db.append(new_patient)
    return new_patient

@app.get("/doctors/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int):
    for doctor in doctors_db:
        if doctor.id == doctor_id:
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.get("/patients/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int):
    for patient in patients_db:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/doctors/", response_model=List[DoctorResponse])
def get_doctors():
    return doctors_db

@app.get("/patients/", response_model=List[PatientResponse])
def get_patients():
    return patients_db

