import os
import re
import json
from typing import Dict, Any
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

EXTRACT_PROMPT_TEMPLATE = '''
You are an expert insurance document parser. Extract the following fields from the input text and return a single JSON object EXACTLY in this shape (no extra keys):


{{
"policy_number": string or null,
"vessel_name": string or null,
"policy_start_date": date string in YYYY-MM-DD or null,
"policy_end_date": date string in YYYY-MM-DD or null,
"insured_value": number (no currency symbols) or null
}}


Rules:
- If a field is not present or not confidently extractable, set it to null.
- Dates: convert to ISO format YYYY-MM-DD if possible.
- Insured value: return a numeric value only (e.g., 1000000). Remove commas, currency signs, and words.
- Output: **Only** output the JSON object (no explanation). If the model adds extra text, the caller will extract the JSON portion.


Here is the document text to parse:

"""
{document_text}
"""
'''

async def extract_data_with_ai(document_text: str) -> Dict[str, Any]:
    """
    Uses a generative AI model to extract structured data from document text.
    """

    extract_prompt = EXTRACT_PROMPT_TEMPLATE.format(document_text=document_text)
    
    client = genai.Client(api_key=API_KEY)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=extract_prompt
        )
    except Exception as e:
        raise RuntimeError(f"genai.generate() failed: {e}")

    parsed = None
    try:
        raw_text = response.candidates[0].content.parts[0].text

        # Remove the triple backticks and optional 'json' language specifier
        clean_text = re.sub(r"^```json\s*|```$", "", raw_text.strip(), flags=re.MULTILINE)

        parsed = json.loads(clean_text)
    except Exception:
        raw_text = str(response)


    return {
        "policy_number": parsed.get("policy_number"),
        "vessel_name": parsed.get("vessel_name"),
        "policy_start_date": parsed.get("policy_start_date"),
        "policy_end_date": parsed.get("policy_end_date"),
        "insured_value": parsed.get("insured_value"),
    }