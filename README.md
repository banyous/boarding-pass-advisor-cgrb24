# Boarding Pass Advisor

An AI-powered travel assistant that transforms boarding pass images into instant airport advisory recommendations. Built as a technical prototype for agentic systems using LangGraph and GPT-4o.

## Architecture
The system is orchestrated as a **LangGraph state machine** with the following pipeline:
1. **OCR Node:** GPT-4o Vision extracts structured fields (IATA codes, Gate, Terminal).
2. **Heuristics:** Fallback logic for terminal inference if gate data is ambiguous.
3. **Lounge Discovery:** Fetches data from a curated JSON cache (extensible to live APIs).
4. **Ranking:** Filters by airport/hours and scores by terminal proximity.
5. **Advisory LLM:** GPT-4o-mini generates a grounded summary with Pydantic-validated citations.

## Project Structure
\`\`\`text
boarding_pass_advisor/
├── src/
│   ├── graph.py             # LangGraph orchestration
│   ├── nodes/               # Individual pipeline logic
│   └── main.py              # FastAPI entry point
├── data/                    # Lounge cache & samples
├── tests/                   # Pytest suite
└── demo.py                  # CLI test scenarios
\`\`\`

## Setup & Usage

### 1. Installation
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Configuration
Create a \`.env\` file from the template and add your OpenAI API key:
\`\`\`bash
cp .env.example .env
\`\`\`

### 3. Execution
* **CLI Demo:** \`python demo.py\`
* **API Server:** \`uvicorn src.main:app --reload\`
* **Tests:** \`pytest tests/ -v\`

## API Usage
**POST \`/advisory\`** (Accepts image or text fallback)
\`\`\`bash
curl -X POST http://localhost:8000/advisory -F "image=@pass.jpg"
\`\`\`

## Technical Decisions
* **Multimodal OCR:** Used GPT-4o over Tesseract for zero-shot JSON extraction.
* **Curated Cache:** Used \`data/lounges_cache.json\` for deterministic testing.
* **Grounded Generation:** Enforced strict RAG constraints to prevent hallucinations.

**Built by:** Youcef Benkhedda, PhD (April 2026)
