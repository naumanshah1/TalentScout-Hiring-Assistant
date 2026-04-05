# TalentScout Hiring Assistant Chatbot
## Developed by: Nauman Shah
## Project Overview

The TalentScout Hiring Assistant is an AI-powered chatbot designed to assist in the initial screening of candidates for technical roles. It interacts with users through a conversational interface, collects essential candidate information, and generates technical interview questions based on the candidate’s declared tech stack.

The system demonstrates the use of Large Language Models (LLMs) to automate and streamline early-stage recruitment processes while maintaining a structured and user-friendly interaction flow.

---

## Features

* Interactive chatbot interface using Streamlit
* Collects candidate details:

  * Full Name
  * Email Address
  * Phone Number
  * Years of Experience
  * Desired Position
  * Current Location
  * Tech Stack
* Generates 3–5 technical questions dynamically based on tech stack
* Maintains conversation context using session state
* Handles invalid input with fallback responses
* Supports exit commands (`exit`, `quit`, `bye`)
* Ensures secure handling of candidate data (no permanent storage)

---

## Installation Instructions

1. Clone the repository:

```
git clone https://github.com/naumanshah1/TalentScout.git
cd TalentScout
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file and add your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

4. Run the application:

```
streamlit run app.py
```

---

## Usage Guide

1. Launch the chatbot using Streamlit
2. Enter your details step-by-step as prompted
3. Provide your tech stack (e.g., Python, Django, MySQL)
4. The chatbot will generate technical interview questions
5. Type `exit` to end the conversation at any time

---

## Technical Details

### Programming Language

* Python

### Libraries & Tools

* Streamlit – for building the chatbot interface
* Groq API – for accessing LLaMA3 Large Language Model
* python-dotenv – for managing environment variables

### Model Used

* LLaMA3 (via Groq API)
* Used for generating dynamic, context-aware technical questions

### Architecture

* Frontend: Streamlit chat interface
* Backend: Python logic with stage-based conversation flow
* State Management: Streamlit session state
* LLM Integration: Prompt-based interaction with Groq API

---

## Prompt Design

The chatbot uses structured prompt engineering to guide the LLM effectively.

### Key Strategies:

* **Role Definition:** The model is instructed to act as an expert technical interviewer
* **Clear Instructions:** Specifies number of questions (3–5), difficulty level, and relevance
* **Context Awareness:** Uses candidate-provided tech stack as input
* **Output Formatting:** Enforces structured numbered questions
* **Quality Constraints:** Avoids repetition and ensures clarity

### Example Prompt Structure:

```
You are an expert technical interviewer.

Generate 3–5 technical questions based on:
{tech_stack}

Requirements:
- Moderate difficulty
- Cover core concepts and practical usage
- Clear and concise
```

This ensures consistent and high-quality outputs from the LLM.

---

## Data Handling

### Simulated Data

* Candidate data is stored temporarily using Streamlit session state
* No database or external storage is used

### Data Privacy

The system follows basic data privacy principles:

* No personally identifiable information (PII) is stored permanently
* Data is only available during the active session
* No logging or external sharing of user data
* Ensures data minimization and limited retention

This approach aligns with fundamental GDPR principles.

---

## Challenges & Solutions

### 1. API Quota Limitation

* **Challenge:** OpenAI API required billing
* **Solution:** Switched to Groq (free LLM provider)

### 2. Maintaining Conversation Flow

* **Challenge:** Keeping interaction structured
* **Solution:** Implemented stage-based state management using `session_state`

### 3. Handling Diverse Tech Stacks

* **Challenge:** Supporting multiple technologies
* **Solution:** Used LLM-based dynamic question generation

### 4. Data Privacy Concerns

* **Challenge:** Handling sensitive candidate data securely
* **Solution:** Used temporary session-based storage with no persistence

---

## Conclusion

The TalentScout Hiring Assistant successfully demonstrates how AI-powered chatbots can automate candidate screening by collecting structured data and generating relevant technical questions. The system is scalable, user-friendly, and aligns with modern AI-driven recruitment practices.
