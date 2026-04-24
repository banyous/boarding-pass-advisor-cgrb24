"""Configuration and constants."""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"                  # Has vision, used for OCR
OPENAI_MODEL_ADVISOR = "gpt-4o-mini"     # Cheaper, used for advisory

# Pipeline settings
OCR_CONFIDENCE_THRESHOLD = 0.6
LOUNGE_CACHE_PATH = "data/lounges_cache.json"

# Terminal inference heuristics
TERMINAL_HEURISTICS = {
    ("LHR", "A"): "T2",
    ("LHR", "B"): "T3",
    ("LHR", "C"): "T3",
    ("LHR", "D"): "T4",
    ("LHR", "E"): "T5",
    ("LHR", "F"): "T5",
    ("CDG", "A"): "T1",
    ("CDG", "B"): "T2A",
    ("CDG", "C"): "T2C",
    ("CDG", "K"): "T2E",
    ("CDG", "L"): "T2E",
    ("JFK", "1"): "T1",
    ("JFK", "4"): "T4",
    ("JFK", "5"): "T5",
    ("JFK", "7"): "T7",
    ("JFK", "8"): "T8",
}
