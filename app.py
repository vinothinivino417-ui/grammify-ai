import streamlit as st
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import re
import html

from agents.crew import create_grammar_crew


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Grammify AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
BABY_IMAGE = BASE_DIR / "assets" / "grammify_baby_mascot.png"


# ============================================================
# CUSTOM CSS
# ============================================================

st.html("""
<style>

.stApp {
    min-height: 100vh;
    background:
        radial-gradient(
            circle at 5% 5%,
            rgba(116,190,255,.30),
            transparent 28%
        ),
        radial-gradient(
            circle at 95% 8%,
            rgba(173,125,255,.28),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 95%,
            rgba(229,164,255,.24),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #eef8ff 0%,
            #f5efff 48%,
            #eef5ff 100%
        );
    color: #30285f;
}


/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* Main container */

.block-container {
    max-width: 1180px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #e7f5ff 0%,
            #eeeaff 48%,
            #f8edff 100%
        );
    border-right: 2px solid rgba(126,107,210,.16);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #5140ad;
}


/* Baby */

div[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    margin-bottom: 8px;
}

div[data-testid="stImage"] img {
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(80,70,160,.15);
}

/* Hero */

.hero-box {
    position: relative;
    background:
        linear-gradient(
            135deg,
            rgba(177,221,255,.94),
            rgba(208,194,255,.96),
            rgba(239,211,255,.94)
        );
    border-radius: 30px;
    padding: 30px;
    margin-bottom: 25px;
    border: 2px solid rgba(255,255,255,.85);
    box-shadow:
        0 18px 45px rgba(87,71,163,.13);
    overflow: hidden;
}

.hero-box:before {
    content: "";
    position: absolute;
    width: 160px;
    height: 160px;
    background: rgba(255,255,255,.20);
    border-radius: 50%;
    top: -80px;
    left: -60px;
}

.hero-box:after {
    content: "";
    position: absolute;
    width: 190px;
    height: 190px;
    background: rgba(255,255,255,.17);
    border-radius: 50%;
    bottom: -110px;
    right: -50px;
}

.hero-title {
    position: relative;
    text-align: center;
    font-size: 56px;
    font-weight: 900;
    letter-spacing: -2px;
    color: #5745c7;
}

.hero-subtitle {
    position: relative;
    text-align: center;
    font-size: 19px;
    font-weight: 650;
    color: #4c557a;
    margin-top: 6px;
}

.rainbow-line {
    position: relative;
    width: 190px;
    height: 7px;
    margin: 15px auto 0 auto;
    border-radius: 50px;
    background:
        linear-gradient(
            90deg,
            #55a8ef,
            #667fe9,
            #745ad5,
            #995bd3
        );
}


/* Input */

.input-box {
    background: rgba(255,255,255,.88);
    border-radius: 25px;
    padding: 22px 25px 10px 25px;
    border: 2px solid rgba(191,181,231,.45);
    box-shadow:
        0 12px 35px rgba(77,65,145,.09);
    margin-bottom: 5px;
}

.input-title {
    font-size: 23px;
    font-weight: 850;
    color: #5141ad;
}

.section-line {
    width: 90px;
    height: 4px;
    border-radius: 50px;
    margin-top: 8px;
    background:
        linear-gradient(
            90deg,
            #55a4ee,
            #745bd6
        );
}


/* Text area */

div[data-testid="stTextArea"] textarea {
    border-radius: 19px !important;
    border: 3px solid #d7d7f5 !important;
    background: rgba(255,255,255,.97) !important;
    color: #30295f !important;
    font-size: 18px !important;
    line-height: 1.55 !important;
    padding: 18px !important;
    box-shadow:
        0 5px 16px rgba(70,65,140,.06);
}

div[data-testid="stTextArea"] textarea:focus {
    border: 3px solid #7664dc !important;
    box-shadow:
        0 0 0 4px rgba(118,100,220,.13) !important;
}


/* Button */

.stButton > button {
    width: 100%;
    min-height: 56px;
    border: none;
    border-radius: 18px;
    background:
        linear-gradient(
            135deg,
            #4d93e9,
            #625bd8,
            #8b59d2
        );
    color: white;
    font-size: 19px;
    font-weight: 850;
    box-shadow:
        0 9px 22px rgba(87,72,190,.24);
    transition: all .2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 13px 28px rgba(87,72,190,.32);
}


/* Result heading */

.result-heading {
    text-align: center;
    margin-top: 28px;
    margin-bottom: 20px;
}

.result-heading-title {
    font-size: 29px;
    font-weight: 900;
    color: #5141ad;
}

.result-heading-line {
    width: 120px;
    height: 5px;
    border-radius: 50px;
    margin: 9px auto;
    background:
        linear-gradient(
            90deg,
            #55a5ee,
            #735bd7,
            #9b61d5
        );
}


/* Corrected sentence */

.corrected-card {
    background:
        linear-gradient(
            135deg,
            #eaf8ff,
            #f0edff,
            #faf0ff
        );
    border: 2px solid #cbd8f5;
    border-radius: 23px;
    padding: 24px;
    margin-top: 8px;
    box-shadow:
        0 12px 30px rgba(72,70,150,.09);
}

.corrected-label {
    color: #4d7bc8;
    font-size: 18px;
    font-weight: 850;
    margin-bottom: 8px;
}

.corrected-text {
    color: #5141a7;
    font-size: 24px;
    font-weight: 800;
    line-height: 1.5;
}


/* Result cards */

.result-card {
    background: rgba(255,255,255,.90);
    border-radius: 22px;
    padding: 21px;
    border: 1px solid rgba(185,176,224,.40);
    box-shadow:
        0 10px 30px rgba(74,65,145,.08);
    margin-bottom: 15px;
}

.result-card-purple {
    border-left: 7px solid #745dd7;
}

.result-card-blue {
    border-left: 7px solid #5599eb;
}

.result-card-violet {
    border-left: 7px solid #9b63d5;
}

.result-title {
    font-size: 20px;
    font-weight: 850;
    color: #5142ad;
    margin-bottom: 10px;
}

.result-text {
    font-size: 17px;
    line-height: 1.65;
    color: #39345d;
}


/* Mistakes */

.mistake-item {
    background:
        linear-gradient(
            90deg,
            #f7f3ff,
            #fbf9ff
        );
    border-left: 4px solid #8d72d8;
    border-radius: 12px;
    padding: 12px 15px;
    margin: 8px 0;
    color: #3d3655;
    line-height: 1.5;
}


/* Rule */

.rule-box {
    background:
        linear-gradient(
            135deg,
            #eef7ff,
            #f1ecff
        );
    border: 1px solid #d6d2f1;
    border-radius: 17px;
    padding: 18px;
    color: #453a70;
    line-height: 1.65;
}


/* Sidebar */

div[data-testid="stSlider"] label {
    color: #5142ad !important;
    font-weight: 800 !important;
}


/* Footer */

.footer-text {
    text-align: center;
    margin-top: 40px;
    color: #77719a;
    font-size: 14px;
}


/* Mobile */

@media (max-width: 768px) {

    .hero-title {
        font-size: 40px;
    }

    .hero-subtitle {
        font-size: 16px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .baby-wrapper img {
        width: 180px;
    }

    .corrected-text {
        font-size: 20px;
    }
}

</style>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Settings")

    st.html("""
    <div style="
        background:rgba(255,255,255,.75);
        padding:16px;
        border-radius:17px;
        margin-bottom:18px;
        border:1px solid rgba(190,180,230,.35);
    ">

        <div style="
            color:#5141AD;
            font-size:18px;
            font-weight:850;
        ">
            🤖 Grammify AI
        </div>

        <div style="
            color:#66617F;
            margin-top:7px;
            line-height:1.5;
        ">
            Tune the AI before checking
            your English sentence.
        </div>

    </div>
    """)

    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1,
        help="Lower values give more consistent grammar corrections.",
    )

    max_tokens = st.slider(
        "🔢 Max Tokens",
        min_value=300,
        max_value=3000,
        value=1200,
        step=100,
    )

    st.markdown("---")

    st.markdown("### 🧠 AI Team")

    st.html("""
    <div style="
        line-height:2;
        color:#514A72;
    ">

        <b style="color:#438CE7;">
            🔵 Planner Agent
        </b>
        <br>
        Plans the grammar analysis.

        <br>

        <b style="color:#735BD4;">
            🟣 Researcher Agent
        </b>
        <br>
        Investigates grammar rules.

        <br>

        <b style="color:#55A878;">
            🟢 Correction Agent
        </b>
        <br>
        Creates the corrected sentence.

        <br>

        <b style="color:#D16BA5;">
            🩷 Reflection
        </b>
        <br>
        Checks the final answer.

    </div>
    """)

    st.markdown("---")

    st.caption("Powered by CrewAI + Hugging Face")


# ============================================================
# BABY IMAGE - TOP CENTER
# ============================================================

baby_left, baby_center, baby_right = st.columns(
    [1, 2, 1],
    gap="small"
)

with baby_center:

    if BABY_IMAGE.exists():

        st.image(
            str(BABY_IMAGE),
            width=220
        )

    else:

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:90px;
                margin-bottom:10px;
            ">
                👶📚🧠
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero-box">

    <div class="hero-title">
        Grammify AI ✨
    </div>

    <div class="hero-subtitle">
        Write it wrong. Grammify it right. 📚
    </div>

    <div class="rainbow-line"></div>

</div>
""")


