
import json
import time
from datetime import datetime
from urllib.parse import urlparse

import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_API_URL = (
    "INVOKE_URL"
)

APP_TITLE = "Tech Cloud Byte"
APP_TAGLINE = (
    "Your organization's internal learning companion "
    "for building AI skills across every team."
)

PURPLE = "#a435f0"
INK = "#1c1d1f"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
}}

.stApp {{
    background: #ffffff;
    color: {INK};
}}

#MainMenu, footer {{
    visibility: hidden;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

.block-container {{
    padding-top: 1.2rem !important;
    max-width: 900px;
}}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {{
    display: none !important;
}}

.topnav {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: .85rem 1.2rem;
    border-radius: 12px;
    background: #1c1d1f;
    color: white;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}}

.brand {{
    font-weight: 800;
    font-size: 1.1rem;
}}

.nav-links {{
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    font-size: .82rem;
    color: #d1d7dc;
}}

.pill {{
    font-size: .75rem;
    padding: .3rem .7rem;
    border-radius: 999px;
    background: rgba(255,255,255,.12);
    white-space: nowrap;
}}

.hero {{
    background: linear-gradient(120deg, #2d2f31, #1c1d1f);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.3rem;
    border: 1px solid #e4e8eb;
}}

.eyebrow {{
    color: #d9a5ff;
    font-weight: 800;
    font-size: .75rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.hero h1 {{
    color: white;
    font-size: 2.1rem;
    font-weight: 800;
    margin: .5rem 0;
}}

.hero p {{
    color: #d1d7dc;
    line-height: 1.6;
}}

.stars {{
    color: #e59819;
    font-size: .85rem;
    margin-top: .8rem;
}}

.section-heading {{
    font-size: 1.3rem;
    font-weight: 800;
    margin: .5rem 0 1rem;
}}

.features {{
    display: flex;
    gap: .8rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}}

.feature {{
    flex: 1;
    min-width: 170px;
    padding: 1rem;
    background: white;
    border: 1px solid #e4e8eb;
    border-radius: 12px;
}}

.feature-title {{
    font-weight: 700;
    margin-top: .4rem;
}}

.feature-description {{
    color: #6a6f73;
    font-size: .82rem;
    line-height: 1.5;
    margin-top: .3rem;
}}

[data-testid="stChatMessage"] {{
    background: white;
    border: 1px solid #e4e8eb;
    border-radius: 12px;
    padding: .85rem 1rem;
    margin-bottom: .8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,.04);
}}

[data-testid="stChatInput"] {{
    border-radius: 10px;
    border: 1px solid #b2b6bd;
    background: white;
}}

div[data-testid="stButton"] > button {{
    background: {PURPLE};
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 700;
}}

div[data-testid="stButton"] > button:hover {{
    background: #8710d8;
    color: white;
}}

.source-card {{
    padding: .9rem;
    border: 1px solid #e4e8eb;
    border-radius: 10px;
    margin: .7rem 0;
}}

.muted {{
    color: #6a6f73;
    font-size: .83rem;
}}

.status-ok {{
    color: #0f7a48;
    font-weight: 700;
}}

.status-bad {{
    color: #b42318;
    font-weight: 700;
}}

@media (max-width: 600px) {{
    .hero {{
        padding: 1.3rem;
    }}
    .hero h1 {{
        font-size: 1.7rem;
    }}
}}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_state():
    defaults = {
        "api_url": DEFAULT_API_URL,
        "timeout": 60,
        "http_method": "POST",
        "messages": [],
        "connection_status": "Not tested",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_state()


# ============================================================
# API RESPONSE PARSING
# ============================================================

def parse_api_response(response):
    """Parse normal JSON and API Gateway proxy-style responses."""

    data = response.json()

    # API Gateway can return a Lambda proxy envelope.
    if isinstance(data, dict) and "body" in data:
        body = data["body"]

        if isinstance(body, str):
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                raise ValueError(
                    "The API returned a body that is not valid JSON."
                )
        elif isinstance(body, dict):
            data = body

    if not isinstance(data, dict):
        raise ValueError("The API response is not a JSON object.")

    status_code = data.get("statusCode")

    if isinstance(status_code, int) and status_code >= 400:
        raise RuntimeError(
            data.get("error", "The backend returned an error.")
        )

    if data.get("error"):
        raise RuntimeError(str(data["error"]))

    return data


# ============================================================
# SOURCE HELPERS
# ============================================================

def safe_http_url(value):
    """Return a valid HTTP(S) URL, otherwise an empty string."""

    if not isinstance(value, str):
        return ""

    value = value.strip()

    try:
        parsed = urlparse(value)
    except ValueError:
        return ""

    if parsed.scheme in ("http", "https") and parsed.netloc:
        return value

    return ""


def format_retrieval_response(data):
    """Format the current retrieval-only Lambda response."""

    results = data.get("results") or []

    if not results:
        return (
            "I couldn't find sufficiently relevant passages in the "
            "knowledge base. Try rephrasing your question.",
            [],
        )

    answer_parts = [
        "### Retrieved information",
        (
            "The following excerpts were retrieved from your indexed "
            "documents. They are source passages, not an AI-generated "
            "answer."
        ),
        "",
    ]

    citations = []

    for index, item in enumerate(results, start=1):
        if not isinstance(item, dict):
            continue

        title = str(item.get("document") or "Unknown document")
        snippet = str(item.get("text") or "").strip()
        page = item.get("page")
        score = item.get("score")
        source = safe_http_url(item.get("source", ""))

        if isinstance(page, (int, float)):
            page_label = str(int(page))
        else:
            page_label = "Not provided"

        if isinstance(score, (int, float)):
            score_label = f"{score:.3f}"
        else:
            score_label = "Not provided"

        answer_parts.extend([
            f"#### {index}. {title}",
            (
                f"**Page:** {page_label} · "
                f"**Retrieval score:** {score_label}"
            ),
            snippet or "_No text was provided for this result._",
            "",
        ])

        citations.append({
            "title": title,
            "page": page_label,
            "source": source,
            "score": score_label,
            "snippet": snippet[:300],
        })

    answer = "\n\n".join(answer_parts)

    return answer, citations


# ============================================================
# CALL API GATEWAY
# ============================================================

def call_backend(prompt):
    """Send a question and format the Lambda retrieval results."""

    api_url = st.session_state.api_url.strip()
    timeout = int(st.session_state.timeout)
    method = st.session_state.http_method

    if not api_url:
        raise ValueError("Enter your API Gateway endpoint in Settings.")

    if method == "GET":
        response = requests.get(
            api_url,
            params={"prompt": prompt},
            timeout=timeout,
        )
    else:
        response = requests.post(
            api_url,
            json={"prompt": prompt},
            timeout=timeout,
        )

    response.raise_for_status()
    data = parse_api_response(response)

    # If a generated answer is added to Lambda in the future,
    # display it directly. The current Lambda uses retrieval-only mode.
    generated_answer = data.get("answer") or data.get("message")

    if generated_answer:
        citations = data.get("citations") or []
        return str(generated_answer), citations

    return format_retrieval_response(data)


# ============================================================
# CONNECTION TEST
# ============================================================

def check_connection():
    """Check whether the configured API endpoint responds."""

    try:
        call_backend("What is Amazon Bedrock?")
        st.session_state.connection_status = "Connected"
    except Exception as exc:
        st.session_state.connection_status = "Connection failed"
        st.session_state.connection_error = str(exc)


# ============================================================
# CITATION DISPLAY
# ============================================================

def render_message(content, citations, timestamp):
    """Render the formatted response and its source references."""

    st.markdown(content)

    if citations:
        with st.expander(f"📎 Sources ({len(citations)})"):
            for index, citation in enumerate(citations, start=1):
                title = citation.get("title") or "Source"
                page = citation.get("page")
                source = safe_http_url(citation.get("source", ""))
                snippet = citation.get("snippet") or ""
                score = citation.get("score")

                heading = f"**{index}. {title}**"

                if page and page != "Not provided":
                    heading += f" · Page {page}"

                st.markdown(heading)

                if score:
                    st.caption(f"Retrieval score: {score}")

                if source:
                    st.markdown(f"[Open source document]({source})")
                else:
                    st.caption(
                        "No browser-accessible source URL was returned."
                    )

                if snippet:
                    st.caption(snippet)

                if index < len(citations):
                    st.divider()

    if timestamp:
        st.caption(timestamp)


# ============================================================
# TOP NAVIGATION
# ============================================================

# st.markdown(
#     """
#     <div class="topnav">
#         <div class="brand">🎓 Tech Cloud Byte</div>
#         <div class="nav-links">
#             <span>Learning Paths</span>
#             <span>My Progress</span>
#             <span>Company Knowledge Base</span>
#         </div>
#         <div class="pill">🟢 Assistant Ready</div>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">Employee AI Enablement Program</div>
        <h1>{APP_TITLE}</h1>
        <p>{APP_TAGLINE}</p>
        <div class="stars">
            ★★★★★
            <span style="color:#d1d7dc">
                Knowledge-base retrieval assistant
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FEATURES
# ============================================================

# st.markdown(
#     """
#     <div class="features">
#         <div class="feature">
#             <div>💬</div>
#             <div class="feature-title">Ask your L&D tutor</div>
#             <div class="feature-description">
#                 Ask questions about your indexed AI learning materials.
#             </div>
#         </div>
#         <div class="feature">
#             <div>📚</div>
#             <div class="feature-title">Grounded in documents</div>
#             <div class="feature-description">
#                 Inspect relevant passages retrieved from your knowledge base.
#             </div>
#         </div>
#         <div class="feature">
#             <div>📈</div>
#             <div class="feature-title">Upskill on the job</div>
#             <div class="feature-description">
#                 Explore your organization's AI learning resources.
#             </div>
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


# ============================================================
# CHAT HEADER AND SETTINGS
# ============================================================

head_left, head_settings, head_clear = st.columns([5, 1.5, 1])

with head_left:
    st.markdown(
        '<div class="section-heading">💬 Your Learning Session</div>',
        unsafe_allow_html=True,
    )

with head_settings:
    with st.popover("⚙️ Settings", use_container_width=True):
        st.text_input(
            "API Gateway endpoint",
            key="api_url",
            help="Your deployed API Gateway URL.",
        )

        st.selectbox(
            "HTTP method",
            options=["POST", "GET"],
            key="http_method",
        )

        st.number_input(
            "Timeout (seconds)",
            min_value=5,
            max_value=300,
            step=5,
            key="timeout",
        )

        if st.button("Test connection", use_container_width=True):
            with st.spinner("Testing API connection..."):
                check_connection()

        status = st.session_state.connection_status

        if status == "Connected":
            st.markdown(
                '<p class="status-ok">🟢 API reachable</p>',
                unsafe_allow_html=True,
            )
        elif status == "Connection failed":
            st.markdown(
                '<p class="status-bad">🔴 Connection failed</p>',
                unsafe_allow_html=True,
            )
            st.caption(
                st.session_state.get("connection_error", "")
            )
        else:
            st.caption("Connection has not been tested.")

with head_clear:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

if not st.session_state.messages:
    st.info(
        "👋 Welcome to Tech Cloud Byte! Ask a question below "
        "to explore your organization's indexed learning materials."
    )

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(message["content"])
            if message.get("timestamp"):
                st.caption(message["timestamp"])
    else:
        with st.chat_message("assistant", avatar="👩‍🏫"):
            render_message(
                message["content"],
                message.get("citations", []),
                message.get("timestamp"),
            )


# ============================================================
# HANDLE NEW QUESTIONS
# ============================================================

prompt = st.chat_input(
    "Ask about AI concepts, tools, or your learning materials..."
)

if prompt:
    timestamp = datetime.now().strftime("%H:%M")

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp,
    })

    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)
        st.caption(timestamp)

    with st.chat_message("assistant", avatar="👩‍🏫"):
        placeholder = st.empty()
        placeholder.markdown("🤔 *Searching your knowledge base...*")

        try:
            answer, citations = call_backend(prompt)
            st.session_state.connection_status = "Connected"

        except requests.exceptions.Timeout:
            answer = (
                "⏱️ The request timed out. Try increasing the timeout "
                "in Settings and ask again."
            )
            citations = []
            st.session_state.connection_status = "Connection failed"

        except requests.exceptions.HTTPError as exc:
            status_code = (
                exc.response.status_code if exc.response is not None else "?"
            )
            answer = (
                f"⚠️ The API returned HTTP {status_code}. "
                "Check your API Gateway route, deployment stage, "
                "and Lambda logs."
            )
            citations = []
            st.session_state.connection_status = "Connection failed"

        except requests.exceptions.RequestException as exc:
            answer = (
                "⚠️ Could not reach API Gateway. Check your endpoint, "
                "network connection, and API configuration.\n\n"
                f"Details: `{exc}`"
            )
            citations = []
            st.session_state.connection_status = "Connection failed"

        except (ValueError, RuntimeError) as exc:
            answer = f"⚠️ {exc}"
            citations = []

        except Exception as exc:
            answer = (
                "⚠️ Something went wrong while processing the response. "
                f"Details: `{exc}`"
            )
            citations = []

        # Small visual typing effect.
        placeholder.empty()
        with st.spinner("Preparing retrieved passages..."):
            time.sleep(0.15)

        render_message(
            answer,
            citations,
            datetime.now().strftime("%H:%M"),
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "citations": citations,
        "timestamp": datetime.now().strftime("%H:%M"),
    })

    st.rerun()
