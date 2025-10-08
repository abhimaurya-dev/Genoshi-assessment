import os
import pytest
from ai_extractor import extract_data_with_ai
from validation import run_all_validations
from validation import (
    rule_date_consistency,
    rule_value_check,
    rule_vessel_match,
    rule_completeness_check,
)
from models.model import ExtractedData


def load_sample_file(filename):
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "provided_assets", filename
    )
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def valid_vessels():
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "provided_assets",
        "valid_vessels.json",
    )
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


# --- Test rule_date_consistency ---
@pytest.mark.parametrize(
    "start, end, expected",
    [
        ("2025-11-01", "2026-10-31", "PASS"),  # Normal valid case
        ("2026-01-01", "2025-12-31", "FAIL"),  # End date before start date
        (None, "2026-10-31", "FAIL"),  # Missing start date
        ("2025-11-01", None, "FAIL"),  # Missing end date
    ],
)
def test_rule_date_consistency(start, end, expected):
    data = ExtractedData(
        policy_number="HM-001",
        vessel_name="MV Neptune",
        policy_start_date=start,
        policy_end_date=end,
        insured_value=1000,
    )
    result = rule_date_consistency(data)
    assert result.status == expected


# --- Test rule_value_check ---
@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "PASS"),  # Positive value
        (0, "FAIL"),  # Zero value
        (-500, "FAIL"),  # Negative value
        (None, "FAIL"),  # Missing value
    ],
)
def test_rule_value_check(value, expected):
    data = ExtractedData(
        policy_number="HM-001",
        vessel_name="MV Neptune",
        policy_start_date="2025-11-01",
        policy_end_date="2026-10-31",
        insured_value=value,
    )
    result = rule_value_check(data)
    assert result.status == expected


# --- Test rule_vessel_match ---
VALID_VESSELS = ["MV Neptune", "Oceanic Voyager", "Starlight Carrier"]


@pytest.mark.parametrize(
    "vessel_name, expected",
    [
        ("MV Neptune", "PASS"),  # Approved vessel
        ("mv neptune", "PASS"),  # Case-insensitive match
        ("The Wanderer", "FAIL"),  # Not approved
        ("", "FAIL"),  # Missing vessel name
        (None, "FAIL"),  # None vessel name
    ],
)
def test_rule_vessel_match(vessel_name, expected):
    data = ExtractedData(
        policy_number="HM-001",
        vessel_name=vessel_name,
        policy_start_date="2025-11-01",
        policy_end_date="2026-10-31",
        insured_value=1000,
    )
    result = rule_vessel_match(data, VALID_VESSELS)
    assert result.status == expected


# --- Test rule_completeness_check ---
@pytest.mark.parametrize(
    "policy_number, expected",
    [
        ("HM-001", "PASS"),  # Valid policy number
        ("", "FAIL"),  # Empty string
        (None, "FAIL"),  # Missing policy number
        ("   ", "FAIL"),  # Whitespace only
    ],
)
def test_rule_completeness_check(policy_number, expected):
    data = ExtractedData(
        policy_number=policy_number,
        vessel_name="MV Neptune",
        policy_start_date="2025-11-01",
        policy_end_date="2026-10-31",
        insured_value=1000,
    )
    result = rule_completeness_check(data)
    assert result.status == expected
