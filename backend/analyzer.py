"""
analyzer.py — Comment categorization and topic extraction for RealTalk

Responsibilities:
  - Categorize comments into Questions / Appreciation / Criticism / Neutral
  - Extract top N noun phrases as next video topic suggestions
"""

from collections import Counter
from typing import TypedDict

from textblob import TextBlob


# ---------------------------------------------------------------------------
# Type Definitions
# ---------------------------------------------------------------------------

class CommentItem(TypedDict):
    text: str
    count: int


class Categories(TypedDict):
    questions: list[CommentItem]
    appreciation: list[CommentItem]
    criticism: list[CommentItem]
    neutral: list[str]


class TopicItem(TypedDict):
    keyword: str
    weight: int   # 0–100 relative score
    trend: str    # "hot" | "rising" | "steady" | "new"


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

APPRECIATION_THRESHOLD = 0.3   # TextBlob polarity > this → Appreciation
CRITICISM_THRESHOLD = -0.1     # TextBlob polarity < this → Criticism


# ---------------------------------------------------------------------------
# Core Logic
# ---------------------------------------------------------------------------

def _get_polarity(text: str) -> float:
    """Returns TextBlob sentiment polarity for the given text."""
    return TextBlob(text).sentiment.polarity


def categorize_comments(comments: list[str]) -> Categories:
    """
    Categorises each comment into one of four buckets:

    Priority order (first match wins):
      1. Questions  — comment contains a '?'
      2. Appreciation — polarity > APPRECIATION_THRESHOLD
      3. Criticism    — polarity < CRITICISM_THRESHOLD
      4. Neutral      — everything else

    To surface the *most representative* comments in each bucket we
    deduplicate exact text and count how many times it appeared, then
    sort by count descending.  This mirrors the ×count display in the
    React UI (NichodCards component).

    Returns:
        A dict with keys "questions", "appreciation", "criticism", "neutral".
        Each value for the first three is a list of CommentItem dicts
        (text + count).  "neutral" is a plain list of strings.
    """
    question_counter: Counter = Counter()
    appreciation_counter: Counter = Counter()
    criticism_counter: Counter = Counter()
    neutral_list: list[str] = []

    for raw in comments:
        text = raw.strip()
        if not text:
            continue

        if "?" in text:
            question_counter[text] += 1
        else:
            polarity = _get_polarity(text)
            if polarity > APPRECIATION_THRESHOLD:
                appreciation_counter[text] += 1
            elif polarity < CRITICISM_THRESHOLD:
                criticism_counter[text] += 1
            else:
                neutral_list.append(text)

    def _to_items(counter: Counter) -> list[CommentItem]:
        return [
            CommentItem(text=t, count=c)
            for t, c in counter.most_common()
        ]

    return Categories(
        questions=_to_items(question_counter),
        appreciation=_to_items(appreciation_counter),
        criticism=_to_items(criticism_counter),
        neutral=neutral_list,
    )


def extract_topics(comments: list[str], top_n: int = 10) -> list[TopicItem]:
    """
    Extracts the top `top_n` most-frequent noun phrases from all comments.

    Trend is assigned by rank position (matching the React TopicHeatmap):
      - Rank 1–2  → "hot"
      - Rank 3–4  → "rising"
      - Rank 5–7  → "steady"
      - Rank 8+   → "new"

    The `weight` (0–100) is normalised relative to the most frequent topic.

    Returns:
        Sorted list of TopicItem dicts (highest weight first).
    """
    phrase_counter: Counter = Counter()

    for comment in comments:
        blob = TextBlob(comment.lower())
        for phrase in blob.noun_phrases:
            phrase = phrase.strip()
            # Filter noise: skip single-character phrases and very long ones
            if 2 <= len(phrase) <= 40:
                phrase_counter[phrase] += 1

    top = phrase_counter.most_common(top_n)
    if not top:
        return []

    max_count = top[0][1]  # frequency of the most common phrase

    def _assign_trend(rank: int) -> str:
        if rank <= 2:
            return "hot"
        if rank <= 4:
            return "rising"
        if rank <= 7:
            return "steady"
        return "new"

    result: list[TopicItem] = []
    for rank, (phrase, count) in enumerate(top, start=1):
        weight = round((count / max_count) * 100) if max_count > 0 else 0
        result.append(
            TopicItem(
                keyword=phrase.title(),
                weight=weight,
                trend=_assign_trend(rank),
            )
        )

    return result
