# -------------------------------
# Imports
# -------------------------------
import streamlit as st
from dotenv import load_dotenv
import os
import re
from groq import Groq

# -------------------------------
# UI CONFIG
# -------------------------------
st.set_page_config(page_title="TalentScout", page_icon="🤖")
st.title("🤖 TalentScout Hiring Assistant")
st.caption("AI-powered candidate screening system")

# -------------------------------
# Language
# -------------------------------
language = st.selectbox("Select Language", ["English", "Hindi"])

# -------------------------------
# Load API
# -------------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# -------------------------------
# VALIDATION
# -------------------------------
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10

def is_valid_experience(exp):
    return exp.isdigit()

# -------------------------------
# SENTIMENT
# -------------------------------
def analyze_sentiment(text):
    text = text.lower()
    if any(w in text for w in ["good", "great", "confident"]):
        return "Positive"
    elif any(w in text for w in ["nervous", "not sure"]):
        return "Negative"
    return "Neutral"

# -------------------------------
# 🔥 SMART FALLBACK (UPGRADED)
# -------------------------------
def fallback_questions(tech_stack):
    techs = [t.strip().lower() for t in tech_stack.split(",")]
    questions = []

    for t in techs:

        if "python" in t:
            questions.append("Explain the difference between list and tuple in Python.")
        elif "django" in t:
            questions.append("Explain Django MVT architecture and request flow.")
        elif "postgresql" in t:
            questions.append("What is indexing in PostgreSQL and how does it improve performance?")
        elif "docker" in t:
            questions.append("What is Docker and how is it used in deployment?")
        elif "react" in t:
            questions.append("What is the virtual DOM in React and how does it improve performance?")
        elif "node" in t:
            questions.append("Explain the event loop in Node.js and how it handles asynchronous operations.")
        elif "mongodb" in t:
            questions.append("What is the difference between SQL and MongoDB, and when would you use MongoDB?")
        else:
            # 🔥 GENERIC BUT SMART
            questions.append(f"Explain the architecture and real-world use cases of {t}.")

    return "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])

# -------------------------------
# LLM FUNCTION
# -------------------------------
def generate_questions(tech_stack, exp):
    if not client:
        raise Exception("No API")

    prompt = f"""
    You are an expert technical interviewer.

    Tech stack: {tech_stack}
    Experience: {exp} years

    Generate ONE strong interview question per technology.
    Make questions practical and NOT generic.
    Do NOT combine technologies.
    """

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# -------------------------------
# CACHE
# -------------------------------
@st.cache_data
def get_questions(tech_stack, exp):
    try:
        return generate_questions(tech_stack, exp)
    except:
        return fallback_questions(tech_stack)

# -------------------------------
# SESSION STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stage" not in st.session_state:
    st.session_state.stage = "name"

if "data" not in st.session_state:
    st.session_state.data = {}

# -------------------------------
# SHOW CHAT
# -------------------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------------
# GREETING
# -------------------------------
if len(st.session_state.messages) == 0:
    greeting = "Hello! What is your full name?"
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.chat_message("assistant").write(greeting)

# -------------------------------
# INPUT
# -------------------------------
user_input = st.chat_input("Type your response...")

if user_input:

    st.caption(f"🧠 Sentiment: {analyze_sentiment(user_input)}")

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = ""
    stage = st.session_state.stage

    if user_input.lower() in ["exit", "quit", "bye"]:
        response = "Thank you! Goodbye!"
        st.session_state.stage = "end"

    elif stage == "name":
        st.session_state.data["name"] = user_input
        response = "Enter email:"
        st.session_state.stage = "email"

    elif stage == "email":
        if not is_valid_email(user_input):
            response = "Invalid email. Try again."
        else:
            st.session_state.data["email"] = user_input
            response = "Enter phone number:"
            st.session_state.stage = "phone"

    elif stage == "phone":
        if not is_valid_phone(user_input):
            response = "Invalid phone number."
        else:
            st.session_state.data["phone"] = user_input
            response = "Years of experience?"
            st.session_state.stage = "exp"

    elif stage == "exp":
        if not is_valid_experience(user_input):
            response = "Enter valid number."
        else:
            st.session_state.data["exp"] = user_input
            response = "Desired role?"
            st.session_state.stage = "role"

    elif stage == "role":
        st.session_state.data["role"] = user_input
        response = "Current location?"
        st.session_state.stage = "location"

    elif stage == "location":
        st.session_state.data["location"] = user_input
        response = "Enter tech stack:"
        st.session_state.stage = "tech"

    elif stage == "tech":
        tech = user_input
        exp = st.session_state.data["exp"]

        questions = get_questions(tech, exp)

        response = f"Here are your technical questions:\n\n{questions}"
        st.session_state.stage = "end"

    elif stage == "end":
        response = "Conversation completed."

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)