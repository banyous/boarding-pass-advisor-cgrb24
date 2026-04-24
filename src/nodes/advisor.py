"""Generate final advisory using OpenAI with grounded data."""
import json
from typing import List, Optional
from openai import OpenAI
from src.config import OPENAI_API_KEY, OPENAI_MODEL_ADVISOR
from src.models import BoardingPass, RankedLounge, Advisory


client = OpenAI(api_key=OPENAI_API_KEY)


ADVISOR_SYSTEM_PROMPT = """You are an airport travel advisor.
Generate a concise advisory based ONLY on the provided data. Do not invent facts.

Rules:
- Ground every claim in provided lounge or boarding pass data
- Always include lounge_id and source_url for citations
- Disclose assumptions (terminal inference, etc.)
- Be concise (3-4 short paragraphs max)
- For destination context: infer short/long-haul if departure region to destination region is inferable
- Warn about lounges closing soon (within 1hr of closing)

Return format: JSON with keys:
- summary_text: The full advisory (plain text, Markdown OK)
- warnings: List of warning strings
- citations: List of "lounge_id: source_url" strings
"""


def generate_advisory(
    boarding_pass: BoardingPass,
    ranked_lounges: List[RankedLounge],
    now_str: str,
) -> Advisory:
    """Generate LLM advisory grounded in extracted data."""
    top_lounge: Optional[RankedLounge] = ranked_lounges[0] if ranked_lounges else None

    context = {
        "boarding_pass": boarding_pass.dict(),
        "top_lounge": top_lounge.dict() if top_lounge else None,
        "alternatives": [r.dict() for r in ranked_lounges[1:3]],
        "current_time": now_str,
    }

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL_ADVISOR,
            messages=[
                {"role": "system", "content": ADVISOR_SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate advisory from this context:\n\n{json.dumps(context, indent=2)}"},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        data = json.loads(response.choices[0].message.content)

        return Advisory(
            lounge_recommendation=top_lounge,
            destination_context=boarding_pass.destination_iata or "Unknown",
            summary_text=data.get("summary_text", ""),
            warnings=data.get("warnings", []),
            citations=data.get("citations", []),
            assumptions=boarding_pass.assumptions,
        )

    except Exception as e:
        return Advisory(
            lounge_recommendation=top_lounge,
            destination_context=boarding_pass.destination_iata or "Unknown",
            summary_text=f"Advisory generation failed: {str(e)}",
            warnings=[f"Error: {str(e)}"],
            citations=[],
            assumptions=boarding_pass.assumptions,
        )
