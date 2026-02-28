"""
app.py — RealTalk: YouTube Comment Intelligence for Creators
Main Streamlit entry point.

Run with:
    streamlit run app.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from googleapiclient.errors import HttpError

from backend.youtube_api import extract_video_id, get_video_comments
from backend.analyzer import categorize_comments, extract_topics
from backend.utils import calc_sentiment_score, calc_engagement_rate

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RealTalk — YouTube Comment Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS — matches the React screenshots exactly ───────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Base resets ── */
html, body, [class*="css"], [data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"], .main, section[data-testid="stSidebar"],
[data-testid="stVerticalBlock"] {
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background: #0F0F0F !important; }
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Input field ── */
[data-testid="stTextInput"] input,
input[type="text"], input[aria-label="YouTube URL"] {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 12px !important;
    color: #e0e0e0 !important;
    font-size: 0.95rem !important;
    height: 52px !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #555 !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #FF3B3B !important;
    box-shadow: 0 0 0 2px rgba(255,59,59,0.15) !important;
}

/* ── Button ── */
[data-testid="stButton"] > button,
button[kind="primary"], button[kind="secondary"],
.stButton > button {
    background: linear-gradient(135deg, #FF3B3B, #FF6B3B) !important;
    color: white !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 0.9rem !important;
    height: 52px !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    font-family: 'Inter', sans-serif !important;
    cursor: pointer !important;
}
[data-testid="stButton"] > button:hover,
.stButton > button:hover {
    background: linear-gradient(135deg, #e02828, #e05030) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(255,59,59,0.35) !important;
}

/* ── Remove Streamlit default padding/borders ── */
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="column"] { padding: 0 !important; }
.block-container { padding: 0 2rem 2rem 2rem !important; max-width: 100% !important; }
[data-testid="stHorizontalBlock"] { gap: 12px !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] div { border-top-color: #FF3B3B !important; }

/* ── Remove default label for text input ── */
[data-testid="stTextInput"] label { display: none !important; }

/* ── Progress bars ── */
[data-testid="stProgressBarValue"] { background: #FF3B3B !important; border-radius: 6px !important; }
[data-testid="stProgressBar"] { background: #222 !important; border-radius: 6px !important; height: 12px !important; }

/* ── Alert / error / warning ── */
[data-testid="stAlert"] { background: #1a1a1a !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:1rem 0 1.5rem 0;
            border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:2rem;">
    <span style="font-size:1.4rem;font-weight:800;
                 background:linear-gradient(135deg,#FF3B3B,#FF8C42);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;">RealTalk</span>
    <span style="font-family:monospace;font-size:0.7rem;color:#555;
                 background:#1a1a1a;padding:3px 12px;border-radius:20px;
                 border:1px solid #2a2a2a;">v1.0 — beta</span>
</div>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 2.5rem;">
    <h1 style="font-size:clamp(3rem,7vw,5rem);font-weight:800;margin:0 0 0.4rem;
               background:linear-gradient(135deg,#FF3B3B,#FF8C42);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;line-height:1.1;">RealTalk</h1>
    <p style="color:#888;font-size:1.05rem;margin:0 0 0.5rem;">
        YouTube Comment Intelligence for Creators &amp; Audience
    </p>
    <p style="color:#aaa;font-size:0.875rem;max-width:500px;
              margin:0.75rem auto 0;line-height:1.6;">
        Paste a video URL and uncover what your audience truly thinks —
        questions, praise, and criticism decoded instantly.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input Row ─────────────────────────────────────────────────────────────────
col_i, col_b = st.columns([5, 1])
with col_i:
    url_input = st.text_input(
        label="YouTube URL",
        label_visibility="collapsed",
        placeholder="https://youtube.com/watch?v=...",
        key="yt_url",
    )
with col_b:
    analyse_clicked = st.button("✨ Generate Insight", key="analyse_btn")

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _bar_color(weight: int) -> str:
    if weight > 80: return "#FF3B3B"
    if weight > 60: return "#FFD54F"
    return "#4FC3F7"

def _badge_style(trend: str) -> str:
    styles = {
        "hot":    "background:rgba(255,59,59,0.15);color:#FF3B3B;",
        "rising": "background:rgba(255,213,79,0.15);color:#FFD54F;",
        "steady": "background:rgba(255,255,255,0.06);color:#888;",
        "new":    "background:rgba(79,195,247,0.15);color:#4FC3F7;",
    }
    return styles.get(trend, styles["steady"])

def _badges(trend: str) -> str:
    icons = {"hot": "🔥", "rising": "📈", "steady": "📊", "new": "✨"}
    return icons.get(trend, "")

def _comment_rows(items, limit=7, empty_msg="No comments in this category."):
    if not items:
        return f'<p style="color:#555;font-size:0.8rem;font-style:italic;margin:0;">{empty_msg}</p>'
    html = ""
    for item in items[:limit]:
        text  = item["text"][:115] + ("…" if len(item["text"]) > 115 else "")
        count = item["count"]
        cnt   = f"×{count}" if count > 1 else ""
        html += f"""
        <div style="display:flex;justify-content:space-between;align-items:flex-start;
                    gap:0.75rem;padding:0.55rem 0;
                    border-bottom:1px solid rgba(255,255,255,0.04);">
            <span style="color:#BDBDBD;font-size:0.83rem;line-height:1.45;flex:1;">
                &ldquo;{text}&rdquo;
            </span>
            <span style="color:#555;font-family:monospace;font-size:0.78rem;
                         white-space:nowrap;margin-top:2px;">{cnt}</span>
        </div>"""
    return html

# ── Analysis Flow ─────────────────────────────────────────────────────────────
if analyse_clicked:
    url = url_input.strip()

    if not url:
        st.error("⚠️  Please enter a YouTube video URL.")
        st.stop()

    video_id = extract_video_id(url)
    if video_id is None:
        st.error(
            "❌  Invalid YouTube URL.\n\n"
            "Accepted: `youtube.com/watch?v=ID` · `youtu.be/ID` · `youtube.com/shorts/ID`"
        )
        st.stop()

    try:
        with st.spinner("🔍 Fetching all comments from YouTube..."):
            comments = get_video_comments(video_id)
    except RuntimeError as e:
        st.error(f"🔑  {e}")
        st.stop()
    except HttpError as e:
        st.error(f"📡 YouTube API Error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌  Unexpected error: {e}")
        st.stop()

    if not comments:
        st.warning("⚠️  No comments found. Comments may be disabled or the video is too new.")
        st.stop()

    with st.spinner("🧠 Analysing sentiment..."):
        categories    = categorize_comments(comments)
        topics        = extract_topics(comments, top_n=10)
    sentiment_pct  = calc_sentiment_score(categories)
    engagement_lbl = calc_engagement_rate(len(comments))
    sentiment_label = "Positive" if sentiment_pct >= 50 else "Mixed" if sentiment_pct >= 25 else "Critical"

    # ── Metrics Row ──────────────────────────────────────────────────────────
    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 0 1.5rem;'>",
                unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)

    CARD = ("background:#1a1a1a;border:1px solid rgba(255,255,255,0.07);"
            "border-radius:14px;padding:1.3rem 1.5rem;")

    with m1:
        st.markdown(f"""
        <div style="{CARD}">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.6rem;">
                <span style="color:#4FC3F7;font-size:1rem;">💬</span>
                <span style="color:#777;font-size:0.8rem;font-weight:500;">Total Comments Scanned</span>
            </div>
            <div style="font-size:2.1rem;font-weight:700;color:#4FC3F7;">{len(comments):,}</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div style="{CARD}">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.6rem;">
                <span style="color:#69F0AE;font-size:1rem;">📈</span>
                <span style="color:#777;font-size:0.8rem;font-weight:500;">Overall Sentiment Score</span>
            </div>
            <div style="font-size:2.1rem;font-weight:700;color:#69F0AE;">
                {sentiment_pct}%
                <span style="font-size:0.9rem;font-weight:500;margin-left:6px;">{sentiment_label}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div style="{CARD}">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.6rem;">
                <span style="color:#FFD54F;font-size:1rem;">👥</span>
                <span style="color:#777;font-size:0.8rem;font-weight:500;">Estimated Creator Engagement</span>
            </div>
            <div style="font-size:2.1rem;font-weight:700;color:#FFD54F;">{engagement_lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)

    # ── RealTalk Breakdown ────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-size:1.8rem;font-weight:700;color:#F0F0F0;margin:0 0 4px;">
            The <span style="background:linear-gradient(135deg,#FF3B3B,#FF8C42);
                             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                             background-clip:text;">RealTalk</span> Breakdown
        </h2>
        <p style="color:#555;font-size:0.82rem;margin:0;">
            Comments categorized by intent — powered by sentiment analysis
        </p>
    </div>""", unsafe_allow_html=True)

    cq, ca, cc = st.columns(3)

    CAT_CARD = ("background:#1a1a1a;border:1px solid rgba(255,255,255,0.07);"
                "border-radius:14px;padding:1.3rem;")

    with cq:
        st.markdown(f"""
        <div style="{CAT_CARD}border-top:2px solid #4FC3F7;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;
                        padding-bottom:0.7rem;border-bottom:1px solid rgba(255,255,255,0.06);">
                <div style="background:#1e2a30;border-radius:8px;padding:7px;">
                    <span style="font-size:1rem;">❓</span>
                </div>
                <div>
                    <div style="font-weight:600;color:#E0E0E0;font-size:0.95rem;">Questions</div>
                    <div style="color:#555;font-size:0.72rem;">What the audience is asking</div>
                </div>
            </div>
            {_comment_rows(categories["questions"])}
        </div>""", unsafe_allow_html=True)

    with ca:
        st.markdown(f"""
        <div style="{CAT_CARD}border-top:2px solid #FFD54F;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;
                        padding-bottom:0.7rem;border-bottom:1px solid rgba(255,255,255,0.06);">
                <div style="background:#2a2610;border-radius:8px;padding:7px;">
                    <span style="font-size:1rem;">❤️</span>
                </div>
                <div>
                    <div style="font-weight:600;color:#E0E0E0;font-size:0.95rem;">Appreciation</div>
                    <div style="color:#555;font-size:0.72rem;">What's working</div>
                </div>
            </div>
            {_comment_rows(categories["appreciation"])}
        </div>""", unsafe_allow_html=True)

    with cc:
        st.markdown(f"""
        <div style="{CAT_CARD}border-top:2px solid #FF3B3B;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;
                        padding-bottom:0.7rem;border-bottom:1px solid rgba(255,255,255,0.06);">
                <div style="background:#2a1a1a;border-radius:8px;padding:7px;">
                    <span style="font-size:1rem;">⚠️</span>
                </div>
                <div>
                    <div style="font-weight:600;color:#E0E0E0;font-size:0.95rem;">Criticism</div>
                    <div style="color:#555;font-size:0.72rem;">Where to improve</div>
                </div>
            </div>
            {_comment_rows(categories["criticism"])}
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

    # ── Next Video Ideas ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;">
        <div style="background:rgba(255,59,59,0.1);border-radius:10px;padding:8px 10px;">
            <span style="font-size:1.1rem;">💡</span>
        </div>
        <div>
            <h2 style="font-size:1.8rem;font-weight:700;color:#F0F0F0;margin:0 0 2px;">
                Next Video <span style="background:linear-gradient(135deg,#FF3B3B,#FF8C42);
                                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                                       background-clip:text;">Ideas</span>
            </h2>
            <p style="color:#555;font-size:0.82rem;margin:0;">
                Hot topics your audience wants — ranked by demand
            </p>
        </div>
    </div>""", unsafe_allow_html=True)

    if not topics:
        st.info("Not enough noun phrases found to generate topic suggestions.")
    else:
        # Build the full topics card as one HTML block — exact React match
        rows_html = ""
        for topic in topics:
            bar_color  = _bar_color(topic["weight"])
            b_style    = _badge_style(topic["trend"])
            b_icon     = _badges(topic["trend"])
            trend_text = topic["trend"].upper()
            weight_pct = topic["weight"]
            keyword    = topic["keyword"]

            rows_html += f"""
            <div style="display:flex;align-items:center;gap:16px;padding:6px 0;">
                <span style="color:#E0E0E0;font-size:0.875rem;font-weight:500;
                             width:155px;overflow:hidden;text-overflow:ellipsis;
                             white-space:nowrap;text-transform:capitalize;">{keyword}</span>
                <div style="flex:1;height:12px;background:#2a2a2a;border-radius:8px;overflow:hidden;">
                    <div style="width:{weight_pct}%;height:100%;
                                background:{bar_color};border-radius:8px;
                                transition:width 0.6s ease;"></div>
                </div>
                <span style="color:#555;font-family:monospace;font-size:0.78rem;
                             width:36px;text-align:right;">{weight_pct}%</span>
                <span style="font-size:0.65rem;font-weight:700;letter-spacing:0.5px;
                             padding:3px 10px;border-radius:20px;white-space:nowrap;{b_style}">
                    {b_icon} {trend_text}
                </span>
            </div>"""

        st.markdown(f"""
        <div style="background:#1a1a1a;border:1px solid rgba(255,255,255,0.07);
                    border-radius:14px;padding:1.5rem 1.75rem;">
            {rows_html}
        </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3rem 0 1.5rem;color:#444;font-size:0.75rem;
            border-top:1px solid rgba(255,255,255,0.05);margin-top:3rem;">
    Built for creators who listen.
    <span style="background:linear-gradient(135deg,#FF3B3B,#FF8C42);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 font-weight:600;">RealTalk</span> © 2026
</div>""", unsafe_allow_html=True)
