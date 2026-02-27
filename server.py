"""
server.py — RealTalk FastAPI Backend
Runs on http://localhost:8000

Start with:
    python server.py
  OR
    uvicorn server:app --reload --port 8000
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from googleapiclient.errors import HttpError

from backend.youtube_api import extract_video_id, get_video_comments
from backend.analyzer import categorize_comments, extract_topics
from backend.utils import calc_sentiment_score, calc_engagement_rate

# ── Load API key ──────────────────────────────────────────────────────────────
# On Render: set YOUTUBE_API_KEY as an Environment Variable in the dashboard.
# Locally:   it falls back to reading .streamlit/secrets.toml.

def _load_api_key() -> str:
    # 1. env var (Render / any cloud host)
    key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if key and key != "YOUR_YOUTUBE_API_KEY_HERE":
        return key

    # 2. local fallback — read .streamlit/secrets.toml
    secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
    if os.path.exists(secrets_path):
        with open(secrets_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("YOUTUBE_API_KEY"):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val and val != "YOUR_YOUTUBE_API_KEY_HERE":
                        return val

    raise RuntimeError(
        "YOUTUBE_API_KEY not found.\n"
        "  - Cloud: set it as an Environment Variable in your Render dashboard.\n"
        "  - Local: add it to .streamlit/secrets.toml"
    )

os.environ["YOUTUBE_API_KEY"] = _load_api_key()


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="RealTalk API", version="1.0.0")

# Manual CORS — guaranteed to work on every response including errors
@app.middleware("http")
async def add_cors(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(status_code=200)
    else:
        response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# ── Request / Response models ─────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    url: str

class CommentItem(BaseModel):
    text: str
    count: int

class TopicItem(BaseModel):
    keyword: str
    weight: int
    trend: str

class AnalyzeResponse(BaseModel):
    total_comments: int
    sentiment_score: float
    sentiment_label: str
    engagement: str
    questions:    list[CommentItem]
    appreciation: list[CommentItem]
    criticism:    list[CommentItem]
    topics:       list[TopicItem]

# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "service": "RealTalk API"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    """
    Accepts a YouTube URL, fetches all comments, analyses them, and
    returns structured data matching the React component data shapes.
    """
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL is required.")

    video_id = extract_video_id(url)
    if video_id is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL. Accepted: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/shorts/ID"
        )

    # Fetch comments
    try:
        comments = get_video_comments(video_id)
    except RuntimeError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except HttpError as e:
        raise HTTPException(status_code=e.resp.status, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    if not comments:
        raise HTTPException(
            status_code=404,
            detail="No comments found. Comments may be disabled or the video has no comments."
        )

    # Analyse
    categories = categorize_comments(comments)
    topics     = extract_topics(comments, top_n=10)
    sentiment  = calc_sentiment_score(categories)
    engagement = calc_engagement_rate(len(comments))
    sentiment_label = (
        "Positive" if sentiment >= 50 else
        "Mixed"    if sentiment >= 25 else "Critical"
    )

    return AnalyzeResponse(
        total_comments=len(comments),
        sentiment_score=sentiment,
        sentiment_label=sentiment_label,
        engagement=engagement,
        questions=[CommentItem(**c)    for c in categories["questions"]],
        appreciation=[CommentItem(**c) for c in categories["appreciation"]],
        criticism=[CommentItem(**c)    for c in categories["criticism"]],
        topics=[TopicItem(**t)         for t in topics],
    )


# ── Dev runner ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("\n🚀  RealTalk API running at http://localhost:8000")
    print("📡  React frontend should be at http://localhost:8080\n")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
