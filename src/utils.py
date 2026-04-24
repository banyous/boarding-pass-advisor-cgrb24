"""Helper utilities."""
from datetime import datetime, time
from typing import Optional, Tuple
from src.config import TERMINAL_HEURISTICS


def infer_terminal(airport: str, gate: Optional[str]) -> Tuple[Optional[str], str]:
    """Infer terminal from airport + gate. Returns (terminal, reasoning)."""
    if not gate:
        return None, "No gate available to infer terminal"
    
    gate_prefix = gate[0].upper() if gate else ""
    key = (airport.upper(), gate_prefix)
    
    if key in TERMINAL_HEURISTICS:
        terminal = TERMINAL_HEURISTICS[key]
        return terminal, f"Inferred {terminal} from gate {gate} at {airport} (heuristic)"
    
    return None, f"No heuristic available for airport={airport}, gate={gate}"


def parse_hours(hours_str: str) -> Optional[Tuple[time, time]]:
    """Parse 'HH:MM-HH:MM' string into (open, close) time tuple."""
    try:
        if "24" in hours_str.lower() or "24h" in hours_str.lower():
            return time(0, 0), time(23, 59)
        
        open_str, close_str = hours_str.split("-")
        open_time = datetime.strptime(open_str.strip(), "%H:%M").time()
        close_time = datetime.strptime(close_str.strip(), "%H:%M").time()
        return open_time, close_time
    except (ValueError, AttributeError):
        return None


def hours_overlap(
    lounge_hours: str,
    now: datetime,
    departure: datetime
) -> bool:
    """Check if lounge is open at any point between now and departure."""
    parsed = parse_hours(lounge_hours)
    if not parsed:
        return False
    
    open_t, close_t = parsed
    now_t = now.time()
    dep_t = departure.time()
    
    # Simple check: lounge open at any point in [now, departure]
    if open_t <= close_t:  # Normal day hours
        return not (dep_t < open_t or now_t > close_t)
    else:  # Overnight (e.g., 22:00-06:00)
        return True  # Simplified: assume overlap for overnight
