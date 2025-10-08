# Genoshi-assessment
# Mini Insurance Document Validator

[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.101.0-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-20.10-blue?logo=docker)](https://www.docker.com/)

## Project Overview

The **Mini Insurance Document Validator** is an AI-powered API that extracts structured data from insurance documents and validates it against predefined business rules. This project leverages a generative AI model to automatically parse policy details and ensures the extracted data is accurate, complete, and consistent.

Key functionalities include:

- AI extraction of policy details such as policy number, vessel name, policy start and end dates, and insured value.
- Rule-based validation:
  - Date consistency check
  - Insured value positivity check
  - Vessel name verification against a predefined list
  - Completeness check for mandatory fields
- API accessible via FastAPI with interactive docs.
- Dockerized for easy deployment.
- Production URL: [https://genoshi-assessment.vercel.app/](https://genoshi-assessment.vercel.app/)

---

## Tech Stack

- **Language:** Python 3.11  
- **Framework:** FastAPI  
- **AI Service:** Google Gemini API  
- **Data Validation:** Pydantic  
- **Testing:** Pytest + AsyncIO  
- **Deployment:** Docker, Vercel  

---

## Project Structure

```
.
|── main.py              # FastAPI app and endpoints
│── models/model.py              # Pydantic models
│── validation.py        # Business rule validations
│── ai_extractor.py      # AI extraction logic
|── provided_assets/     # JSON and sample documents
├── tests/               # Pytest test cases
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Installation & Local Setup

### 1. Clone git repository
```bash
git clone https://github.com/abhimaurya-dev/Genoshi-assessment.git
cd Genoshi-assessment
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
Rename `.env.example` to `.env` file in the root directory
Update required environment variables

### 5. Run the FastAPI app locally
```bash
uvicorn main:app --reload
```

Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the interactive API documentation.

---

## Docker Setup

### Build the Docker image
```bash
docker build -t mini-insurance-validator .
```

### Run the container
```bash
docker run -d -p 8000:8000 mini-insurance-validator
```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

## API Endpoints

### Root
```
GET /
```
- Returns a welcome HTML page with a link to API docs.

### Validate Document
```
POST /validate
```
- **Description:** Extracts data from an insurance document and runs validation rules.
- **Request Body:**
```json
{
  "document_text": "Full text of the insurance document here."
}
```
- **Response:**
```json
{
  "extracted_data": {
    "policy_number": "HM-001",
    "vessel_name": "MV Neptune",
    "policy_start_date": "2025-11-01",
    "policy_end_date": "2026-10-31",
    "insured_value": 1000
  },
  "validation_results": [
    {"rule": "Date Consistency", "status": "PASS", "message": "Policy end date is after start date."},
    {"rule": "Value Check", "status": "PASS", "message": "Insured value is valid."},
    {"rule": "Vessel Name Match", "status": "PASS", "message": "Vessel 'MV Neptune' is on the approved list."},
    {"rule": "Completeness Check", "status": "PASS", "message": "Policy number is present."}
  ]
}
```

---

## Testing

Run all tests using Pytest:
```bash
pytest tests/
```

---

## Production

The project is deployed at: [https://genoshi-assessment.vercel.app/](https://genoshi-assessment.vercel.app/)

---