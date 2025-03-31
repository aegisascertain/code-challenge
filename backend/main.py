import os
from typing import Dict, List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import uvicorn

from fhir_utils import (
    load_patients_fhir,
    load_encounters_fhir,
    load_medication_requests_fhir,
    query_patient_by_name_and_dob,
    get_patient_encounters_and_med_requests_by_id,
    get_all_encounters
)

# Initialize FastAPI
app = FastAPI(
    title="FHIR API",
    description="An API for querying FHIR healthcare data",
    version="0.1.0",
)

# Define data file paths - adjust if needed
DATA_DIR = os.environ.get("DATA_DIR", "data")
PATIENTS_FILE = os.path.join(DATA_DIR, "patients.json")
ENCOUNTERS_FILE = os.path.join(DATA_DIR, "encounters.json")
MEDICATION_REQUESTS_FILE = os.path.join(DATA_DIR, "medication_requests.json")

# Load data at startup
patients = load_patients_fhir(PATIENTS_FILE)
encounters = load_encounters_fhir(ENCOUNTERS_FILE)
med_requests = load_medication_requests_fhir(MEDICATION_REQUESTS_FILE)


# Define Pydantic models for response validation
class Patient(BaseModel):
    resourceType: str
    id: str
    name: List[Dict]
    birthDate: str


class Encounter(BaseModel):
    resourceType: str
    id: str
    status: str
    subject: Dict
    description: str


class MedicationRequest(BaseModel):
    resourceType: str
    id: str
    encounter: Dict
    dosageInstruction: List[Dict]


class PatientResponse(BaseModel):
    patients: List[Patient]


class EncounterResponse(BaseModel):
    encounters: List[Encounter]


class MedicationRequestResponse(BaseModel):
    medicationRequests: List[MedicationRequest]


class PatientDetailsResponse(BaseModel):
    patient: Patient
    encounters: List[Encounter]
    medicationRequests: List[MedicationRequest]


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the FHIR API"}


@app.get("/patients/", response_model=PatientResponse, tags=["Patients"])
async def search_patients(
    name: str = Query(None, description="Patient name (full or partial)"),
    birthDate: str = Query(None, description="Patient birth date (YYYY-MM-DD)"),
    threshold: float = Query(0.7, description="Minimum similarity threshold for name matching")
):
    """
    Search for patients by name and birth date using fuzzy matching.
    """
    if not name or not birthDate:
        raise HTTPException(status_code=400, detail="Both name and birthDate parameters are required")
    
    results = query_patient_by_name_and_dob(name, birthDate, patients, threshold)
    return {"patients": results}


@app.get("/patients/{patient_id}", response_model=PatientDetailsResponse, tags=["Patients"])
async def get_patient_details(patient_id: str):
    """
    Get a patient's details including encounters and medication requests.
    """
    # Find patient
    patient = next((p for p in patients if p["id"] == patient_id), None)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")
    
    # Get encounters and medication requests
    patient_encounters, patient_med_requests = get_patient_encounters_and_med_requests_by_id(
        patient_id, encounters, med_requests
    )
    
    return {
        "patient": patient,
        "encounters": patient_encounters,
        "medicationRequests": patient_med_requests
    }


@app.get("/encounters/", response_model=EncounterResponse, tags=["Encounters"])
async def list_encounters():
    """
    Get all encounters.
    """
    all_encounters = get_all_encounters(encounters)
    return {"encounters": all_encounters}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 