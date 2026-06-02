"""Core tools for the Research Assistant.

This module provides web search and content summarization capabilities
for the Gemini-powered research assistant.
"""

import re
from typing import Optional

import requests


def search_web(query: str, max_results: int = 5) -> str:
    """Search the web for information about a given query.

    This tool performs a web search and returns relevant results with titles,
    URLs, and snippets. You can use this to gather information on any topic.

    Args:
        query: The search query (e.g., "climate change 2024", "AI trends")
        max_results: Maximum number of results to return (default: 5, max: 10)

    Returns:
        str: Formatted search results with titles, URLs, and snippets
    """
    if max_results > 10:
        max_results = 10

    try:
        # Using a simple search approach - in production, integrate with
        # a real search API (Google Search API, DuckDuckGo API, etc.)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # Simulate search results for demonstration
        # In production, replace with actual API call
        search_results = _simulate_search_results(query, max_results)

        return search_results

    except Exception as e:
        return f"Error performing search: {str(e)}"


def summarize_content(content: str, max_length: int = 200) -> str:
    """Summarize the provided content into a concise summary.

    This tool takes a text passage and distills it into a shorter summary,
    preserving the key information and main ideas.

    Args:
        content: The text content to summarize
        max_length: Maximum length of the summary in characters (default: 200)

    Returns:
        str: A concise summary of the content
    """
    try:
        if not content or len(content.strip()) == 0:
            return "No content provided to summarize."

        # Clean the content
        content = content.strip()

        # If content is shorter than max_length, return as-is
        if len(content) <= max_length:
            return content

        # Simple extractive summarization by sentence selection
        sentences = re.split(r'(?<=[.!?])\s+', content)

        summary_sentences = []
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if adding this sentence would exceed max_length
            test_length = current_length + len(sentence) + 1
            if test_length <= max_length:
                summary_sentences.append(sentence)
                current_length = test_length
            else:
                break

        summary = " ".join(summary_sentences)

        if not summary:
            # If no complete sentences fit, truncate with ellipsis
            summary = content[:max_length].rsplit(' ', 1)[0] + "..."

        return summary

    except Exception as e:
        return f"Error summarizing content: {str(e)}"


def _simulate_search_results(query: str, num_results: int) -> str:
    """Simulate web search results for demonstration.

    In a production system, this would call a real search API.

    Args:
        query: The search query
        num_results: Number of results to return

    Returns:
        str: Formatted search results
    """
    # Simulated results for demonstration
    sample_results = {
        "python": [
            {
                "title": "Python Official Website",
                "url": "https://www.python.org",
                "snippet": "Official Python programming language website with documentation, downloads, and community resources.",
            },
            {
                "title": "Python Documentation",
                "url": "https://docs.python.org",
                "snippet": "Complete Python language reference and library documentation.",
            },
        ],
        "ai": [
            {
                "title": "Artificial Intelligence - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
                "snippet": "Artificial intelligence (AI) is intelligence demonstrated by machines.",
            },
            {
                "title": "AI Research Papers",
                "url": "https://arxiv.org/list/cs.AI/recent",
                "snippet": "Recent research papers in artificial intelligence.",
            },
        ],
        "research": [
            {
                "title": "Research Methods Guide",
                "url": "https://www.example.com/research",
                "snippet": "Comprehensive guide to academic research methodologies.",
            },
        ],
    }

    # Return sample results or generic results
    results = []
    for i in range(num_results):
        keyword = None
        for key in sample_results.keys():
            if key.lower() in query.lower():
                keyword = key
                break

        if keyword and sample_results[keyword]:
            result = sample_results[keyword][i % len(sample_results[keyword])]
        else:
            result = {
                "title": f"Search Result {i + 1}: {query}",
                "url": f"https://www.example.com/result-{i+1}",
                "snippet": f"This is a sample search result for '{query}'.",
            }

        results.append(
            f"{i + 1}. {result['title']}\n   URL: {result['url']}\n   {result['snippet']}"
        )

    return "\n\n".join(results)
