# FHIR Healthcare Data API

This backend service provides a FastAPI application that allows querying FHIR healthcare data including Patients, Encounters, and Medication Requests.

## Requirements

- Python 3.11+
- Poetry (for dependency management)

## Setup

### Using Poetry

```bash
# Install dependencies
poetry install

# Run the application
poetry run uvicorn main:app --reload
```

### Using Docker

```bash
# Build and run using Docker Compose
docker-compose up --build
```

## API Endpoints

Once running, the following endpoints are available:

- `GET /` - API root with welcome message
- `GET /patients/` - Get all patients
- `GET /patients/{patient_id}` - Get patient details by ID
- `POST /fhir/push` - Push a FHIR resource to the FHIR server

## API Documentation

FastAPI automatically generates documentation for the API:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## FHIR Data Structure

The API works with the following FHIR resources:

### Patient

```json
{
  "resourceType": "Patient",
  "id": "patient-001",
  "name": [
    {
      "family": "Collins",
      "given": ["Jonathan", "Michael"]
    }
  ],
  "birthDate": "1980-01-01"
}
```

### Encounter

```json
{
  "resourceType": "Encounter",
  "id": "encounter-001-2",
  "status": "finished",
  "subject": {
    "reference": "Patient/patient-001",
    "display": "Jonathan Michael Collins"
  },
  "description": "General checkup"
}
```

### MedicationRequest

```json
{
  "resourceType": "MedicationRequest",
  "id": "medreq-001-1",
  "status": "active",
  "intent": "order",
  "medicationCodeableConcept": {
    "coding": [
      {
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "code": "8334",
        "display": "Atorvastatin 20 MG Oral Tablet"
      }
    ],
    "text": "Atorvastatin 20mg"
  },
  "subject": {
    "reference": "Patient/patient-001",
    "display": "Jonathan Michael Collins"
  },
  "encounter": {
    "reference": "Encounter/encounter-001-2"
  },
  "authoredOn": "2024-03-15T14:15:00-05:00",
  "requester": {
    "display": "Dr. Smith"
  },
  "reasonCode": [
    {
      "text": "High cholesterol management"
    }
  ],
  "dosageInstruction": [
    {
      "text": "Take one tablet daily.",
      "timing": {
        "repeat": {
          "frequency": 1,
          "period": 1,
          "periodUnit": "d"
        }
      },
      "route": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "26643006",
            "display": "Oral route"
          }
        ],
        "text": "Oral"
      },
      "doseAndRate": [
        {
          "doseQuantity": {
            "value": 20,
            "unit": "mg"
          }
        }
      ]
    }
  ]
}
```

## CoderPad Exercise

For the CoderPad portion of this exercise, check the `coderpad_sample.py` file which contains a simplified version of the core functionality with stub implementations for candidates to complete. 