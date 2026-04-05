# -------------------------------
# Imports & Setup
# -------------------------------
import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq

# -------------------------------
# UI Configuration
# -------------------------------
st.set_page_config(page_title="TalentScout", page_icon="🤖", layout="centered")

st.markdown("""
<style>
body { background-color: #0e1117; }
.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🤖 TalentScout Hiring Assistant")
st.caption("AI-powered candidate screening system")

# -------------------------------
# Language Selection
# -------------------------------
language = st.selectbox("Select Language", ["English", "Hindi"])

# -------------------------------
# Load API Key
# -------------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# -------------------------------
# Session State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stage" not in st.session_state:
    st.session_state.stage = "collect_name"

if "candidate" not in st.session_state:
    st.session_state.candidate = {
        "name": "",
        "email": "",
        "phone": "",
        "experience": "",
        "role": "",
        "location": "",
        "tech_stack": ""
    }

# -------------------------------
# Sentiment Analysis
# -------------------------------
def analyze_sentiment(text):
    text = text.lower()
    if any(w in text for w in ["good", "great", "confident"]):
        return "Positive"
    elif any(w in text for w in ["nervous", "difficult", "not sure"]):
        return "Negative"
    return "Neutral"

# -------------------------------
# LLM Function (FINAL FIX)
# -------------------------------
def generate_questions(tech_stack, experience, language):
    if not client:
        raise Exception("No API key")

    prompt = f"""
    You are an expert technical interviewer.

    Candidate Tech Stack:
    {tech_stack}

    Experience: {experience} years

    Generate EXACTLY 4 technical interview questions.
    Each question must focus on ONE technology only.

    Example:
    - One Python question
    - One Django question
    - One PostgreSQL question

    Do NOT combine technologies.
    Keep them practical and interview-focused.

    Respond in {language}.
    """

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # ✅ WORKING MODEL
        messages=[
            {"role": "system", "content": "You are a strict technical interviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# -------------------------------
# Cached Questions
# -------------------------------
@st.cache_data
def cached_questions(tech_stack, experience, language):
    try:
        return generate_questions(tech_stack, experience, language)
    except Exception:
        return """
1. What is the difference between list and tuple in Python?
2. Explain Django MVT architecture.
3. What is indexing in PostgreSQL?
4. How would you scale a Django application?
"""

# -------------------------------
# Progress Bar
# -------------------------------
progress_map = {
    "collect_name": 10,
    "collect_email": 20,
    "collect_phone": 30,
    "collect_experience": 40,
    "collect_role": 50,
    "collect_location": 60,
    "tech_stack": 80,
    "end": 100
}
st.progress(progress_map.get(st.session_state.stage, 0))

# -------------------------------
# Initial Greeting
# -------------------------------
if len(st.session_state.messages) == 0:
    greeting = "Hello! What is your full name?" if language == "English" else "नमस्ते! आपका नाम क्या है?"
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# -------------------------------
# Display Chat
# -------------------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------------
# End Handling
# -------------------------------
if st.session_state.stage == "end":
    st.chat_input("Conversation completed.", disabled=True)
    st.stop()

# -------------------------------
# Chat Input
# -------------------------------
user_input = st.chat_input("Type your response...")

if user_input:

    sentiment = analyze_sentiment(user_input)
    st.caption(f"🧠 Sentiment: {sentiment}")

    if user_input.lower() in ["exit", "quit", "bye"]:
        st.chat_message("assistant").write("Thank you! Goodbye!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = ""

    # -------------------------------
    # Conversation Flow
    # -------------------------------
    if st.session_state.stage == "collect_name":
        st.session_state.candidate["name"] = user_input
        response = "Enter email:"
        st.session_state.stage = "collect_email"

    elif st.session_state.stage == "collect_email":
        st.session_state.candidate["email"] = user_input
        response = "Enter phone number:"
        st.session_state.stage = "collect_phone"

    elif st.session_state.stage == "collect_phone":
        st.session_state.candidate["phone"] = user_input
        response = "Years of experience?"
        st.session_state.stage = "collect_experience"

    elif st.session_state.stage == "collect_experience":
        st.session_state.candidate["experience"] = user_input
        response = "Desired role?"
        st.session_state.stage = "collect_role"

    elif st.session_state.stage == "collect_role":
        st.session_state.candidate["role"] = user_input
        response = "Current location?"
        st.session_state.stage = "collect_location"

    elif st.session_state.stage == "collect_location":
        st.session_state.candidate["location"] = user_input
        response = "Enter tech stack:"
        st.session_state.stage = "tech_stack"

    # 🔥 FINAL FIX: instant generation
    elif st.session_state.stage == "tech_stack":
        st.session_state.candidate["tech_stack"] = user_input

        tech = user_input
        exp = st.session_state.candidate["experience"]

        questions = cached_questions(tech, exp, language)

        response = f"Here are your technical questions:\n\n{questions}"
        st.session_state.stage = "end"

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)