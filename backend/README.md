# FHIR Healthcare Data API

This backend service provides a FastAPI application that allows querying FHIR healthcare data including Patients, Encounters, and Medication Requests.

## Requirements

- Python 3.8+
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
- `GET /patients/` - Search patients by name and birth date
  - Query parameters:
    - `name`: Patient name (full or partial)
    - `birthDate`: Patient birth date in YYYY-MM-DD format
    - `threshold`: Minimum similarity threshold for name matching (default: 0.7)
- `GET /patients/{patient_id}` - Get patient details including encounters and medication requests
- `GET /encounters/` - Get all encounters

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
  "id": "P001",
  "name": [
    {
      "family": "Doe",
      "given": ["John"]
    }
  ],
  "birthDate": "1980-01-01"
}
```

### Encounter

```json
{
  "resourceType": "Encounter",
  "id": "V001",
  "status": "finished",
  "subject": {
    "reference": "Patient/P001"
  },
  "description": "General checkup"
}
```

### MedicationRequest

```json
{
  "resourceType": "MedicationRequest",
  "id": "RX001",
  "encounter": {
    "reference": "Encounter/V001"
  },
  "dosageInstruction": [
    {
      "text": "Take one tablet daily"
    }
  ]
}
```

## CoderPad Exercise

For the CoderPad portion of this exercise, check the `coderpad_sample.py` file which contains a simplified version of the core functionality with stub implementations for candidates to complete. 