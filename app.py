import os
import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from agents.router_agent import RouterAgent
from agents.answer_agent import AnswerAgent
from utils.images import fetch_image_url
from utils.image_map import get_image_info

load_dotenv()

st.set_page_config(
    page_title="Ella Tourism Assistant",
    layout="centered",
)

IMAGE_DIR = Path(__file__).resolve().parent / "image"
BG_IMAGE_PATH = IMAGE_DIR / "hero-bg.jpg"
LOGO_IMAGE_PATH = IMAGE_DIR / "logo.png"
MASCOT_IMAGE_PATH = IMAGE_DIR / "mascot.png"

@st.cache_data
def get_base64_image(path: Path) -> str | None:
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


bg_base64 = get_base64_image(BG_IMAGE_PATH)
bg_css_url = f"data:image/jpeg;base64,{bg_base64}" if bg_base64 else ""

logo_base64 = get_base64_image(LOGO_IMAGE_PATH)
logo_data_url = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""

mascot_base64 = get_base64_image(MASCOT_IMAGE_PATH)
mascot_data_url = f"data:image/png;base64,{mascot_base64}" if mascot_base64 else ""

CATEGORY_CARDS = [
    {
        "title": "Attractions",
        "desc": "Nine Arch Bridge, Ella Rock, Little Adam's Peak & more",
        "color": "#3d5a80",
    },
    {
        "title": "Hotels",
        "desc": "From budget hostels to resorts overlooking the Gap",
        "color": "#5c4d7d",
    },
    {
        "title": "Transport",
        "desc": "Trains, buses, and tuk-tuks around the hill country",
        "color": "#2f6b5e",
    },
    {
        "title": "Culture",
        "desc": "Local food, etiquette, festivals & history",
        "color": "#8a5a3b",
    },
]

