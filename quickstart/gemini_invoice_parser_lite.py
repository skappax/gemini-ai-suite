"""
============================================================================
GEMINI AI SUITE - QUICKSTART COMMUNITY SAMPLE
Python / Gemini 2.5 Flash Vision Multimodal Invoice Parser
============================================================================
Turnkey production FastAPI service with Pydantic validation & batch export at:
https://skappax.github.io/gemini-ai-suite/
============================================================================
"""

import os
import json
from google import genai
from google.genai import types

def parse_invoice(image_path: str) -> dict:
    """
    Extracts structured financial data from an invoice or receipt image
    using Google Gemini 2.5 Flash Multimodal Vision.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    client = genai.Client(api_key=api_key)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = (
        "Extract the following fields from this invoice/receipt into strict JSON format:\n"
        "- invoice_number (string)\n"
        "- vendor_name (string)\n"
        "- date (YYYY-MM-DD)\n"
        "- total_amount (float)\n"
        "- currency (e.g. EUR, USD)\n"
        "- line_items (list of objects with: description, quantity, unit_price, total_price)\n"
        "Return ONLY the raw JSON object, without markdown formatting or backticks."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            prompt
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )

    return json.loads(response.text)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python gemini_invoice_parser_lite.py <path_to_invoice_image.jpg>")
    else:
        result = parse_invoice(sys.argv[1])
        print(json.dumps(result, indent=2))
