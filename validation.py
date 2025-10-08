from datetime import datetime, date
from typing import List
from models.model import ExtractedData, ValidationResult

DATE_FORMAT = "%Y-%m-%d"


def _parse_date(d):
    if not d:
        return None
    if isinstance(d, datetime):
        return d
    if isinstance(d, date):
        return datetime(d.year, d.month, d.day)
    try:
        return datetime.strptime(d.strip(), "%Y-%m-%d")
    except Exception:
        print(f"Failed to parse date: {repr(d)}")
        return None


def rule_date_consistency(data: ExtractedData) -> ValidationResult:
    start = _parse_date(data.policy_start_date)
    end = _parse_date(data.policy_end_date)
    if not start or not end:
        return ValidationResult(
            rule="Date Consistency",
            status="FAIL",
            message="Could not parse dates to YYYY-MM-DD format.",
        )
    if end > start:
        return ValidationResult(
            rule="Date Consistency",
            status="PASS",
            message="Policy end date is after start date.",
        )

    return ValidationResult(
        rule="Date Consistency",
        status="FAIL",
        message="Policy end date cannot be before the start date.",
    )


def rule_value_check(data: ExtractedData) -> ValidationResult:
    val = data.insured_value
    if val is None:
        return ValidationResult(
            rule="Value Check",
            status="FAIL",
            message="Insured value is missing or not parseable.",
        )
    try:
        if float(val) > 0:
            return ValidationResult(
                rule="Value Check", status="PASS", message="Insured value is valid."
            )
        return ValidationResult(
            rule="Value Check",
            status="FAIL",
            message="Insured value must be a positive number.",
        )
    except Exception:
        return ValidationResult(
            rule="Value Check",
            status="FAIL",
            message="Insured value is not a valid number.",
        )


def rule_vessel_match(data: ExtractedData, valid_vessels: list) -> ValidationResult:
    vessel = data.vessel_name
    if not vessel:
        return ValidationResult(
            rule="Vessel Name Match", status="FAIL", message="Vessel name missing."
        )

    normalized_name = vessel.strip().lower()
    lower_list = [v.strip().lower() for v in valid_vessels]
    if normalized_name in lower_list:
        return ValidationResult(
            rule="Vessel Name Match",
            status="PASS",
            message=f"Vessel '{vessel}' is on the approved list.",
        )
    return ValidationResult(
        rule="Vessel Name Match",
        status="FAIL",
        message=f"Vessel '{vessel}' is not on the approved list.",
    )


def rule_completeness_check(data: ExtractedData) -> ValidationResult:
    pn = data.policy_number
    if pn and isinstance(pn, str) and pn.strip() != "":
        return ValidationResult(
            rule="Completeness Check",
            status="PASS",
            message="Policy number is present.",
        )
    return ValidationResult(
        rule="Completeness Check", status="FAIL", message="Policy number is missing."
    )


def run_all_validations(
    data: ExtractedData, valid_vessels: list
) -> List[ValidationResult]:
    results = []
    results.append(rule_date_consistency(data))
    results.append(rule_value_check(data))
    results.append(rule_vessel_match(data, valid_vessels))
    results.append(rule_completeness_check(data))
    return results
