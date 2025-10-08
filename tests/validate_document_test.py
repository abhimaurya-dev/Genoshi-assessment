import os
import pytest
from ai_extractor import extract_data_with_ai
from validation import run_all_validations
from models.model import ExtractedData

def load_sample_file(filename):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "provided_assets", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
@pytest.fixture
def valid_vessels():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "provided_assets", "valid_vessels.json")
    import json
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Test documents that should PASS validation
@pytest.mark.asyncio
async def test_sample_document_pass(valid_vessels):
    document_text = load_sample_file("sample_document_pass.txt")
    
    extracted_data_dict = await extract_data_with_ai(document_text)
    extracted = ExtractedData(**extracted_data_dict)
    
    validation_results = run_all_validations(extracted, valid_vessels)
    print(validation_results)
    # All rule should PASS
    pass_rules = [r for r in validation_results if r.status == "PASS"]
    assert len(pass_rules) == len(validation_results)


# Test documents that should FAIL validation
@pytest.mark.asyncio
async def test_sample_document_fail(valid_vessels):
    document_text = load_sample_file("sample_document_fail.txt")
    
    extracted_data_dict = await extract_data_with_ai(document_text)
    extracted = ExtractedData(**extracted_data_dict)
    
    validation_results = run_all_validations(extracted, valid_vessels)

    print(validation_results)
    
    # At least one rule should FAIL
    fail_rules = [r for r in validation_results if r.status == "FAIL"]
    assert len(fail_rules) > 0
