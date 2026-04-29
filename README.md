# Boarding Pass Advisor

Simple AI tool that reads a boarding pass (image or text) and gives a quick airport advisory (mainly lounge suggestions).

Built as a prototype to show an agent-style pipeline using LangGraph + LLMs.

---

## How it works

Pipeline:

Input (image/text)
→ OCR (GPT-4o extracts flight info)
→ Terminal inference (if missing, simple rules)
→ Lounge lookup (from JSON cache)
→ Filter + rank (by terminal + time)
→ Advisory (GPT-4o-mini generates final output)

---

## What it does

- Extracts: airport, gate, terminal, flight, time
- Finds lounges for that airport
- Filters ones that are open
- Prefers same terminal
- Generates a short recommendation with sources

---

## Key choices

- GPT-4o for OCR → better than Tesseract for messy boarding passes
- JSON lounge cache → simple + reliable (no scraping issues)
- LangGraph → clean pipeline, easy to test
- Heuristics → used for terminal + ranking (kept simple on purpose)

---

## Edge cases handled

- Missing terminal → inferred from gate
- Low OCR confidence → fallback to text
- No lounges → explicit message
- Lounge closing soon → warning
- Cross-terminal → flagged
- Missing fields → not guessed

---

## Project structure

boarding_pass_advisor/
├── src/
├── data/
├── tests/
├── demo.py

---

## Run

Install:
pip install -r requirements.txt

Setup:
cp .env.example .env
(add OPENAI_API_KEY)

Run demo:
python demo.py

Run API:
uvicorn src.main:app --reload

---

## API

POST /advisory

Example:
curl -X POST http://localhost:8000/advisory -F "image=@pass.jpg"

---

## Limitations

- Few airports only (LHR, CDG, JFK, LAX)
- No live lounge data
- OCR not fully tested on all formats
- No real-time updates (e.g. gate changes)

---

## Stack

Python, LangGraph, OpenAI (GPT-4o, GPT-4o-mini), FastAPI, Pydantic, pytest

---

Built by Youcef Benkhedda — April 2026
