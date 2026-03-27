"""
app.py
------
FastAPI REST API server exposing FLAMES endpoints.
Responsibility: Friend 1 (Backend)

Endpoints:
  POST /api/flames          → Calculate FLAMES result
  GET  /api/flames/options  → List all FLAMES outcomes
  GET  /health              → Health check
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, validator
from flames_engine import calculate_flames, FLAMES_LABELS, FLAMES_EMOJIS
import os

app = FastAPI(
    title="FLAMES Game API",
    description="Backend API for the FLAMES relationship calculator game",
    version="1.0.0",
)

# Allow frontend (running on different port in dev) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ────────────────────────────────────────────────

class FlamesRequest(BaseModel):
    name1: str
    name2: str
    generate_story: bool = False  # If True, calls the AI model for a story

    @validator("name1", "name2")
    def name_must_not_be_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty")
        if not any(c.isalpha() for c in v):
            raise ValueError("Name must contain at least one letter")
        return v


class StepResponse(BaseModel):
    step_number: int
    description: str
    detail: str | None


class FlamesResponse(BaseModel):
    name1: str
    name2: str
    common_letters: list[str]
    remaining_name1: str
    remaining_name2: str
    total_count: int
    elimination_order: list[str]
    winner: str
    label: str
    emoji: str
    steps: list[StepResponse]
    story: str | None = None


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "FLAMES API"}


@app.get("/api/flames/options")
def get_flames_options():
    """Return all possible FLAMES outcomes with labels and emojis."""
    return {
        letter: {"label": label, "emoji": FLAMES_EMOJIS[letter]}
        for letter, label in FLAMES_LABELS.items()
    }


@app.post("/api/flames", response_model=FlamesResponse)
async def calculate(request: FlamesRequest):
    """
    Calculate FLAMES result for two names.
    Optionally generates an AI story via the model service.
    """
    try:
        result = calculate_flames(request.name1, request.name2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

    story = None
    if request.generate_story:
        try:
            # Import here to avoid circular imports; model service is optional
            from model.story_generator import generate_story
            story = await generate_story(
                name1=result.name1,
                name2=result.name2,
                outcome=result.label,
                emoji=result.emoji,
            )
        except Exception as e:
            story = f"(Story unavailable: {str(e)})"

    return FlamesResponse(
        name1=result.name1,
        name2=result.name2,
        common_letters=result.common_letters,
        remaining_name1=result.remaining_name1,
        remaining_name2=result.remaining_name2,
        total_count=result.total_count,
        elimination_order=result.elimination_order,
        winner=result.winner,
        label=result.label,
        emoji=result.emoji,
        steps=[
            StepResponse(
                step_number=s.step_number,
                description=s.description,
                detail=s.detail,
            )
            for s in result.steps
        ],
        story=story,
    )


# ─── Serve Frontend (production) ─────────────────────────────────────────────

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend(full_path: str):
        index = os.path.join(FRONTEND_DIR, "index.html")
        return FileResponse(index)


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
