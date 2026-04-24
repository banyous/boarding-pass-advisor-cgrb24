"""FastAPI application entry point."""
import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import Optional
from src.graph import run_pipeline
from src.models import Advisory


app = FastAPI(title="Boarding Pass Advisor", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/advisory", response_model=Advisory)
async def advisory(
    image: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
):
    """Generate advisory from boarding pass image or text."""
    if not image and not text:
        raise HTTPException(status_code=400, detail="Provide image or text input")
    
    image_path = None
    if image:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await image.read())
            image_path = tmp.name
    
    try:
        result = run_pipeline(image_path=image_path, text_input=text)
        if result.get("error") and not result.get("advisory"):
            raise HTTPException(status_code=422, detail=result["error"])
        return result["advisory"]
    finally:
        if image_path and os.path.exists(image_path):
            os.unlink(image_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
