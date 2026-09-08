# AI School & Study Assistant API

An intelligent, multi-tenant AI Assistant API designed to generate personalized daily study plans and academic guidance for high school students. Powered by FastAPI and the Google Gemini 3.6 Flash model.

## Features
- **Personalized Scheduling:** Dynamically builds study plans based on weak subjects, daily targets, and personal busy hours.
- **Session-Based Chat History:** Maintains contextual dialogue across user interactions.
- **Modern SDK:** Built using the official `google-genai` SDK and `gemini-3.6-flash`.
- **CORS Supported:** Ready for external web or mobile client integration.
- **Interactive UI:** Built-in web client (`/`) and auto-generated OpenAPI docs (`/docs`).

## Tech Stack
- Python 3.10+
- FastAPI & Uvicorn
- Pydantic v2
- Google GenAI SDK (`google-genai`)

## Quick Start

### 1. Installation
Clone the repository and install the dependencies:
```bash
git clone <your-repository-url>
cd sa-ma-ai-i-leri
pip install -r requirements.txt