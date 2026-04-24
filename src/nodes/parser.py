"""Parser node - validates extracted data with Pydantic."""
from src.models import BoardingPass


def validate_boarding_pass(data: dict) -> BoardingPass:
    """Validate and clean boarding pass data."""
    # Ensure required fields exist
    if not data.get("airport_iata"):
        data["assumptions"] = data.get("assumptions", [])
        data["assumptions"].append("No airport code found - lounge search may be limited")
    
    return BoardingPass(**data)
