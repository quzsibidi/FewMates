# 🏫 Experimental School Assistant AI

An extensible, modular, and customizable AI Assistant built with **Google Gemini 1.5 Flash API** and **Streamlit**. Designed as an open-source experimental assistant for educational institutions, allowing seamless integration of custom school knowledge bases (`JSON`) and real-time persona/prompt switching.

---

## ✨ Key Features

- 🧠 **Dynamic Persona Switching**: Switch between predefined system instructions (e.g., *Guidance Counselor*, *Strict Teacher*, *Friendly Classmate*) on the fly using `prompts.json`.
- 📁 **Custom Knowledge Base**: Upload custom school data dynamically via the UI or rely on default `school_data.json` context.
- ⚡ **Real-Time Token Streaming**: Low-latency, streaming-based chat responses powered by Streamlit's native `write_stream`.
- 💬 **Contextual Chat Memory**: Retains multi-turn chat history utilizing Gemini's `start_chat` session handler.
- 🔐 **Secure Key Management**: Uses `python-dotenv` to isolate sensitive credentials from public code repositories.

---

## 🛠️ Project Structure

```text
├── app.py              # Main Streamlit web application & Gemini logic
├── school_data.json    # Default context data (schedule, rules, announcements)
├── prompts.json        # Predefined system instructions & personas
├── .env.example        # Template for environment variables
├── .gitignore          # Git exclusion list (ignores .env, bytecode, etc.)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

🚀 Quickstart
1. Prerequisites
Make sure you have Python 3.10+ installed on your system.

2. Installation
Clone the repository and install the required dependencies:
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
pip install -r requirements.txt

3. API Key Setup
Get a Gemini API key from Google AI Studio.

Create a .env file in the root directory:
GEMINI_API_KEY=your_actual_gemini_api_key_here
(Note: Never commit your actual .env file to version control.)

4. Running the Application
Launch the Streamlit app:
streamlit run app.py

⚙️ Configuration & Customization
Customizing Knowledge Base (school_data.json)
You can edit school_data.json directly or upload a custom JSON file via the Streamlit sidebar. The JSON structure should reflect relevant school metadata:
{
  "school_name": "Experimental High School",
  "rules": [
    "Mobile phones are strictly prohibited during class hours.",
    "Students must maintain silence in the library."
  ],
  "schedule": {
    "Monday": "Mathematics, Physics, Literature",
    "Tuesday": "Chemistry, Biology, English"
  },
  "announcements": [
    "Science Fair applications are now open.",
    "AI Club meeting this Friday at 3:30 PM."
  ]
}

Customizing Personas (prompts.json)
Add or modify system prompts in prompts.json to introduce new bot behaviors:
{
  "Guidance Counselor": "You are an empathetic, supportive, and motivating high school guidance counselor. Help students reduce academic stress and provide constructive advice.",
  "Strict Teacher": "You are a strict, rule-enforcing, and serious teacher on duty. Give short, direct, and authoritative responses.",
  "Friendly Classmate": "You are a friendly, witty high school classmate who speaks casually and uses peer jargon."
}
🤝 Contributing  
Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.
License  
This project is licensed under the MIT License - see the LICENSE file for details.
🗺️ Roadmap & Future Enhancements
Here are the planned features and improvements for upcoming releases:

[ ] Document Support (RAG Integration): Expand beyond JSON to support .pdf, .docx, and .txt files for school rulebooks and course syllabus processing.

[ ] Voice Interaction: Integrate speech-to-text (STT) and text-to-speech (TTS) for natural voice conversations with the assistant.

[ ] Multi-Language Support: Enable dynamic language switching (e.g., Turkish, English, Spanish) within the chat interface.

[ ] Export Chat Logs: Allow students and teachers to download chat transcripts as PDF or Markdown files.

[ ] Advanced Guardrails: Strengthen safety boundaries to prevent off-topic or policy-violating queries.

[ ] UI/UX Polish: Custom CSS styling with light/dark theme toggles matching school branding.