# ============================================================
# INPUT
# ============================================================

st.html("""
<div class="input-box">

    <div class="input-title">
        ✏️ Enter your English sentence
    </div>

    <div class="section-line"></div>

</div>
""")


sentence = st.text_area(
    "English sentence",
    placeholder="Example: She go to school every day.",
    height=150,
    label_visibility="collapsed",
)


st.markdown(
    "<div style='height:8px'></div>",
    unsafe_allow_html=True,
)


grammify = st.button(
    "✨ Grammify It!",
    use_container_width=True,
)


# ============================================================
# OUTPUT PARSER
# ============================================================

def extract_section(text, section_name, next_sections):

    if next_sections:

        next_pattern = "|".join(
            re.escape(section)
            for section in next_sections
        )

        pattern = (
            rf"{re.escape(section_name)}:\s*"
            rf"(.*?)(?=\n\s*(?:{next_pattern}):|\Z)"
        )

    else:

        pattern = (
            rf"{re.escape(section_name)}:\s*"
            rf"(.*?)(?=\Z)"
        )

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(1).strip()

    return ""


# ============================================================
# PROCESS
# ============================================================

if grammify:

    if not sentence.strip():

        st.warning(
            "✏️ Please enter an English sentence first."
        )

        st.stop()


    with st.spinner(
        "🧠 Your grammar genius is thinking..."
    ):

        try:

            crew = create_grammar_crew(
                temperature=temperature,
                max_tokens=max_tokens,
            )

            stdout_buffer = StringIO()
            stderr_buffer = StringIO()

            with redirect_stdout(stdout_buffer), \
                 redirect_stderr(stderr_buffer):

                result = crew.kickoff(
                    inputs={
                        "sentence": sentence.strip()
                    }
                )

            output = str(result)

        except Exception as e:

            st.error(
                "Something went wrong while checking the sentence."
            )

            with st.expander("Technical details"):

                st.code(str(e))

            st.stop()


    # ========================================================
    # PARSE
    # ========================================================

    original = extract_section(
        output,
        "ORIGINAL",
        [
            "MISTAKES",
            "CORRECTED",
            "NATURAL VERSION",
            "RULE",
        ],
    )

    mistakes = extract_section(
        output,
        "MISTAKES",
        [
            "CORRECTED",
            "NATURAL VERSION",
            "RULE",
        ],
    )

    corrected = extract_section(
        output,
        "CORRECTED",
        [
            "NATURAL VERSION",
            "RULE",
        ],
    )

    natural = extract_section(
        output,
        "NATURAL VERSION",
        [
            "RULE",
        ],
    )

    rule = extract_section(
        output,
        "RULE",
        [],
    )


    # ========================================================
    # FALLBACK
    # ========================================================

    if not original:
        original = sentence.strip()

    if not corrected:
        corrected = output

    if not natural:
        natural = corrected


    # ========================================================
    # ESCAPE CONTENT
    # ========================================================

    original_html = html.escape(original)
    corrected_html = html.escape(corrected)
    natural_html = html.escape(natural)
    rule_html = html.escape(rule)


    # ========================================================
    # RESULT HEADER
    # ========================================================

    st.html("""
    <div class="result-heading">

        <div class="result-heading-title">
            📖 Grammar Analysis
        </div>

        <div class="result-heading-line"></div>

    </div>
    """)


    # ========================================================
    # CORRECTED SENTENCE
    # ========================================================

    st.html(f"""
    <div class="corrected-card">

        <div class="corrected-label">
            ✅ Corrected Sentence
        </div>

        <div class="corrected-text">
            {corrected_html}
        </div>

    </div>
    """)


    # ========================================================
    # DETAILS
    # ========================================================

    col1, col2 = st.columns(2, gap="medium")


    # ========================================================
    # DETECTED ISSUES
    # ========================================================

    with col1:

        st.html("""
        <div class="result-card result-card-purple">

            <div class="result-title">
                🔍 Detected Issues
            </div>

        </div>
        """)

        if mistakes:

            mistake_lines = mistakes.splitlines()

            for line in mistake_lines:

                line = line.strip()

                if not line:
                    continue

                line = re.sub(
                    r"^\s*[-•*]\s*",
                    "",
                    line,
                )

                safe_line = html.escape(line)

                st.html(f"""
                <div class="mistake-item">
                    • {safe_line}
                </div>
                """)

        else:

            st.success(
                "No major mistakes found! 🎉"
            )


    # ========================================================
    # WHY THIS CHANGE
    # ========================================================

    with col2:

        safe_natural = html.escape(natural)

        st.html(f"""
        <div class="result-card result-card-blue">

            <div class="result-title">
                💡 Why this change?
            </div>

            <div class="result-text">
                {safe_natural}
            </div>

        </div>
        """)


    # ========================================================
    # ORIGINAL + RULE
    # ========================================================

    col3, col4 = st.columns(2, gap="medium")


    # ========================================================
    # ORIGINAL
    # ========================================================

    with col3:

        st.html(f"""
        <div class="result-card result-card-violet">

            <div class="result-title">
                📝 Original Sentence
            </div>

            <div class="result-text">
                {original_html}
            </div>

        </div>
        """)


    # ========================================================
    # RULE
    # ========================================================

    with col4:

        if not rule_html:

            rule_html = (
                "The sentence was reviewed for grammar, "
                "spelling, punctuation, word choice, "
                "sentence structure, and context."
            )

        st.html(f"""
        <div class="result-card result-card-blue">

            <div class="result-title">
                📚 Grammar Rule
            </div>

            <div class="rule-box">
                {rule_html}
            </div>

        </div>
        """)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer-text">

    📚 Grammify AI
    • Your personal English grammar genius ✨

</div>
""")