import os
import json
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found! Please check your .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

# Page Configuration
st.set_page_config(page_title="Experimental School Assistant", page_icon="🏫", layout="wide")
st.title("🏫 Experimental School Assistant AI")

# --- SIDEBAR (Settings & Data Upload) ---
with st.sidebar:
    st.header("⚙️ Bot Configuration")
    
    # 1. Persona Selection
    st.subheader("1. Bot Persona (Prompt)")
    try:
        with open("prompts.json", "r", encoding="utf-8") as f:
            prompts = json.load(f)
        selected_mode = st.selectbox("Select a persona:", list(prompts.keys()))
        system_instruction = prompts[selected_mode]
    except Exception:
        system_instruction = "You are a helpful school assistant."
        st.warning("prompts.json not found, using default persona.")

    # 2. Custom Data Upload
    st.subheader("2. School Knowledge Base (JSON)")
    uploaded_file = st.file_uploader("Upload custom school JSON", type=["json"])
    
    if uploaded_file is not None:
        school_data = json.load(uploaded_file)
        st.success("Custom School Data Loaded!")
    else:
        try:
            with open("school_data.json", "r", encoding="utf-8") as f:
                school_data = json.load(f)
            st.info("Using default school_data.json")
        except Exception:
            school_data = {"info": "No data available"}

    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.session_state.chat = None
        st.rerun()

# --- BACKEND MODEL SETUP ---
full_instruction = f"""
You are an experimental School Assistant AI.
Answer questions based STRICTLY on the following school context.
If a question cannot be answered using the context, state: 'This information is not available in the school database.'

[SCHOOL KNOWLEDGE BASE]:
{json.dumps(school_data, ensure_ascii=False, indent=2)}

[PERSONA & STYLE INSTRUCTIONS]:
{system_instruction}
"""

if "chat" not in st.session_state or st.session_state.chat is None:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=full_instruction
    )
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask something about the school..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(user_input, stream=True)
            
            def stream_generator():
                for chunk in response:
                    yield chunk.text
            
            bot_reply = st.write_stream(stream_generator())
        except Exception as e:
            bot_reply = f"[Error]: {str(e)}"
            st.markdown(bot_reply)
        
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})