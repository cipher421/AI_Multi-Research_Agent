from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

# Support multiple duckduckgo_search versions / APIs:
# - older versions expose a `ddg` function
# - newer versions provide a `DDGS` class (or module.submodule)
try:
    # prefer simple function if available
    from duckduckgo_search import ddg  # type: ignore
    _DDG_MODE = "function"
except Exception:
    try:
        from duckduckgo_search import DDGS  # type: ignore
        _DDG_MODE = "class"
        _DDGS_CLASS = DDGS
    except Exception:
        # last resort: import package and try to access submodule
        import duckduckgo_search as _ddgs_mod  # type: ignore
        _DDG_MODE = "module"
        _DDGS_CLASS = getattr(_ddgs_mod, "duckduckgo_search", None) and getattr(_ddgs_mod.duckduckgo_search, "DDGS", None)

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
    results = None
    if _DDG_MODE == "function":
        try:
            results = ddg(query, max_results=5)  # type: ignore
        except Exception:
            results = []
    else:
        try:
            # instantiate DDGS class from whichever import succeeded
            ddgs = _DDGS_CLASS()  # type: ignore
            results = ddgs.text(query, max_results=5)
        except Exception:
            results = []

    out = []

    if not results:
        return ""

    for r in results:
        # result shape varies between providers/backends
        if isinstance(r, dict):
            title = r.get("title") or r.get("name") or ""
            url = r.get("href") or r.get("url") or r.get("link") or ""
            snippet = r.get("body") or r.get("snippet") or r.get("text") or ""
        else:
            # fallback: try to string-format the result
            s = str(r)
            title = s[:80]
            url = ""
            snippet = s
        out.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet[:300]}\n")

    return "\n----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