# CSS 
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {{
        font-family: 'Inter', sans-serif;
    }}

    /* Hero header with background image */
    .hero-banner {{
        position: relative;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 2rem;
        min-height: 220px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        background-image:
            linear-gradient(180deg, rgba(15,23,32,0.55) 0%, rgba(15,23,32,0.82) 100%),
            url("{bg_css_url}");
        background-size: cover;
        background-position: center;
        animation: fadeIn 0.9s ease-in-out;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }}

    .hero-title {{
        color: #ffffff;
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.4rem;
    }}

    .hero-subtitle {{
        color: #d8dde3;
        font-size: 0.98rem;
        font-weight: 400;
        max-width: 480px;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    /* Section labels */
    .section-label {{
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #8a8f98;
        margin: 1.6rem 0 0.7rem 0;
    }}

    /* Category cards */
    .cat-card {{
        border-radius: 10px;
        padding: 0.9rem 1rem;
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);
        border-left: 3px solid var(--accent);
        transition: background 0.2s ease, border-color 0.2s ease;
        margin-bottom: 0.6rem;
        height: 100%;
    }}
    .cat-card:hover {{
        background: rgba(255,255,255,0.06);
        border-color: rgba(255,255,255,0.2);
    }}
    .cat-title {{
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
        color: #eaecef;
    }}
    .cat-desc {{
        font-size: 0.8rem;
        color: #9aa0a8;
        line-height: 1.35rem;
    }}

    /* Answer card */
    .answer-box {{
        background: rgba(61, 90, 128, 0.08);
        border-left: 3px solid #3d5a80;
        border-radius: 8px;
        padding: 1.1rem 1.3rem;
        line-height: 1.6rem;
        animation: fadeIn 0.5s ease-in-out;
    }}

    /* Buttons */
    div.stButton > button {{
        border-radius: 8px;
        font-weight: 500;
        transition: opacity 0.15s ease;
    }}
    div.stButton > button:hover {{
        opacity: 0.88;
    }}

    /* Image gallery */
    .img-card {{
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03);
        animation: fadeIn 0.6s ease-in-out;
        margin-bottom: 0.8rem;
    }}
    .img-card img {{
        width: 100%;
        height: 150px;
        object-fit: cover;
        display: block;
    }}
    .img-card-body {{
        padding: 0.55rem 0.7rem 0.65rem 0.7rem;
    }}
    .img-card-title {{
        font-size: 0.82rem;
        font-weight: 600;
        color: #eaecef;
        margin-bottom: 0.15rem;
    }}
    .img-card-price {{
        font-size: 0.78rem;
        color: #7fb88f;
        font-weight: 600;
    }}
    .img-card-credit {{
        font-size: 0.68rem;
        color: #6b7178;
        margin-top: 0.2rem;
    }}
    .img-card-credit a {{
        color: #6b7178;
    }}

    /* Navbar / logo */
    .app-navbar {{
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 1.1rem;
        animation: fadeIn 0.7s ease-in-out;
    }}
    .app-navbar img {{
        width: 150px;
        height: 150px;
        object-fit: contain;
    }}
    .app-navbar-name {{
        font-weight: 700;
        font-size: 2.5rem;
        color: #eaecef;
        letter-spacing: -0.01em;
    }}

    /* Answer header with mascot avatar */
    .answer-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 1.6rem 0 0.7rem 0;
    }}
    .answer-header img {{
        width: 70px;
        height: 70px;
        object-fit: contain;
        animation: nod 2.4s ease-in-out infinite;
    }}
    .answer-header .section-label {{
        margin: 0;
    }}
    @keyframes nod {{
        0%, 100% {{ transform: rotate(0deg); }}
        50% {{ transform: rotate(-6deg); }}
    }}

    /* Floating mascot widget (fixed, bottom-right) */
    .mascot-wrap {{
        position: fixed;
        bottom: 22px;
        right: 22px;
        z-index: 999999;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        pointer-events: none;
    }}
    .mascot-bubble {{
        background: #ffffff;
        color: #1a1a1a;
        padding: 0.5rem 0.85rem;
        border-radius: 14px 14px 2px 14px;
        font-size: 0.78rem;
        font-weight: 600;
        line-height: 1.15rem;
        margin-bottom: 0.5rem;
        max-width: 165px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        animation: bubblePop 0.5s ease-out 0.3s both, floatSoft 3.2s ease-in-out 0.8s infinite;
    }}
    .mascot-img {{
        width: 92px;
        filter: drop-shadow(0 8px 12px rgba(0,0,0,0.4));
        animation: floatSoft 3.2s ease-in-out infinite;
    }}
    @keyframes floatSoft {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    @keyframes bubblePop {{
        from {{ opacity: 0; transform: scale(0.8) translateY(6px); }}
        to {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Navbar with logo 
if logo_data_url:
    navbar_html = (
        '<div class="app-navbar">'
        f'<img src="{logo_data_url}" />'
        '<span class="app-navbar-name">Ella Go</span>'
        '</div>'
    )
    st.markdown(navbar_html, unsafe_allow_html=True)

#ella image
hero_html = (
    '<div class="hero-banner">'
    '<div class="hero-title">Ella Tourism Assistant</div>'
    '<div class="hero-subtitle">An AI guide to attractions, accommodation, '
    'transport, and culture in Ella, Sri Lanka</div>'
    '</div>'
)
st.markdown(hero_html, unsafe_allow_html=True)

#Sidebar
with st.sidebar:
    st.header("About")
    st.markdown(
        """
This assistant answers questions about visiting **Ella, Sri Lanka**
using a small multi-agent system:

- **Agent 1 — Router** (`Llama 3.1 8B` via Groq)
  Classifies your question and refines it for search.
  *Patterns: Routing, Planning*

- **Agent 2 — Answer Generator** (`GPT-4o-mini` via OpenRouter)
  Retrieves relevant knowledge-base chunks, drafts an answer,
  then critiques and revises it.
  *Patterns: Tool Use, Reflection*

Knowledge base: 22 curated documents covering attractions, hotels,
transport, and culture in the Ella region.
        """
    )
    st.divider()
    show_debug = st.checkbox("Show agent internals (debug view)", value=False)


# Cached agent instances 
@st.cache_resource
def load_agents():
    router = RouterAgent()
    answerer = AnswerAgent()
    return router, answerer


missing_keys = []
if not os.environ.get("GROQ_API_KEY"):
    missing_keys.append("GROQ_API_KEY")
if not os.environ.get("OPENROUTER_API_KEY"):
    missing_keys.append("OPENROUTER_API_KEY")

if missing_keys:
    st.error(
        f"Missing required API key(s): {', '.join(missing_keys)}. "
        f"Add them to your .env file locally, or to Streamlit Cloud's "
        f"'Secrets' settings when deployed."
    )
    st.stop()

router_agent, answer_agent = load_agents()

if mascot_data_url:
    mascot_html = (
        '<div class="mascot-wrap">'
        "<div class=\"mascot-bubble\">Hi, I'm Elly! Ask me anything about Ella.</div>"
        f'<img class="mascot-img" src="{mascot_data_url}" />'
        '</div>'
    )
    st.markdown(mascot_html, unsafe_allow_html=True)

st.markdown('<div class="section-label">Explore by category</div>', unsafe_allow_html=True)
cat_cols = st.columns(4)
for col, cat in zip(cat_cols, CATEGORY_CARDS):
    with col:
        cat_html = (
            f'<div class="cat-card" style="--accent: {cat["color"]}">'
            f'<div class="cat-title">{cat["title"]}</div>'
            f'<div class="cat-desc">{cat["desc"]}</div>'
            '</div>'
        )
        st.markdown(cat_html, unsafe_allow_html=True)

#questions
st.markdown('<div class="section-label">Try a question</div>', unsafe_allow_html=True)
example_questions = [
    "What's the best time to visit Nine Arch Bridge?",
    "How do I get from Kandy to Ella?",
    "Where should I stay if I want to hike Little Adam's Peak?",
    "What local food should I try in Ella?",
]

cols = st.columns(2)
for i, ex in enumerate(example_questions):
    if cols[i % 2].button(ex, use_container_width=True):
        st.session_state["question"] = ex

question = st.text_input(
    "Your question",
    value=st.session_state.get("question", ""),
    placeholder="e.g. Is Ella Rock hike difficult?",
)

ask = st.button("Ask", type="primary", use_container_width=True)

if ask and question.strip():
    with st.spinner("Agent 1 is understanding your question..."):
        router_output = router_agent.route(question)

    if show_debug:
        st.markdown("**Agent 1 output (Router):**")
        st.json(router_output)

    with st.spinner("Agent 2 is retrieving info and drafting an answer..."):
        result = answer_agent.answer(router_output)

    if mascot_data_url:
        answer_header_html = (
            '<div class="answer-header">'
            f'<img src="{mascot_data_url}" />'
            '<div class="section-label">Answer</div>'
            '</div>'
        )
        st.markdown(answer_header_html, unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-label">Answer</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)

    # Related images 
    seen_files = []
    gallery_items = []
    for src in result["sources"]:
        fname = src["source"]
        if fname in seen_files:
            continue
        seen_files.append(fname)

        info = get_image_info(fname)
        if not info:
            continue

        img = fetch_image_url(info["query"])
        if not img:
            continue

        gallery_items.append(
            {
                "title": fname.replace(".txt", "").replace("_", " ").title(),
                "price": info.get("price"),
                "img": img,
            }
        )

    if gallery_items:
        st.markdown('<div class="section-label">Related images</div>', unsafe_allow_html=True)
        img_cols = st.columns(min(len(gallery_items), 3))
        for i, item in enumerate(gallery_items):
            with img_cols[i % len(img_cols)]:
                price_html = (
                    f'<div class="img-card-price">{item["price"]}</div>'
                    if item.get("price")
                    else ""
                )
                card_html = (
                    '<div class="img-card">'
                    f'<img src="{item["img"]["url"]}" />'
                    '<div class="img-card-body">'
                    f'<div class="img-card-title">{item["title"]}</div>'
                    f'{price_html}'
                    '<div class="img-card-credit">'
                    f'Photo by {item["img"]["photographer"]} · '
                    f'<a href="{item["img"]["pexels_url"]}" target="_blank">Pexels</a>'
                    '</div>'
                    '</div>'
                    '</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)
    elif not os.environ.get("PEXELS_API_KEY"):
        st.caption(
            "Tip: add a free PEXELS_API_KEY to your .env file to show relevant "
            "photos alongside answers."
        )

    if show_debug and "draft_answer" in result:
        with st.expander("Reflection: draft vs. final answer"):
            st.markdown("**Draft (before reflection):**")
            st.write(result["draft_answer"])
            st.markdown("**Final (after reflection/self-critique):**")
            st.write(result["answer"])

    if result["sources"]:
        with st.expander(f"Retrieved sources ({len(result['sources'])})"):
            for src in result["sources"]:
                st.markdown(f"**{src['source']}** · category: `{src['category']}`")
                st.caption(src["text"])
                st.divider()

elif ask:
    st.warning("Please enter a question first.")
