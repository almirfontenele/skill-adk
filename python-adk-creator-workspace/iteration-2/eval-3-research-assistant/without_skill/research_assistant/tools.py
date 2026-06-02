"""Tools available to the Research Assistant agent.

Each public function in this module is registered as a callable tool that
the Gemini model can invoke via automatic function calling.  The docstrings
and type annotations are used by the SDK to build the function declarations
sent to the model, so keep them accurate and complete.
"""

from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level config reference (injected by the agent at startup)
# ---------------------------------------------------------------------------
_serpapi_key: str = ""
_max_results: int = 5


def configure(serpapi_key: str, max_results: int = 5) -> None:
    """Inject runtime configuration into the tools module."""
    global _serpapi_key, _max_results
    _serpapi_key = serpapi_key
    _max_results = max_results


# ---------------------------------------------------------------------------
# Web search tool
# ---------------------------------------------------------------------------

def search_web(query: str, num_results: int = 5) -> str:
    """Search the web for a given query and return a JSON list of results.

    Each result contains 'title', 'link', and 'snippet' fields.
    Use this tool when you need up-to-date information or facts from the web.

    Args:
        query: The search query string.
        num_results: Maximum number of results to return (1-10).

    Returns:
        A JSON-encoded list of search result objects, or an error message.
    """
    num_results = max(1, min(num_results, 10))

    if _serpapi_key:
        return _search_via_serpapi(query, num_results)
    else:
        return _search_via_duckduckgo(query, num_results)


def _search_via_serpapi(query: str, num_results: int) -> str:
    """Use SerpAPI Google Search endpoint."""
    params = {
        "q": query,
        "num": num_results,
        "api_key": _serpapi_key,
        "engine": "google",
    }
    url = "https://serpapi.com/search?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:  # noqa: S310
            data = json.loads(resp.read().decode())
        organic = data.get("organic_results", [])[:num_results]
        results = [
            {
                "title": r.get("title", ""),
                "link": r.get("link", ""),
                "snippet": r.get("snippet", ""),
            }
            for r in organic
        ]
        return json.dumps(results, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001
        logger.error("SerpAPI search failed: %s", exc)
        return json.dumps({"error": str(exc)})


def _search_via_duckduckgo(query: str, num_results: int) -> str:
    """Fallback: use DuckDuckGo Instant Answer API (no key required, limited results)."""
    params = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
    url = "https://api.duckduckgo.com/?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ResearchAssistant/0.1"})
        with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
            data = json.loads(resp.read().decode())

        results: list[dict] = []

        # Abstract (top answer)
        if data.get("AbstractText") and data.get("AbstractURL"):
            results.append(
                {
                    "title": data.get("Heading", query),
                    "link": data["AbstractURL"],
                    "snippet": data["AbstractText"],
                }
            )

        # Related topics
        for topic in data.get("RelatedTopics", []):
            if len(results) >= num_results:
                break
            if isinstance(topic, dict) and topic.get("Text") and topic.get("FirstURL"):
                results.append(
                    {
                        "title": topic.get("Text", "")[:80],
                        "link": topic["FirstURL"],
                        "snippet": topic.get("Text", ""),
                    }
                )

        if not results:
            results = [
                {
                    "title": "No results found",
                    "link": "",
                    "snippet": (
                        "DuckDuckGo Instant Answer returned no results for this query. "
                        "Try providing a SERPAPI_KEY for richer search results."
                    ),
                }
            ]

        return json.dumps(results[:num_results], ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001
        logger.error("DuckDuckGo search failed: %s", exc)
        return json.dumps({"error": str(exc)})


# ---------------------------------------------------------------------------
# Content fetch tool
# ---------------------------------------------------------------------------

def fetch_page_content(url: str, max_chars: int = 4000) -> str:
    """Fetch the plain-text content of a web page.

    Strips HTML tags and returns readable text, suitable for summarization.
    Use this after search_web to retrieve the full content of a specific page.

    Args:
        url: The full URL of the page to fetch.
        max_chars: Maximum number of characters to return (to stay within
                   model context limits).

    Returns:
        Plain-text content of the page, or an error description.
    """
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (compatible; ResearchAssistant/0.1; "
                    "+https://github.com/example/research_assistant)"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310
            raw = resp.read(max_chars * 5)  # over-fetch, then trim after strip
            charset = resp.headers.get_content_charset("utf-8")
            html = raw.decode(charset, errors="replace")

        text = _strip_html(html)
        return text[:max_chars]
    except Exception as exc:  # noqa: BLE001
        logger.error("fetch_page_content failed for %s: %s", url, exc)
        return f"Error fetching page: {exc}"


def _strip_html(html: str) -> str:
    """Remove HTML tags and collapse whitespace."""
    import re

    # Remove <script> and <style> blocks entirely
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    # Remove remaining tags
    html = re.sub(r"<[^>]+>", " ", html)
    # Decode common HTML entities
    for entity, char in [
        ("&amp;", "&"),
        ("&lt;", "<"),
        ("&gt;", ">"),
        ("&quot;", '"'),
        ("&#39;", "'"),
        ("&nbsp;", " "),
    ]:
        html = html.replace(entity, char)
    # Collapse whitespace
    html = re.sub(r"\s+", " ", html).strip()
    return html


# ---------------------------------------------------------------------------
# Summarize tool
# ---------------------------------------------------------------------------

def summarize_text(text: str, max_words: int = 300, focus: Optional[str] = None) -> str:
    """Summarize a block of text in plain English.

    This is a lightweight extractive summarizer that does NOT call the model
    again — it trims and condenses the text so it can be passed back to the
    model for a final, high-quality response.

    Args:
        text: The text to summarize.
        max_words: Approximate maximum number of words in the output.
        focus: Optional topic or question to guide relevance ranking.

    Returns:
        A condensed version of the input text.
    """
    if not text or not text.strip():
        return "No content to summarize."

    sentences = _split_sentences(text)

    if focus:
        sentences = _rank_sentences(sentences, focus)

    # Greedily collect sentences until we hit the word limit
    words_so_far = 0
    selected: list[str] = []
    for sent in sentences:
        wc = len(sent.split())
        if words_so_far + wc > max_words and selected:
            break
        selected.append(sent)
        words_so_far += wc

    if not selected:
        # Fall back: truncate by words
        words = text.split()
        return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

    return " ".join(selected)


def _split_sentences(text: str) -> list[str]:
    import re

    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if len(p.strip()) > 20]


def _rank_sentences(sentences: list[str], focus: str) -> list[str]:
    """Return sentences sorted by number of focus-keyword matches (descending)."""
    keywords = set(focus.lower().split())

    def score(s: str) -> int:
        words = set(s.lower().split())
        return len(words & keywords)

    return sorted(sentences, key=score, reverse=True)
