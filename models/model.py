from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Optional
from datetime import date

# --- Pydantic Models ---

class DocumentRequest(BaseModel):
    """Request model for the document text."""
    document_text: str = Field(..., description="The raw text content of the insurance document.")

class ExtractedData(BaseModel):
    """Model for the data extracted by the AI service."""
    policy_number: Optional[str] = None
    vessel_name: Optional[str] = None
    policy_start_date: Optional[date] = None
    policy_end_date: Optional[date] = None
    insured_value: Optional[int] = None

class ValidationResult(BaseModel):
    """Model for a single validation check result."""
    rule: str
    status: str # "PASS" or "FAIL"
    message: str

class ValidationResponse(BaseModel):
    """The final response model for the /validate endpoint."""
    extracted_data: ExtractedData
    validation_results: List[ValidationResult]