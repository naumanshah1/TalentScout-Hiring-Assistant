import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq

# -------------------------------
# Data Privacy Note
# -------------------------------
# All candidate data is stored temporarily using Streamlit session state.
# No data is persisted or stored in any database.
# This ensures user privacy and secure handling of sensitive information.

# -------------------------------
# Load API Key
# -------------------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🤖 TalentScout Hiring Assistant")

# -------------------------------
# Initialize session states
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stage" not in st.session_state:
    st.session_state.stage = "greeting"

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
# LLM Function (Improved Prompt)
# -------------------------------
def generate_questions(tech_stack):
    prompt = f"""
    You are an expert technical interviewer.

    Your task is to generate 3 to 5 high-quality technical interview questions.

    Requirements:
    - Questions must be based on the candidate's tech stack: {tech_stack}
    - Questions should be moderately difficult
    - Cover core concepts, practical usage, and problem-solving
    - Be clear and concise
    - Avoid repetition

    Output format:
    1. Question
    2. Question
    3. Question
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception:
        return f"""
1. Explain fundamentals of {tech_stack}.
2. What are real-world applications of {tech_stack}?
3. What are advantages and limitations of {tech_stack}?
4. Describe a project you built using {tech_stack}.
"""

# -------------------------------
# Initial Greeting
# -------------------------------
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! 👋 I am TalentScout Hiring Assistant.\n\nI will collect your details and ask a few technical questions.\n\nWhat is your full name?"
    })
    st.session_state.stage = "collect_name"

# -------------------------------
# Display chat history
# -------------------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------------
# Chat input
# -------------------------------
user_input = st.chat_input("Type your response...")

if user_input:

    # Exit condition
    if user_input.lower() in ["exit", "quit", "bye"]:
        response = "Thank you for your time! 🙌 Our team will contact you soon."

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.chat_message("assistant").write(response)
        st.stop()

    # Fallback handling
    if not user_input.strip():
        response = "Sorry, I didn’t understand that. Please provide valid input."

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.chat_message("assistant").write(response)
        st.stop()

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    st.chat_message("user").write(user_input)

    response = ""

    # -------------------------------
    # Conversation Flow
    # -------------------------------
    if st.session_state.stage == "collect_name":
        st.session_state.candidate["name"] = user_input
        response = "Please enter your email address:"
        st.session_state.stage = "collect_email"

    elif st.session_state.stage == "collect_email":
        st.session_state.candidate["email"] = user_input
        response = "Please enter your phone number:"
        st.session_state.stage = "collect_phone"

    elif st.session_state.stage == "collect_phone":
        st.session_state.candidate["phone"] = user_input
        response = "How many years of experience do you have?"
        st.session_state.stage = "collect_experience"

    elif st.session_state.stage == "collect_experience":
        st.session_state.candidate["experience"] = user_input
        response = "What position are you applying for?"
        st.session_state.stage = "collect_role"

    elif st.session_state.stage == "collect_role":
        st.session_state.candidate["role"] = user_input
        response = "What is your current location?"
        st.session_state.stage = "collect_location"

    elif st.session_state.stage == "collect_location":
        st.session_state.candidate["location"] = user_input
        response = "Please list your tech stack (languages, frameworks, tools):"
        st.session_state.stage = "tech_stack"

    elif st.session_state.stage == "tech_stack":
        st.session_state.candidate["tech_stack"] = user_input
        response = "Thanks! Generating technical questions..."
        st.session_state.stage = "generate_questions"

    elif st.session_state.stage == "generate_questions":
        tech_stack = st.session_state.candidate["tech_stack"]
        questions = generate_questions(tech_stack)

        response = f"Here are your technical questions:\n\n{questions}"
        st.session_state.stage = "end"

    elif st.session_state.stage == "end":
        response = (
            "✅ Thank you for completing the initial screening!\n\n"
            "Our recruitment team will review your responses and reach out to you soon.\n\n"
            "Have a great day! 🚀"
        )

    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.chat_message("assistant").write(response)

# -------------------------------
# Disable input after completion
# -------------------------------
if st.session_state.stage == "end":
    st.chat_input("Conversation completed. Type 'exit' to close.", disabled=True)