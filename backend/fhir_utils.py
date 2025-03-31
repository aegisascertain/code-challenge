import json
from difflib import SequenceMatcher

# ------------------------------------------------------------------------------
# Data Loading Functions
# ------------------------------------------------------------------------------

def load_patients_fhir(file: str) -> list[dict]:
    """Load FHIR Patient resources from a JSON file.

    The JSON file is expected to contain an array of Patient resources.
    
    Args:
        file: Path to the JSON file containing Patient resources.
    
    Returns:
        A list of dictionaries representing Patient resources.
    """
    with open(file, 'r') as f:
        return json.load(f)


def load_encounters_fhir(file: str) -> list[dict]:
    """Load FHIR Encounter resources from a JSON file.

    The JSON file is expected to contain an array of Encounter resources.
    
    Args:
        file: Path to the JSON file containing Encounter resources.
    
    Returns:
        A list of dictionaries representing Encounter resources.
    """
    with open(file, 'r') as f:
        return json.load(f)


def load_medication_requests_fhir(file: str) -> list[dict]:
    """Load FHIR MedicationRequest resources from a JSON file.

    The JSON file is expected to contain an array of MedicationRequest resources.
    
    Args:
        file: Path to the JSON file containing MedicationRequest resources.
    
    Returns:
        A list of dictionaries representing MedicationRequest resources.
    """
    with open(file, 'r') as f:
        return json.load(f)


# ------------------------------------------------------------------------------
# Query Functions
# ------------------------------------------------------------------------------

def query_patient_by_name_and_dob(query_name: str, dob: str, patients: list[dict], threshold: float = 0.7) -> list[dict]:
    """Query patients by name and date of birth using fuzzy matching.

    Args:
        query_name: The patient name to search for (can be partial or full).
        dob: The birthDate to match (formatted as 'YYYY-MM-DD').
        patients: A list of Patient resources (dictionaries).
        threshold: The minimum similarity ratio required for a match (default is 0.7).
    
    Returns:
        A list of Patient resources that match the query.
    """
    matches = []
    
    for patient in patients:
        # Skip if birth date doesn't match
        if patient.get('birthDate') != dob:
            continue
            
        # Get first name entry and extract given and family names
        if patient.get('name') and len(patient['name']) > 0:
            name_obj = patient['name'][0]
            given_names = ' '.join(name_obj.get('given', []))
            family_name = name_obj.get('family', '')
            full_name = f"{given_names} {family_name}".strip()
            
            # Calculate similarity ratio
            similarity = SequenceMatcher(None, query_name.lower(), full_name.lower()).ratio()
            
            # Add to matches if above threshold
            if similarity >= threshold:
                matches.append(patient)
                
    return matches


def get_patient_encounters_and_med_requests_by_id(patient_id: str, encounters: list[dict], med_requests: list[dict]) -> tuple[list[dict], list[dict]]:
    """Retrieve patient encounters and associated medication requests by patient id.

    Args:
        patient_id: The unique identifier of the patient.
        encounters: A list of Encounter resources (dictionaries).
        med_requests: A list of MedicationRequest resources (dictionaries).
    
    Returns:
        A tuple containing:
          - A list of Encounter resources for the patient.
          - A list of MedicationRequest resources associated with the patient's encounters.
    """
    patient_reference = f"Patient/{patient_id}"
    
    # Filter encounters for this patient
    patient_encounters = [
        encounter for encounter in encounters
        if encounter.get('subject', {}).get('reference') == patient_reference
    ]
    
    # Get encounter IDs
    encounter_ids = [encounter['id'] for encounter in patient_encounters]
    
    # Filter medication requests associated with these encounters
    patient_med_requests = [
        request for request in med_requests
        if request.get('encounter', {}).get('reference', '').split('/')[1] in encounter_ids
    ]
    
    return patient_encounters, patient_med_requests


def get_all_encounters(encounters: list[dict]) -> list[dict]:
    """Retrieve all Encounter resources.

    This function mimics a GET list endpoint for encounters.

    Args:
        encounters: A list of Encounter resources (dictionaries).
    
    Returns:
        A list of all Encounter resources.
    """
    return encounters
