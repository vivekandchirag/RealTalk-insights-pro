"""
youtube_api.py — YouTube Data API v3 helpers for RealTalk

Responsibilities:
  - Parse / validate YouTube video URLs
  - Fetch top N comments using commentThreads.list
  - Handle pagination and quota management
"""

import os
import re
from typing import Optional

import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# ---------------------------------------------------------------------------
# URL Parsing
# ---------------------------------------------------------------------------

# Covers: watch?v=, youtu.be/, /shorts/, /embed/, /live/
_YT_REGEX = re.compile(
    r"(?:https?://)?(?:www\.|m\.)?"
    r"(?:youtube\.com/(?:watch\?.*v=|shorts/|embed/|live/)|youtu\.be/)"
    r"([A-Za-z0-9_-]{11})"
)


def extract_video_id(url: str) -> Optional[str]:
    """
    Returns the 11-character video ID from any recognised YouTube URL format,
    or None if the URL is not a valid YouTube video link.
    """
    if not url or not isinstance(url, str):
        return None
    match = _YT_REGEX.search(url.strip())
    return match.group(1) if match else None


# ---------------------------------------------------------------------------
# Comment Fetching
# ---------------------------------------------------------------------------

def _build_service():
    """Builds and returns an authorised YouTube API service client.
    
    Reads the key from the YOUTUBE_API_KEY environment variable first
    (set by server.py for FastAPI), then falls back to st.secrets
    (for Streamlit usage).
    """
    api_key = os.environ.get("YOUTUBE_API_KEY", "")
    if not api_key or api_key == "YOUR_YOUTUBE_API_KEY_HERE":
        # Fallback: try Streamlit secrets (when running via app.py)
        try:
            import streamlit as st
            api_key = st.secrets["YOUTUBE_API_KEY"]
        except Exception:
            pass
    if not api_key or api_key == "YOUR_YOUTUBE_API_KEY_HERE":
        raise RuntimeError(
            "YouTube API key not found. "
            "Add YOUTUBE_API_KEY to .streamlit/secrets.toml"
        )
    return build("youtube", "v3", developerKey=api_key)


def get_video_comments(video_id: str) -> list[str]:
    """
    Fetches ALL top-level comments for the given video by paginating
    through every page until YouTube returns no nextPageToken.

    Each page fetches 100 comments (API maximum per request).
    Each page costs 1 quota unit → 1,000 comments = 10 units.

    Args:
        video_id: 11-character YouTube video ID.

    Returns:
        A list of all comment text strings for the video.

    Raises:
        RuntimeError: If the API key is missing or comments are disabled.
        HttpError:    For other YouTube API errors (passed to caller).
    """
    service = _build_service()
    comments: list[str] = []
    next_page_token: Optional[str] = None

    while True:
        try:
            request = service.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,          # 100 per page — API maximum
                pageToken=next_page_token,
                textFormat="plainText",
                order="relevance",       # top comments first
            )
            response = request.execute()
        except HttpError as e:
            if e.resp.status == 403:
                raise RuntimeError(
                    "Comments are disabled on this video, or your API key "
                    "does not have permission to access them."
                ) from e
            raise

        for item in response.get("items", []):
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # All pages exhausted

    return comments
