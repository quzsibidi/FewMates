# FewMates - Experimental School Assistant AI

A Streamlit-based AI assistant powered by the Groq API that answers questions based on a specific school knowledge base and customizable personas.

## Features

- **Groq API Integration:** Fast and efficient inference using Groq's high-performance LLMs.
- **Custom Knowledge Base:** Load school-specific data dynamically via JSON uploads or default configuration files.
- **Persona Management:** Switch between different system prompts and assistant personalities using `prompts.json`.
- **Interactive Chat Interface:** Clean, streaming-supported conversational UI built with Streamlit.

## Setup & Installation

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install streamlit python-dotenv openai

OPENAI_API_KEY=your_groq_api_key_here
OPENAI_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=openai/gpt-oss-120b

Running the Application
Launch the Streamlit app using the following command:

PowerShell
streamlit run app.py