import os
from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from utils.fhir_utils import (
    load_patients_fhir,
    load_encounters_fhir,
    load_medication_requests_fhir,
    push_to_fhir_stream
)

# Initialize FastAPI
app = FastAPI(
    title="FHIR API",
    description="An API for querying FHIR healthcare data",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    full_name: str
    birth_date: date

# Define model for FHIR resource submission
class FHIRResource(BaseModel):
    resource: dict

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the FHIR API"}


@app.get("/patients/{patient_id}", response_model=Patient, tags=["Patients"])
async def get_patient_details(patient_id: str) -> Patient | None:
    """
    Get a patient's details including encounters and medication requests.
    """
    # Find patient
    patient = next((p for p in patients if p["id"] == patient_id), None)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")
    
    full_name = ""
    if patient.get("name") and len(patient["name"]) > 0:
        name_obj = patient["name"][0]
        given_names = " ".join(name_obj.get("given", []))
        family_name = name_obj.get("family", "")
        full_name = f"{given_names} {family_name}".strip()
        
        # Transform to match Patient model
        mapped_patient = {
            "resourceType": patient.get("resourceType", ""),
            "id": patient.get("id", ""),
            "full_name": full_name,
            "birth_date": patient.get("birthDate", "")
        }
        return mapped_patient
    
    

@app.get("/patients/", response_model=list[Patient], tags=["Patients"])
async def list_patients() -> list[Patient]:
    """
    Get all patients.
    """
    
    mapped_patients = []
    for p in patients:
        # Extract full name from name array (family name + given names)
        full_name = ""
        if p.get("name") and len(p["name"]) > 0:
            name_obj = p["name"][0]
            given_names = " ".join(name_obj.get("given", []))
            family_name = name_obj.get("family", "")
            full_name = f"{given_names} {family_name}".strip()
        
        # Transform to match Patient model
        mapped_patient = {
            "resourceType": p.get("resourceType", ""),
            "id": p.get("id", ""),
            "full_name": full_name,
            "birth_date": p.get("birthDate", "")
        }
        mapped_patients.append(mapped_patient)
    
    return mapped_patients

@app.post("/fhir/push", tags=["FHIR Operations"])
async def push_patient_to_fhir(resource: FHIRResource):
    """
    Push a patient record to the FHIR server.
    
    This endpoint accepts a FHIR resource and pushes it to the configured FHIR server.
    """
    try:
        result = push_to_fhir_stream(resource.resource)
        return {"status": "success", "message": "Resource pushed to FHIR server", "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to push to FHIR server: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 