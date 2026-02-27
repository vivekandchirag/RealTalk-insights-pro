"""
utils.py — Shared metric helpers for RealTalk

Provides:
  - calc_sentiment_score : % of engaged comments that are positive
  - calc_engagement_rate : rough engagement label based on comment volume
"""

from backend.analyzer import Categories


def calc_sentiment_score(categories: Categories) -> float:
    """
    Returns the percentage of categorised comments that are Appreciation.

    Formula:
        appreciation_count / (questions + appreciation + criticism) * 100

    Neutral comments are excluded from the denominator because they carry
    no signal — this keeps the metric focused on intent-bearing comments.

    Returns:
        Float between 0.0 and 100.0 (rounded to 1 decimal).
        Returns 0.0 if no categorised comments exist.
    """
    appreciation = len(categories["appreciation"])
    questions    = len(categories["questions"])
    criticism    = len(categories["criticism"])
    total = questions + appreciation + criticism

    if total == 0:
        return 0.0
    return round((appreciation / total) * 100, 1)


def calc_engagement_rate(total_comments: int) -> str:
    """
    Returns a rough engagement-rate display string.

    Without access to view-count data from the YouTube API (requires an
    extra authenticated call), we infer engagement tier from comment volume:

        ≥ 5 000  comments → "High (5 000 + comments)"
        ≥ 1 000  comments → "Good (1 000 + comments)"
        ≥   200  comments → "Moderate"
        <   200  comments → "Low / new video"

    This is shown as a qualitative label in the MetricsRow.

    Args:
        total_comments: Number of comments fetched from the video.

    Returns:
        A short human-readable engagement label string.
    """
    if total_comments >= 5_000:
        return "🔥 High"
    if total_comments >= 1_000:
        return "📈 Good"
    if total_comments >= 200:
        return "📊 Moderate"
    return "🌱 Early / Low"
