# Boarding Pass Advisor

AI-powered airport lounge advisor that extracts data from boarding passes and recommends lounges based on terminal, hours, and amenities.

## Setup

1. Install dependencies:

   pip install -r requirements.txt

2. Copy .env.example to .env and add your OpenAI API key:

   cp .env.example .env
   # Edit .env with your API key

3. Run the demo:

   python demo.py

4. Start the API server:

   uvicorn src.main:app --reload

## API Endpoints

- POST /advisory - Upload boarding pass image or text to get lounge recommendations

## Testing

Run tests with pytest:

   pytest tests/

## Cache Setup

Populate data/lounges_cache.json with lounge data for airports you care about (see example in src/nodes/lounge_fetch.py)
