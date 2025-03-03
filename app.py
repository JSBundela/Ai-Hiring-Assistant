import os
import streamlit as st
import random
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import ollama
import nltk

# Download the VADER lexicon and initialize the sentiment analyzer globally
import nltk
nltk.data.path.append('/path/to/your/nltk_data')

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()  # Global instance for sentiment analysis

# Load environment variables
load_dotenv()

# Initialize session state
if "info" not in st.session_state:
    st.session_state.info = {
        "name": "", "email": "", "phone": "", "location": "",
        "experience": "0", "position": "", "tech_stack": [],
        "tech_questions": {}, "answers": {}
    }
if "step" not in st.session_state:
    st.session_state.step = "greeting"
if "current_tech" not in st.session_state:
    st.session_state.current_tech = None
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "follow_up" not in st.session_state:
    st.session_state.follow_up = None

LANGUAGES = {
    "English": "en", "French": "fr", "Spanish": "es",
    "German": "de", "Hindi": "hi"
}

FALLBACK_RESPONSES = [
    "Let's focus on your application. Could you clarify that?",
    "I'm here to help with your job application. Please continue."
]

def translate_text(text, dest_lang):
    if dest_lang == "en" or not text.strip():
        return text
    try:
        return GoogleTranslator(source='auto', target=dest_lang).translate(text)
    except:
        return text

def generate_questions(tech_stack, years_exp):
    questions = {}
    try:
        years_exp = int(years_exp)
    except:
        years_exp = 0

    for tech in tech_stack:
        try:
            response = ollama.chat(
                model="mistral",
                messages=[{
                    "role": "user",
                    "content": f"Generate 3-5 technical interview questions about {tech} for {years_exp} years experience. Return each question on a new line."
                }]
            )
            content = response["message"]["content"].strip()
            questions[tech] = [q.split('. ', 1)[1] if '. ' in q else q 
                             for q in content.split("\n") if q.strip()][:5]
        except:
            questions[tech] = [f"Describe your experience with {tech}."]
    
    return questions

def generate_follow_up(question, answer):
    try:
        response = ollama.chat(
            model="mistral",
            messages=[{
                "role": "user",
                "content": f"Generate one follow-up question based on this answer:\nQuestion: {question}\nAnswer: {answer}"
            }]
        )
        return response["message"]["content"].strip()
    except:
        return f"Can you elaborate more on: {question}?"

def validate_email(email):
    return '@' in email and '.' in email.split('@')[-1] and len(email) > 5

def validate_phone(phone):
    return phone.isdigit() and len(phone) >= 7

steps = {
    "greeting": {
        "message": "👋 Hello! I'm the TalentScout Hiring Assistant, an AI-powered interviewer designed to help with your initial screening process. You can type 'exit' or 'quit' at any time to end our conversation. Let's begin! Please tell me your full name.",
        "next": "collect_name",
        "validation": lambda x: len(x.split()) >= 2,
        "error": "Please provide both first and last name"
    },
    "collect_name": {
        "message": "Thank you! What's your email address?",
        "next": "collect_email",
        "validation": validate_email,
        "error": "Please provide a valid email address"
    },
    "collect_email": {
        "message": "Please provide your phone number:",
        "next": "collect_phone",
        "validation": validate_phone,
        "error": "Please provide a valid phone number (at least 7 digits)"
    },
    "collect_phone": {
        "message": "What is your current location (city, country)?",
        "next": "collect_location",
        "validation": lambda x: len(x) > 3,
        "error": "Please provide a valid location"
    },
    "collect_location": {
        "message": "How many years of professional experience do you have?",
        "next": "collect_exp",
        "validation": lambda x: x.isdigit() and int(x) >= 0,
        "error": "Please enter a valid number of years"
    },
    "collect_exp": {
        "message": "What position(s) are you applying for?",
        "next": "collect_position",
        "validation": lambda x: len(x) > 2,
        "error": "Please enter a valid position"
    },
    "collect_position": {
        "message": "Please list your technical stack (comma-separated):",
        "next": "collect_tech_stack",
        "validation": lambda x: len(x) > 2,
        "error": "Please enter a valid position"
    },
    "collect_tech_stack": {
        "message": "Please list your technical stack (comma-separated):",
        "validation": lambda x: len([t.strip() for t in x.split(',') if t.strip()]) >= 1,
        "error": "Please list at least one technology"
    }
}

