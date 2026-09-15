# AI Multi-Research Agent

A multi-agent research application that searches the web, scrapes the best sources, writes a structured report, and critiques the result using OpenRouter-hosted models.

## Features

- Search agent that queries DuckDuckGo for recent, relevant sources
- Reader agent that fetches and cleans a source page for deeper context
- Writer chain that drafts a polished research report
- Critic chain that scores and reviews the report
- Both a Streamlit web app and a Python CLI workflow

## Tech Stack

- Python
- LangChain + LangChain Core
- OpenRouter via `langchain-openrouter`
- Streamlit
- DuckDuckGo Search
- Requests + BeautifulSoup
- Python-dotenv

## Project Workflow

1. User enters a research topic
2. The search agent finds relevant sources
3. The reader agent scrapes the most useful page
4. The writer chain creates a structured report
5. The critic chain reviews the final output and gives feedback

## Setup

### 1) Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Add your OpenRouter API key

Create a `.env` file in the project root with:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

This is loaded automatically by the app using `python-dotenv`.

## Run the app

### Streamlit UI

```bash
streamlit run streamlit_app.py
```

Then open the local URL shown by Streamlit in your browser.

### CLI version

```bash
python pipeline.py
```

## File Structure

- `agents.py` — LLM setup and agent definitions
- `tools.py` — search and scraping tool functions
- `pipeline.py` — command-line research pipeline runner
- `streamlit_app.py` — Streamlit interface
- `.env` — environment variables such as `OPENROUTER_API_KEY`
- `requirements.txt` — Python project dependencies

## Notes

- The default model is `google/gemma-4-31b-it-20260402:free` via OpenRouter.
- The project expects a valid OpenRouter key in the environment.
- If `duckduckgo_search` changes behavior across versions, the tool layer includes compatibility handling for different package APIs.

## Troubleshooting

- If the app cannot connect to OpenRouter, verify that `OPENROUTER_API_KEY` is set correctly in the `.env` file.
- If dependencies are missing, run `pip install -r requirements.txt` again.
- If the app fails during search, confirm the `duckduckgo_search` package is installed and importable.

## License

This project is intended for educational and local research use.