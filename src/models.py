"""Data models for boarding pass advisor."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BoardingPass(BaseModel):
    """Extracted boarding pass information."""
    airport_iata: Optional[str] = Field(None, description="Origin airport IATA code")
    destination_iata: Optional[str] = Field(None, description="Destination IATA or city")
    terminal: Optional[str] = Field(None, description="Terminal (if present)")
    gate: Optional[str] = Field(None, description="Gate number")
    flight_number: Optional[str] = Field(None, description="Flight number (e.g., BA123)")
    departure_time: Optional[str] = Field(None, description="Local departure time")
    ocr_confidence: float = Field(0.0, ge=0.0, le=1.0)
    assumptions: List[str] = Field(default_factory=list)


class Lounge(BaseModel):
    """Normalized lounge record."""
    lounge_id: str
    name: str
    airport_code: str
    terminal: Optional[str] = None
    opening_hours: str  # e.g., "05:00-22:00"
    amenities: List[str] = Field(default_factory=list)
    access_notes: str = ""
    source_url: str


class RankedLounge(BaseModel):
    """Lounge with ranking metadata."""
    lounge: Lounge
    score: float
    rank_reason: str
    same_terminal: bool
    open_at_departure: bool


class Advisory(BaseModel):
    """Final advisory output."""
    lounge_recommendation: Optional[RankedLounge] = None
    destination_context: str
    warnings: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)
    summary_text: str
