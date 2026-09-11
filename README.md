# AI Multi-Research Agent

A four-stage multi-agent research pipeline built with LangChain and Streamlit. A search agent, a reader/scraper agent, a writer chain, and a critic chain work together to turn a topic into a structured, cited research report with a critique.

## Features

- **Search agent** — tool-calling agent (`create_agent`) that queries DuckDuckGo for titles, URLs, and snippets
- **Reader agent** — tool-calling agent that scrapes and cleans a chosen page (`requests` + `BeautifulSoup`), truncated to ~3000 characters
- **Writer chain** — prompt chain that drafts a structured report (Introduction / Key Findings / Conclusion / Sources)
- **Critic chain** — prompt chain that scores the report out of 10 with strengths, areas to improve, and a one-line verdict
- Both a Streamlit web UI and a scripted CLI runner

## Tech Stack

- **Orchestration:** LangChain (`langchain`, `langchain-core`, `langchain-community`)
- **LLM:** OpenRouter, via `langchain-openrouter`'s `ChatOpenRouter` — default model `openai/gpt-oss-20b:free`
- **Search:** `duckduckgo_search`, with fallback handling across its `ddg` function and `DDGS` class APIs (the package's interface has changed across versions)
- **Scraping:** `requests` + `beautifulsoup4` (+ `lxml`/`html5lib` parsers)
- **UI:** Streamlit

## Pipeline

```
Topic
  │
  ▼
Search Agent   → web_search (DuckDuckGo)                → titles, URLs, snippets
  │
  ▼
Reader Agent   → scrape_url (requests + BeautifulSoup)   → cleaned page text (~3000 chars)
  │
  ▼
Writer Chain   → structured report (Introduction / Key Findings / Conclusion / Sources)
  │
  ▼
Critic Chain   → scored review (Strengths / Areas to Improve / Verdict)
```

All four stages run on the same LLM (`openai/gpt-oss-20b:free` via OpenRouter, `temperature=0`, `max_tokens=1000` by default). Only the Search and Reader stages are tool-calling agents (`create_agent`); the Writer and Critic stages are plain prompt chains (`ChatPromptTemplate | llm | StrOutputParser`).

## Installation

```bash
git clone https://github.com/chmodgaurav/AI-Multi-Research-Agent.git
cd AI-Multi-Research-Agent
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

`agents.py` initializes `ChatOpenRouter(model="openai/gpt-oss-20b:free", ...)`, which reads `OPENROUTER_API_KEY` from the environment.

## Usage

### Web UI

```bash
streamlit run streamlit_app.py
```

Open `http://localhost:8501`, enter a research topic, and the app runs through search → read → write → critique.

### CLI

```bash
python pipeline.py
```

Prompts for a topic in the terminal, runs the same four-stage pipeline, and prints each stage's output as it completes.

## Project Structure

| File | Purpose |
|---|---|
| `streamlit_app.py` | Web UI entry point (Streamlit) |
| `pipeline.py` | CLI runner for the full pipeline (`run_research_pipeline`) |
| `agents.py` | Agent/chain definitions and LLM configuration |
| `tools.py` | `web_search` and `scrape_url` tool implementations |
| `requirements.txt` | Python dependencies |

## Implementation Notes

- **Search** (`tools.web_search`): wraps `duckduckgo_search`, trying the module's `ddg` function first, then its `DDGS` class, then a last-resort submodule lookup — this covers both older and newer versions of the package.
- **Scraper** (`tools.scrape_url`): fetches and cleans page text, truncated to ~3000 characters to keep prompts within context limits.
- **Model:** change the model, temperature, or token limit in `agents.py` (`llm = ChatOpenRouter(...)`).
- **Writer/Critic:** both are plain prompt chains, not tool-calling agents — they receive text (topic + combined research, or the drafted report) and return text.

## Troubleshooting

- **`duckduckgo_search` import errors:** the package's API has changed across versions; `tools.py` already handles both the legacy `ddg` function and the newer `DDGS` class, but ensure the package is installed (`pip install duckduckgo_search`).
- **LLM authentication errors:** confirm `OPENROUTER_API_KEY` is set and valid, and that the account has credit/access for the configured model.
- **Missing packages in Streamlit:** re-run `pip install -r requirements.txt` inside the activated virtual environment.