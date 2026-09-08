Set-Content -Path "README.md" -Value @"
# FewMates 🚀
> **AI-Powered Academic Assistant API with RAG & SSE Streaming**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Google GenAI](https://img.shields.io/badge/Google%20GenAI-Gemini%202.5-4285F4.svg)](https://ai.google.dev/)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange.svg)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FewMates** is an asynchronous academic assistant backend built with FastAPI and Google Gemini 2.5 Flash. It provides real-time streaming responses via Server-Sent Events (SSE) and enables contextual document querying (RAG) over uploaded course materials using ChromaDB.

---

## 🏛️ System Architecture

\`\`\`
                                  +-----------------------+
                                  |   Frontend / Client   |
                                  +-----------+-----------+
                                              |
                                   HTTP / SSE | Requests
                                              v
+-----------------------------------------------------------------------------------+
| FewMates FastAPI Backend                                                          |
|                                                                                   |
|  +--------------------+       +-----------------------+       +----------------+  |
|  | /upload-pdf        | ----> | PyPDF & Text Splitter | ----> | ChromaDB       |  |
|  | (Document Ingest)  |       +-----------------------+       | (Vector Store) |  |
|  +--------------------+                                       +-------+--------+  |
|                                                                       |           |
|                                                               Context | Retrieval |
|                                                                       v           |
|  +--------------------+       +-----------------------+       +---------------+   |
|  | /chat/stream       | ----> | RAG Prompt Builder    | ----> | Google GenAI  |   |
|  | (SSE Endpoint)     |       +-----------------------+       | (Gemini 3.6)  |   |
|  +---------+----------+                                       +-------+-------+   |
+------------|----------------------------------------------------------|-----------+
             |                                                          |
             +<----------------- EventStream Chunks <-------------------+
\`\`\`

---

## ✨ Core Features

* **Real-time SSE Streaming:** Asynchronous text streaming delivering sub-second response latency via Server-Sent Events.
* **Retrieval-Augmented Generation (RAG):** Context-aware question answering backed by local ChromaDB vector index and PyPDF ingestion.
* **Dynamic System Prompting:** Built-in academic instruction rules guaranteeing clean Markdown, structured explanations, and verified sources.
* **Asynchronous I/O:** Powered by \`FastAPI\`, \`aiofiles\`, and non-blocking streaming handlers.

---

## 🛠️ Tech Stack

* **Framework:** FastAPI
* **LLM:** Google GenAI (\`gemini-2.5-flash\`)
* **Vector Database:** ChromaDB
* **Document Processing:** PyPDF, LangChain Text Splitters
* **Server:** Uvicorn

---

## 🚀 Quickstart

### Prerequisites

* Python 3.10+ installed
* Google Gemini API Key

### Installation

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/quzsibidi/FewMates.git
   cd FewMates
   \`\`\`

2. **Set up a virtual environment:**
   \`\`\`bash
   python -m venv .venv
   \`\`\`
   * Activate on Windows:
     \`\`\`powershell
     .\.venv\Scripts\Activate.ps1
     \`\`\`
   * Activate on Linux/macOS:
     \`\`\`bash
     source .venv/bin/activate
     \`\`\`

3. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Configure Environment Variables:**
   Create a \`.env\` file in the project root directory or export your Gemini API key:
   \`\`\`bash
   export GEMINI_API_KEY="your-gemini-api-key"
   \`\`\`

5. **Run the server:**
   \`\`\`bash
   python -m uvicorn main:app --reload
   \`\`\`

   The server will start at \`http://127.0.0.1:8000\`. Interactive API documentation will be available at \`http://127.0.0.1:8000/docs\`.

---

## 📄 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| \`POST\` | \`/upload-pdf\` | Upload and chunk PDF documents into ChromaDB |
| \`POST\` | \`/chat/stream\` | Send prompt with optional RAG flag and receive SSE stream |

---

## 📜 License

Distributed under the MIT License. See \`LICENSE\` for more information.
"@ -Encoding UTF8
