import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import ValidationError
from .models.model import ValidationResponse, DocumentRequest, ExtractedData
from .ai_extractor import extract_data_with_ai
from .validation import run_all_validations

# --- Configuration ---
# Use environment variables for API key management

app = FastAPI(
    title="Mini Insurance Document Validator",
    description="An API to validate extracted data from insurance documents using AI.",
    version="1.0.0",
)

# --- API Endpoint ---


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Welcome endpoint with a link to API docs.
    """
    html_content = """
    <html>
        <head>
            <title>Mini Insurance Document Validator</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align:center; padding:50px;">
            <h1>Welcome to the Mini Insurance Document Validator API!</h1>
            <p>Click the button below to explore and test the API endpoints:</p>
            <a href="/docs" style="
                display:inline-block;
                padding: 12px 24px;
                font-size: 18px;
                color: white;
                background-color: #4CAF50;
                text-decoration: none;
                border-radius: 6px;
                margin-top: 20px;
            ">Go to API Docs</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/validate", response_model=ValidationResponse)
async def validate_document(request: DocumentRequest):
    """
    Validates an insurance document by extracting data via AI and running business rules.
    """
    # Call the AI service to extract data from the document text
    try:
        raw_extracted_data = await extract_data_with_ai(request.document_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service failed: {str(e)}")

    # Parse and validate the AI's output using your Pydantic model.
    try:
        extracted_data = ExtractedData(**raw_extracted_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=400, detail=f"AI output did not match expected schema: {e}"
        )

    VALID_VESSELS_PATH = os.path.join(
        os.path.dirname(__file__), "provided_assets", "valid_vessels.json"
    )
    with open(VALID_VESSELS_PATH, "r", encoding="utf-8") as f:
        VALID_VESSELS = json.load(f)

    validation_results = run_all_validations(extracted_data, VALID_VESSELS)

    # Return the final, structured response.
    return ValidationResponse(
        extracted_data=extracted_data, validation_results=validation_results
    )
