# 📚 Automated Book Workflow

An AI-powered pipeline to **scrape, rewrite, review, and publish book chapters** automatically. This project demonstrates a modern, agent-based content automation system using Python, Playwright, and ChromaDB.

---

## ✨ Features

- 🤖 **Agent-Based Architecture**  
  Modular agents handle each part of the workflow — scraping, rewriting, reviewing, and versioning.

- 🌐 **Web Content Scraping**  
  Uses [Playwright](https://playwright.dev/python/) to scrape chapters and capture full-page screenshots.

- ✍️ **AI-Powered Content Generation**  
  Simulates AI agents for rewriting and refining content using LLMs.

- 🧑‍💻 **Human-in-the-Loop (HITL)**  
  Reviewer can approve or edit AI-generated content manually via CLI.

- 💾 **Vector-Based Versioning**  
  Final versions are stored in [ChromaDB](https://docs.trychroma.com/), enabling semantic search.

- 🧠 **Reinforcement Learning Concept**  
  Assigns reward scores to AI outputs based on how little the human had to edit.

- 🚀 **API-Ready**  
  A sample [FastAPI](https://fastapi.tiangolo.com/) server exposes the workflow as an HTTP API.

---

## ⚙️ How It Works

The workflow is managed by a central orchestrator script (`main.py`) that runs each agent in sequence:

1. **Scraping Agent**  
   → Takes a URL, scrapes the chapter's text, saves a screenshot.

2. **AI Writer Agent**  
   → Rewrites the raw text using creative prompts.

3. **AI Reviewer Agent**  
   → Refines grammar, clarity, and style.

4. **HITL Agent (Human-in-the-Loop)**  
   → CLI prompt allows human to approve, edit, or reject.

5. **Versioning Agent**  
   → Calculates an RL-style reward score  
   → Saves final text + metadata to ChromaDB

6. **Search**  
   → Search by semantic similarity or highest reward score.

---

## 🛠️ Tech Stack

| Category           | Tool                         |
|--------------------|------------------------------|
| Backend            | Python                       |
| Web Scraping       | Playwright                   |
| AI Text Handling   | OpenAI / LLMs (simulated)    |
| Database           | ChromaDB (Vector Store)      |
| API Layer          | FastAPI, Uvicorn             |
| Text Comparison    | python-Levenshtein           |
| HTML Parsing       | BeautifulSoup4               |

---

## 🚀 Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2. Create a Virtual Environment

**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

### 5. Run the Workflow

```bash
python main.py
```

The workflow will:
- Scrape a chapter from a URL
- Rewrite and refine it using AI agents
- Let you review it in the CLI
- Save outputs (text, screenshots, vector data) in the `outputs/` directory

---

## 📁 Project Structure

```
/automated-book-workflow
│
├── main.py                # The main orchestrator script
├── agents/                # Specialized agents
│   ├── scraping_agent.py
│   ├── ai_agents.py
│   ├── hitl_agent.py
│   ├── versioning_agent.py
│
├── api/                   # Optional FastAPI service
│   └── server.py
│
├── outputs/               # Generated content
│   ├── /screenshots
│   └── /chapters
│
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # You are here!
```

---
