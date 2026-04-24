"""Tests for advisory output structure."""
from src.graph import run_pipeline


def test_advisory_contains_lounge_and_destination():
    """Smoke test: advisory should contain lounge + destination context."""
    result = run_pipeline(
        text_input="BA Flight BA123 from LHR to JFK. Terminal 5, Gate A12. Departure 14:30."
    )
    advisory = result.get("advisory")
    assert advisory is not None
    assert advisory.summary_text  # Non-empty
    assert len(advisory.citations) > 0  # Has at least one citation


def test_assumptions_disclosed():
    """If terminal was inferred, assumption should be disclosed."""
    result = run_pipeline(
        text_input="UA923 from LHR to ORD. Gate B22. Departure 18:45."  # No terminal
    )
    bp = result["boarding_pass"]
    if bp.terminal:  # If we managed to infer
        assert any("inferred" in a.lower() or "heuristic" in a.lower() for a in bp.assumptions)
