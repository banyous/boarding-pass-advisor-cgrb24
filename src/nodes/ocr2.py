"""OCR extraction using GPT-4 Vision."""
import base64
import json
from openai import OpenAI
from src.config import OPENAI_API_KEY, MODEL_VISION
from src.models import BoardingPass


client = OpenAI(api_key=OPENAI_API_KEY)


OCR_SYSTEM_PROMPT = """You are an OCR extraction agent for boarding passes.
Extract the following fields from the boarding pass image and return strict JSON.

Required fields:
- airport_iata: 3-letter IATA code of ORIGIN airport
- destination_iata: 3-letter IATA code of DESTINATION (or city name if IATA unclear)
- terminal: Terminal identifier (e.g., "T2", "5", "B") or null if not present
- gate: Gate number or null
- flight_number: Full flight number (e.g., "BA123")
- departure_time: Local departure time in format "HH:MM" or null
- ocr_confidence: Float 0.0-1.0, your confidence in the extraction

Rules:
- Return ONLY valid JSON, no markdown
- Use null for missing fields
- Be conservative with confidence (0.7+ only if text is clear)
"""


def extract_from_image(image_path: str) -> BoardingPass:
    """Extract boarding pass data from image using GPT-4V."""
    with open(image_path, "rb") as img_file:
        image_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model=MODEL_VISION,
        messages=[
            {"role": "system", "content": OCR_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract boarding pass data."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        },
                    },
                ],
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    try:
        data = json.loads(response.choices[0].message.content)
        return BoardingPass(**data)
    except (json.JSONDecodeError, ValueError) as e:
        return BoardingPass(
            ocr_confidence=0.0,
            assumptions=[f"OCR parsing failed: {str(e)}"]
        )


def extract_from_text(text: str) -> BoardingPass:
    """Fallback: extract from manual text input using LLM."""
    response = client.chat.completions.create(
        model=MODEL_VISION,
        messages=[
            {"role": "system", "content": OCR_SYSTEM_PROMPT},
            {"role": "user", "content": f"Parse this boarding pass text:\n\n{text}"},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    # Manual input gets high confidence
    data["ocr_confidence"] = 0.95
    return BoardingPass(**data)
