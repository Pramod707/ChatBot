# 🤖 Multi-LLM ChatBot

A collection of chatbot implementations built with **LangChain** and **Streamlit**, supporting both cloud-hosted and local Large Language Models (LLMs). This repository also contains experiments with Hugging Face models, API integrations, and AI agents.

---

## ✨ Features

- 💬 Streamlit-based chatbot interface
- 🤖 Supports multiple LLM providers
  - Groq
  - Local LLMs (Ollama)
  - Hugging Face
- 🔗 LangChain & LCEL
- 📝 Prompt Templates
- 🔒 Environment variable management
- 🧪 Experimental notebooks for Agents and Hugging Face

---

## 📂 Project Structure

```text
ChatBot/
│
├── agents/
│   └── agent.ipynb          # LangChain Agent experiments
│
├── apis/
│   ├── app.py               # API server
│   └── client.py            # API client
│
├── Bots/
│   ├── main.py              # Groq chatbot
│   └── localai.py           # Local LLM chatbot
│
├── groq/
│   └── app.py               # Groq examples
│
├── huggingface/
│   ├── pdfs/                # Sample documents
│   └── huggingface.ipynb    # Hugging Face experiments
│
├── outputs/
│   ├── groq.png
│   └── loacal.png
│
├── Rag/                     # RAG experiments
├── .env
├── pyproject.toml
├── req.txt
├── README.md
└── test.ipynb
```

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq API
- Ollama
- Hugging Face
- dotenv
- uv

---

## 🚀 Installation

Clone the repository

```bash
git clone <repository-url>
cd ChatBot
```

Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r req.txt
```

or

```bash
uv sync
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_api_key
```

---

## ▶️ Run

### Groq ChatBot

```bash
streamlit run Bots/main.py
```

### Local LLM ChatBot

```bash
streamlit run Bots/localai.py
```

---

## 📸 Demo

| Groq | Local LLM |
|------|-----------|
| ![](outputs/groq.png) | ![](outputs/loacal.png) |

---

## 📚 Topics Covered

- LangChain
- LCEL
- Prompt Engineering
- Chat Models
- Output Parsers
- Local LLMs (Ollama)
- Groq API
- Hugging Face
- AI Agents
- RAG (Work in Progress)

---

## 👨‍💻 Author

**Pramod B**

- GitHub: https://github.com/Pramod707
- LinkedIn: https://linkedin.com/in/pramod7

---

⭐ If you found this project helpful, consider giving it a star.