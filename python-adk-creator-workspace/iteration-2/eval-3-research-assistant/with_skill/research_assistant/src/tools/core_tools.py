"""Core tools for the research assistant agent.

Each function must have:
- A clear docstring (used as tool description for automatic function calling)
- Type hints on all parameters and return value
- Primitive or dict return type
"""

import urllib.parse
import urllib.request
import json


def search_web(query: str) -> str:
    """Search the web for information about a given query.

    Uses DuckDuckGo Instant Answer API to retrieve search results.

    Args:
        query: The search query string to look up.

    Returns:
        A string with search results or an abstract about the topic.
    """
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "research-assistant/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        abstract = data.get("AbstractText", "")
        related = [r.get("Text", "") for r in data.get("RelatedTopics", [])[:3] if r.get("Text")]

        if abstract:
            result = f"Summary: {abstract}"
            if related:
                result += "\n\nRelated topics:\n" + "\n".join(f"- {t}" for t in related)
            return result
        elif related:
            return "Related topics found:\n" + "\n".join(f"- {t}" for t in related)
        else:
            return f"No direct results found for '{query}'. Try rephrasing your query."
    except Exception as e:
        return f"Search failed: {e}. Please check your internet connection."


def summarize_content(text: str, max_sentences: int = 5) -> str:
    """Summarize a block of text by extracting the most important sentences.

    Args:
        text: The content to summarize.
        max_sentences: Maximum number of sentences to include in the summary (default 5).

    Returns:
        A concise summary of the provided text.
    """
    if not text or not text.strip():
        return "No content provided to summarize."

    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    if len(sentences) <= max_sentences:
        return text.strip()

    # Simple extractive summary: take first sentence, last sentence, and evenly spaced middle ones
    if max_sentences <= 2:
        selected = sentences[:max_sentences]
    else:
        step = max(1, (len(sentences) - 2) // (max_sentences - 2))
        middle = sentences[1:-1][::step][: max_sentences - 2]
        selected = [sentences[0]] + middle + [sentences[-1]]

    return ". ".join(selected) + "."


def get_page_content(url: str) -> str:
    """Fetch and return the plain text content of a web page.

    Args:
        url: The full URL of the web page to fetch (e.g. 'https://example.com').

    Returns:
        Plain text content of the page, truncated to 2000 characters if necessary.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "research-assistant/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode(errors="replace")

        # Strip HTML tags with a simple approach
        import re
        text = re.sub(r"<[^>]+>", " ", raw)
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) > 2000:
            return text[:2000] + "... [truncated]"
        return text
    except Exception as e:
        return f"Failed to fetch page: {e}"
