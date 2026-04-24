"""Filter and rank lounges."""
from datetime import datetime
from typing import List
from src.models import Lounge, RankedLounge, BoardingPass
from src.utils import hours_overlap


def filter_and_rank(
    lounges: List[Lounge],
    boarding_pass: BoardingPass,
    now: datetime,
    departure: datetime,
) -> List[RankedLounge]:
    """Filter and rank lounges based on boarding pass context."""
    ranked = []
    
    for lounge in lounges:
        # Same airport check (should already be filtered)
        if lounge.airport_code.upper() != (boarding_pass.airport_iata or "").upper():
            continue
        
        # Hours overlap
        open_at_departure = hours_overlap(lounge.opening_hours, now, departure)
        if not open_at_departure:
            continue
        
        # Same terminal check
        bp_terminal = (boarding_pass.terminal or "").upper()
        lounge_terminal = (lounge.terminal or "").upper()
        same_terminal = bp_terminal == lounge_terminal
        
        # Score: same terminal = 10, different terminal = 5
        score = 10.0 if same_terminal else 5.0
        rank_reason = (
            f"Same terminal ({lounge_terminal})"
            if same_terminal
            else f"Alternative terminal ({lounge_terminal} vs your {bp_terminal or 'unknown'}); walk time applies"
        )
        
        ranked.append(RankedLounge(
            lounge=lounge,
            score=score,
            rank_reason=rank_reason,
            same_terminal=same_terminal,
            open_at_departure=open_at_departure,
        ))
    
    # Sort by score descending
    ranked.sort(key=lambda r: r.score, reverse=True)
    return ranked
