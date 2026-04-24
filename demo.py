"""Demo script showing 3 scenarios with REAL boarding pass images."""
import os
from src.graph import run_pipeline

SAMPLES_DIR = "data/sample_passes"


SCENARIOS = [
    {
        "name": "Scenario 1: Standard boarding pass (full data)",
        "image": f"{SAMPLES_DIR}/1.png",
        "description": "Full boarding pass with terminal, gate, all fields present",
    },
    {
        "name": "Scenario 2: Missing terminal (must infer from gate)",
        "image": f"{SAMPLES_DIR}/2.png",
        "description": "Terminal not printed; pipeline infers from gate heuristics",
    },
    {
        "name": "Scenario 3: Low OCR confidence → fallback to text",
        "image": None,
        "text": "Flight AF1234 from CDG. Terminal 2E. Gate K45. Departure 09:15.",
        "description": "Fallback path when image OCR fails or is unavailable",
    },
]


def run_demo():
    for i, scenario in enumerate(SCENARIOS, 1):
        print(f"\n{'='*70}")
        print(f"  {scenario['name']}")
        print(f"  {scenario['description']}")
        print(f"{'='*70}\n")
        
        if scenario.get("image") and os.path.exists(scenario["image"]):
            print(f"📸 Processing image: {scenario['image']}")
            result = run_pipeline(image_path=scenario["image"])
        elif scenario.get("text"):
            print(f"📝 Processing text: {scenario['text']}")
            result = run_pipeline(text_input=scenario["text"])
        else:
            print(f"⚠️  Missing input for scenario")
            continue
        
        bp = result["boarding_pass"]
        if bp is None:
            print(f"❌ No extraction result")
            continue
            
        print(f"\n📋 EXTRACTED FIELDS:")
        print(f"   Airport:     {bp.airport_iata}")
        print(f"   Destination: {bp.destination_iata}")
        print(f"   Terminal:    {bp.terminal}")
        print(f"   Gate:        {bp.gate}")
        print(f"   Flight:      {bp.flight_number}")
        print(f"   Departure:   {bp.departure_time}")
        print(f"   OCR Confidence: {bp.ocr_confidence:.2f}")
        
        if bp.assumptions:
            print(f"\n⚠️  ASSUMPTIONS:")
            for a in bp.assumptions:
                print(f"   - {a}")
        
        advisory = result.get("advisory")
        if advisory and advisory.summary_text:
            print(f"\n💼 ADVISORY:")
            print(advisory.summary_text)
            
            if advisory.warnings:
                print(f"\n⚠️  WARNINGS:")
                for w in advisory.warnings:
                    print(f"   - {w}")
            
            if advisory.citations:
                print(f"\n📚 CITATIONS:")
                for c in advisory.citations:
                    print(f"   - {c}")
        else:
            print(f"❌ No advisory generated")


if __name__ == "__main__":
    run_demo()
