import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.warning("OpenAI API key not found. Put your API key in .env.")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

st.set_page_config(page_title="Rooman Support Assistant", layout="centered")

# ----------------------------------------
# PREMIUM UI CSS
# ----------------------------------------
st.markdown("""
<style>

/* GLOBAL BACKGROUND */
body {
    background: linear-gradient(135deg, #e3ecff 0%, #f9fbff 100%);
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER */
.header {
    background: linear-gradient(90deg, #003A74, #005BB5);
    padding: 30px;
    color: white;
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    margin-bottom: 25px;
}

/* CHAT CARD */
.chat-box {
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    width: 100%;
    max-width: 820px;
    margin: auto;
    border: 1px solid #e3e3e3;
}

/* USER BUBBLE */
.user-msg {
    background-color: #d9eaff;
    padding: 12px 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    font-weight: 500;
    border-left: 4px solid #005BB5;
}

/* ASSISTANT BUBBLE */
.bot-msg {
    background-color: #e8ffe5;
    padding: 14px 16px;
    border-radius: 12px;
    margin-bottom: 15px;
    border-left: 4px solid #2e7d32;
    font-size: 15px;
}

/* FAQ CARD */
.faq-box {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.12);
    width: 100%;
    max-width: 820px;
    margin: auto;
}

/* Send Button Styling */
.stButton>button {
    background: linear-gradient(90deg, #005BB5, #007FFF);
    color: white;
    border-radius: 10px;
    padding: 10px 22px;
    font-size: 16px;
    font-weight: 600;
    border: none;
    box-shadow: 0 3px 10px rgba(0,0,0,0.2);
}
.stButton>button:hover {
    background: linear-gradient(90deg, #004799, #006ad9);
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}

/* Typing Animation */
.typing {
    width: 55px;
}
.typing span {
    height: 10px;
    width: 10px;
    margin: 0 2px;
    background: #777;
    display: inline-block;
    border-radius: 50%;
    animation: blink 1.3s infinite;
}
@keyframes blink {
    0% {opacity: .2;}
    20% {opacity: 1;}
    100% {opacity: .2;}
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# HEADER
# ----------------------------------------
st.markdown('<div class="header">Rooman Support Assistant</div>', unsafe_allow_html=True)

# ----------------------------------------
# Load FAQs
# ----------------------------------------
def load_faqs(path="faqs.txt"):
    if not os.path.exists(path):
        return []

    raw = open(path, "r", encoding="utf-8").read().strip()
    blocks = [b.strip() for b in raw.split("\n\n") if b.strip()]

    items = []
    for b in blocks:
        lines = b.split("\n")
        q = lines[0].replace("Q:", "").strip()
        k = lines[1].replace("K:", "").strip().lower().split(",")
        a = "\n".join(lines[2:]).replace("A:", "").strip()
        items.append({"q": q, "k": [kw.strip() for kw in k], "a": a})
    return items

FAQ_ITEMS = load_faqs("faqs.txt")

# ----------------------------------------
# Keyword Match
# ----------------------------------------
def keyword_match(user_input, items):
    user_input_lower = user_input.lower()
    results = []
    for item in items:
        score = 0
        for key in item["k"]:
            if key in user_input_lower:
                score += 2
        if score > 0:
            results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)
    return results

def ask_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    return response.choices[0].message.content.strip()

# ----------------------------------------
# Chat Section
# ----------------------------------------
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
st.subheader("How can I help you today?")

if "history" not in st.session_state:
    st.session_state.history = []

user_q = st.text_input("Type your query here...")

support_email = "support@roomantech.com"

if st.button("Send") and user_q:
    matches = keyword_match(user_q, FAQ_ITEMS)

    if matches:
        best = matches[0][1]
        answer = f"""### {best['q']}

{best['a']}

Let me know if you need more help 😊"""
    else:
        prompt = f"""
        User asked: {user_q}.
        No FAQ match found.
        Respond politely and escalate to support: {support_email}
        """
        answer = ask_openai(prompt)

    st.session_state.history.append({"q": user_q, "a": answer})
    st.rerun()

# Show conversation history
for turn in reversed(st.session_state.history):
    st.markdown(f'<div class="user-msg">👤 <b>You:</b> {turn["q"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-msg">🤖 <b>Assistant:</b><br>{turn["a"]}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------
# FAQ SECTION
# ----------------------------------------
st.subheader("Frequently Asked Questions")
st.markdown('<div class="faq-box">', unsafe_allow_html=True)

for item in FAQ_ITEMS:
    st.markdown(f"""
    <b>{item['q']}</b><br>
    {item['a']}<br><br>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
