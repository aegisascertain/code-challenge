import json
import requests
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def push_to_fhir_stream(resource: dict) -> None:
    """Push a FHIR resource to the FHIR stream.
    
    Args:
        resource: A dictionary representing a FHIR resource.
    """
    
    # Example FHIR server endpoint - in a real application, this would be configurable
    FHIR_SERVER_URL = "https://hapi.fhir.org/baseR4"
    
    # Check if the resource has a valid type
    if not resource or "resourceType" not in resource:
        logger.error("Invalid FHIR resource: missing resourceType")
        raise ValueError("Invalid FHIR resource: missing resourceType")
    
    resource_type = resource["resourceType"]
    resource_id = resource.get("id")
    
    # Determine the endpoint URL based on resource type
    endpoint = f"{FHIR_SERVER_URL}/{resource_type}"
    if resource_id:
        endpoint = f"{endpoint}/{resource_id}"
    
    try:
        
        response = requests.post(
            endpoint,
            json=resource,
            headers={"Content-Type": "application/fhir+json"}
        )
    
        # Check if the request was successful
        response.raise_for_status()
        logger.info(f"Successfully pushed {resource_type} to FHIR server: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to push to FHIR server: {str(e)}")
        raise