def chatbot_response(user_input):
    user_input = user_input.strip()
    lower_input = user_input.lower()
    
    if any(word in lower_input for word in ["exit", "quit", "stop"]):
        st.session_state.step = "end"
        return "Thank you for your time! We'll review your application and contact you shortly."
    
    current_step = steps.get(st.session_state.step, {})
    
    # Field validation
    if 'validation' in current_step:
        if not current_step['validation'](user_input):
            return current_step.get('error', "Please provide a valid response")
    
    # Process valid input based on current step
    if st.session_state.step == "greeting":
        st.session_state.info["name"] = user_input
        st.session_state.step = "collect_name"
        return steps["collect_name"]["message"]
    
    elif st.session_state.step == "collect_name":
        st.session_state.info["name"] = user_input  
        st.session_state.step = "collect_email"
        return steps["collect_email"]["message"]
    
    elif st.session_state.step == "collect_email":
        st.session_state.info["email"] = user_input
        st.session_state.step = "collect_phone"
        return steps["collect_phone"]["message"]
    
    elif st.session_state.step == "collect_phone":
        st.session_state.info["phone"] = user_input
        st.session_state.step = "collect_location"
        return steps["collect_location"]["message"]
    
    elif st.session_state.step == "collect_location":
        st.session_state.info["location"] = user_input
        st.session_state.step = "collect_exp"
        return steps["collect_exp"]["message"]
    
    elif st.session_state.step == "collect_exp":
        st.session_state.info["experience"] = user_input
        st.session_state.step = "collect_position"
        return steps["collect_position"]["message"]
    
    elif st.session_state.step == "collect_position":
        st.session_state.info["position"] = user_input
        st.session_state.step = "collect_tech_stack"
        # Transition directly without re-displaying duplicate prompt later
        return steps["collect_tech_stack"]["message"]
    
    elif st.session_state.step == "collect_tech_stack":
        # --- CORRECTION: Remove duplicate tech stack prompt from the chat history ---
        if st.session_state.messages and st.session_state.messages[-1]["content"] == steps["collect_tech_stack"]["message"]:
            st.session_state.messages.pop()
        # --------------------------------------------------------------------------
        tech_stack = [t.strip().lower() for t in user_input.split(',') if t.strip()]
        st.session_state.info["tech_stack"] = tech_stack
        st.session_state.info["tech_questions"] = generate_questions(
            tech_stack, 
            st.session_state.info["experience"]
        )
        if tech_stack:
            st.session_state.current_tech = tech_stack[0]
            st.session_state.current_question = 0
            st.session_state.follow_up = None
            st.session_state.step = "tech_assessment"
            first_question = st.session_state.info["tech_questions"][tech_stack[0]][0]
            return f"Let's begin the technical assessment!\n\n{tech_stack[0].upper()} questions:\n\n{first_question}"
        return "Please specify at least one technology"
    
    elif st.session_state.step == "tech_assessment":
        return handle_tech_assessment(user_input)
    
    return random.choice(FALLBACK_RESPONSES)
def handle_tech_assessment(user_input):
    tech = st.session_state.current_tech
    questions = st.session_state.info["tech_questions"][tech]
    
    if tech not in st.session_state.info["answers"]:
        st.session_state.info["answers"][tech] = []
    
    # Compute sentiment for the response using the global analyzer
    sentiment = analyzer.polarity_scores(user_input)
    
    # Handle follow-up if one exists
    if st.session_state.follow_up:
        st.session_state.info["answers"][tech][-1]["follow_ups"].append({
            "question": st.session_state.follow_up,
            "answer": user_input,
            "sentiment": sentiment  # sentiment for follow-up answer
        })
        st.session_state.follow_up = None
    else:
        # Save the main answer with sentiment analysis
        if st.session_state.current_question < len(questions):
            st.session_state.info["answers"][tech].append({
                "question": questions[st.session_state.current_question],
                "answer": user_input,
                "sentiment": sentiment,  # sentiment for main answer
                "follow_ups": []
            })
            follow_up = generate_follow_up(
                questions[st.session_state.current_question], 
                user_input
            )
            st.session_state.follow_up = follow_up
            return follow_up

    # Move to next question within the current technology if available
    if st.session_state.current_question < len(questions) - 1:
        st.session_state.current_question += 1
        return questions[st.session_state.current_question]
    
    # After finishing questions for the current technology, move to the next technology if available
    tech_list = st.session_state.info["tech_stack"]
    next_idx = tech_list.index(tech) + 1
    if next_idx < len(tech_list):
        st.session_state.current_tech = tech_list[next_idx]
        st.session_state.current_question = 0
        st.session_state.follow_up = None
        first_question = st.session_state.info["tech_questions"][tech_list[next_idx]][0]
        return f"Moving to {tech_list[next_idx].upper()} questions:\n\n{first_question}"
    
    # End the assessment if no more technologies remain
    st.session_state.step = "end"
    return "Assessment complete! Thank you for your responses."

def main():
    st.set_page_config(page_title="TalentScout AI Interviewer", page_icon="🤖")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        greeting = steps["greeting"]["message"]
        st.session_state.messages.append({"role": "assistant", "content": greeting})
    
    st.title("TalentScout AI Interviewer 🤖")
    st.caption("AI-powered technical screening assistant")
    
    selected_lang = st.selectbox("🌐 Select Language:", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[selected_lang]
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(translate_text(msg["content"], lang_code))
    
    if prompt := st.chat_input("💬 Type your response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = chatbot_response(prompt)
        if response:
            translated = translate_text(response, lang_code)
            st.session_state.messages.append({"role": "assistant", "content": translated})
        st.rerun()

if __name__ == "__main__":
    main()













