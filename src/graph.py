"""LangGraph orchestration of the advisory pipeline."""
from datetime import datetime, timedelta
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END

from src.models import BoardingPass, Lounge, RankedLounge, Advisory
from src.nodes.ocr import extract_from_image, extract_from_text
from src.nodes.lounge_fetch import fetch_lounges_for_airport
from src.nodes.ranker import filter_and_rank
from src.nodes.advisor import generate_advisory
from src.utils import infer_terminal
from src.config import OCR_CONFIDENCE_THRESHOLD


class PipelineState(TypedDict):
    """State passed between LangGraph nodes."""
    image_path: Optional[str]
    text_input: Optional[str]
    boarding_pass: Optional[BoardingPass]
    lounges: List[Lounge]
    ranked_lounges: List[RankedLounge]
    advisory: Optional[Advisory]
    error: Optional[str]


def node_ocr(state: PipelineState) -> PipelineState:
    """OCR node: extract from image or text."""
    if state.get("image_path"):
        bp = extract_from_image(state["image_path"])
    elif state.get("text_input"):
        bp = extract_from_text(state["text_input"])
    else:
        return {**state, "error": "No input provided"}
    
    # If OCR confidence low AND we have no text fallback, request manual input
    if bp.ocr_confidence < OCR_CONFIDENCE_THRESHOLD and not state.get("text_input"):
        return {**state, "boarding_pass": bp, "error": "OCR confidence too low"}
    
    return {**state, "boarding_pass": bp}


def node_terminal_inference(state: PipelineState) -> PipelineState:
    """Infer terminal if missing."""
    bp = state["boarding_pass"]
    if not bp.terminal and bp.airport_iata and bp.gate:
        inferred, reasoning = infer_terminal(bp.airport_iata, bp.gate)
        if inferred:
            bp.terminal = inferred
            bp.assumptions.append(reasoning)
    return {**state, "boarding_pass": bp}


def node_fetch_lounges(state: PipelineState) -> PipelineState:
    """Fetch lounges for airport."""
    bp = state["boarding_pass"]
    if not bp.airport_iata:
        return {**state, "lounges": [], "error": "No airport code to fetch lounges"}
    
    lounges = fetch_lounges_for_airport(bp.airport_iata)
    return {**state, "lounges": lounges}


def node_rank(state: PipelineState) -> PipelineState:
    """Filter and rank lounges."""
    bp = state["boarding_pass"]
    now = datetime.now()
    
    # Parse departure time (simplified - assume same day)
    try:
        dep_time = datetime.strptime(bp.departure_time or "12:00", "%H:%M").time()
        departure = datetime.combine(now.date(), dep_time)
        if departure < now:  # If already past, assume tomorrow
            departure += timedelta(days=1)
    except ValueError:
        departure = now + timedelta(hours=2)
    
    ranked = filter_and_rank(state["lounges"], bp, now, departure)
    return {**state, "ranked_lounges": ranked}


def node_advisor(state: PipelineState) -> PipelineState:
    """Generate LLM advisory."""
    bp = state["boarding_pass"]
    advisory = generate_advisory(
        bp, 
        state["ranked_lounges"], 
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    return {**state, "advisory": advisory}


def build_graph():
    """Build the LangGraph pipeline."""
    workflow = StateGraph(PipelineState)
    
    workflow.add_node("ocr", node_ocr)
    workflow.add_node("terminal_inference", node_terminal_inference)
    workflow.add_node("fetch_lounges", node_fetch_lounges)
    workflow.add_node("rank", node_rank)
    workflow.add_node("advisor", node_advisor)
    
    workflow.set_entry_point("ocr")
    workflow.add_edge("ocr", "terminal_inference")
    workflow.add_edge("terminal_inference", "fetch_lounges")
    workflow.add_edge("fetch_lounges", "rank")
    workflow.add_edge("rank", "advisor")
    workflow.add_edge("advisor", END)
    
    return workflow.compile()


# Module-level singleton
app_graph = build_graph()


def run_pipeline(image_path: Optional[str] = None, text_input: Optional[str] = None) -> PipelineState:
    """Run the full pipeline."""
    initial_state: PipelineState = {
        "image_path": image_path,
        "text_input": text_input,
        "boarding_pass": None,
        "lounges": [],
        "ranked_lounges": [],
        "advisory": None,
        "error": None,
    }
    return app_graph.invoke(initial_state)
