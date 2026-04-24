"""Lounge discovery from public web sources."""
import json
import os
from typing import List
from src.models import Lounge
from src.config import LOUNGE_CACHE_PATH


def load_lounge_cache() -> dict:
    """Load cached lounge data."""
    if not os.path.exists(LOUNGE_CACHE_PATH):
        return {}
    with open(LOUNGE_CACHE_PATH, "r") as f:
        return json.load(f)


def fetch_lounges_for_airport(airport_code: str) -> List[Lounge]:
    """Fetch lounges for an airport. 
    
    For demo: uses pre-curated cache.
    In production: scrape airport sites, LoungeBuddy, Priority Pass API, etc.
    """
    cache = load_lounge_cache()
    airport_data = cache.get(airport_code.upper(), [])
    
    return [Lounge(**lounge_data) for lounge_data in airport_data]


# ========== PRE-BUILD YOUR CACHE ==========
# data/lounges_cache.json should look like:
"""
{
  "LHR": [
    {
      "lounge_id": "lhr_t5_ba_galleries_first",
      "name": "British Airways Galleries First Lounge",
      "airport_code": "LHR",
      "terminal": "T5",
      "opening_hours": "05:00-22:00",
      "amenities": ["Hot food", "Showers", "Champagne bar", "Wi-Fi", "Quiet zone"],
      "access_notes": "BA First Class, Oneworld Emerald, or paid entry £65",
      "source_url": "https://www.britishairways.com/en-gb/information/airport-information/lounges/galleries-first-heathrow"
    },
    {
      "lounge_id": "lhr_t5_plaza_premium",
      "name": "Plaza Premium Lounge",
      "airport_code": "LHR",
      "terminal": "T5",
      "opening_hours": "05:30-22:00",
      "amenities": ["Hot buffet", "Bar", "Showers", "Wi-Fi"],
      "access_notes": "Priority Pass, LoungeKey, or paid entry £50",
      "source_url": "https://www.plazapremiumlounge.com/en/locations/lhr-london-heathrow/plaza-premium-lounge-departures-terminal-5"
    },
    {
      "lounge_id": "lhr_t2_united_club",
      "name": "United Club",
      "airport_code": "LHR",
      "terminal": "T2",
      "opening_hours": "06:00-21:00",
      "amenities": ["Breakfast", "Bar", "Wi-Fi"],
      "access_notes": "United Global Services, Star Alliance Gold",
      "source_url": "https://www.united.com/ual/en/us/fly/travel/airport/lounges.html"
    }
  ],
  "CDG": [
    {
      "lounge_id": "cdg_t2e_air_france_lounge",
      "name": "Air France Lounge",
      "airport_code": "CDG",
      "terminal": "T2E",
      "opening_hours": "05:00-23:00",
      "amenities": ["Hot food", "Champagne", "Showers", "Wi-Fi"],
      "access_notes": "Air France La Premiere, SkyTeam Elite Plus",
      "source_url": "https://www.airfrance.com/us/en/common/voyage-travel/salon-lounge.htm"
    }
  ]
}
"""
