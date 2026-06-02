"""Tool definitions for web search and content summarization."""

from typing import Any, Optional

import requests
from bs4 import BeautifulSoup

from google.genai import types

from research_assistant.config import Config


class WebSearchTool:
    """Tool for searching the web using Google Custom Search API alternative."""

    def __init__(self, config: Config):
        """Initialize the web search tool.

        Args:
            config: Application configuration
        """
        self.config = config
        self.session = requests.Session()

    def search(self, query: str, num_results: Optional[int] = None) -> dict[str, Any]:
        """Search the web for a query.

        Args:
            query: The search query
            num_results: Maximum number of results to return

        Returns:
            Dictionary containing search results
        """
        if not query or not isinstance(query, str):
            return {"error": "Query must be a non-empty string", "results": []}

        num_results = num_results or self.config.MAX_SEARCH_RESULTS

        try:
            # Using DuckDuckGo-like approach with requests
            # In production, use actual search API (Google Custom Search, SerpAPI, etc.)
            results = self._perform_search(query, num_results)
            return {
                "query": query,
                "results": results,
                "count": len(results),
            }
        except Exception as e:
            return {"error": f"Search failed: {str(e)}", "results": []}

    def _perform_search(self, query: str, num_results: int) -> list[dict[str, Any]]:
        """Perform actual web search (placeholder implementation).

        In production, replace with:
        - Google Custom Search API
        - SerpAPI
        - Brave Search API
        - DuckDuckGo API
        """
        # Mock implementation returning sample results
        mock_results = [
            {
                "title": f"Result for '{query}'",
                "url": f"https://example.com/search?q={query}",
                "snippet": f"This is a search result for {query}. "
                "In production, this would be replaced with actual search results.",
            }
        ]
        return mock_results[:num_results]

    def get_function_declaration(self) -> types.FunctionDeclaration:
        """Get the function declaration for this tool."""
        return types.FunctionDeclaration(
            name="web_search",
            description="Search the web for information on a given topic",
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find information about",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)",
                    },
                },
                "required": ["query"],
            },
        )


class ContentSummarizerTool:
    """Tool for summarizing content."""

    def __init__(self, config: Config):
        """Initialize the content summarizer tool.

        Args:
            config: Application configuration
        """
        self.config = config
        self.session = requests.Session()

    def summarize(self, content: str, length: Optional[int] = None) -> dict[str, Any]:
        """Summarize content to a specified length.

        Args:
            content: The content to summarize
            length: Target summary length in words

        Returns:
            Dictionary containing the summary
        """
        if not content or not isinstance(content, str):
            return {"error": "Content must be a non-empty string", "summary": ""}

        length = length or self.config.SUMMARIZATION_LENGTH

        try:
            # Extract sentences and create summary
            sentences = [s.strip() for s in content.split(".") if s.strip()]

            if not sentences:
                return {"error": "No content to summarize", "summary": ""}

            # Calculate words per sentence to determine how many to keep
            total_words = sum(len(s.split()) for s in sentences)
            if total_words == 0:
                return {"error": "Content has no words", "summary": ""}

            words_per_sentence = total_words / len(sentences)
            num_sentences = max(1, int(length / words_per_sentence))

            # Select sentences (simple extractive summarization)
            summary_sentences = sentences[:num_sentences]
            summary = ". ".join(summary_sentences) + "."

            return {
                "original_length": total_words,
                "summary_length": len(summary.split()),
                "summary": summary,
                "sentence_count": len(summary_sentences),
            }
        except Exception as e:
            return {"error": f"Summarization failed: {str(e)}", "summary": ""}

    def get_function_declaration(self) -> types.FunctionDeclaration:
        """Get the function declaration for this tool."""
        return types.FunctionDeclaration(
            name="summarize_content",
            description="Summarize provided content to a specified length",
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content to summarize",
                    },
                    "length": {
                        "type": "integer",
                        "description": "Target summary length in words (default: 500)",
                    },
                },
                "required": ["content"],
            },
        )


class FetchPageTool:
    """Tool for fetching and extracting text from web pages."""

    def __init__(self, config: Config):
        """Initialize the page fetcher tool.

        Args:
            config: Application configuration
        """
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
            }
        )

    def fetch(self, url: str) -> dict[str, Any]:
        """Fetch and extract text from a web page.

        Args:
            url: The URL to fetch

        Returns:
            Dictionary containing extracted page content
        """
        if not url or not isinstance(url, str):
            return {"error": "URL must be a non-empty string", "content": ""}

        try:
            response = self.session.get(url, timeout=self.config.SEARCH_TIMEOUT)
            response.raise_for_status()

            # Parse HTML and extract text
            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            content = " ".join(chunk for chunk in chunks if chunk)

            return {
                "url": url,
                "content": content[:5000],  # Limit content size
                "length": len(content),
                "success": True,
            }
        except requests.RequestException as e:
            return {"error": f"Failed to fetch URL: {str(e)}", "content": ""}
        except Exception as e:
            return {"error": f"Failed to parse content: {str(e)}", "content": ""}

    def get_function_declaration(self) -> types.FunctionDeclaration:
        """Get the function declaration for this tool."""
        return types.FunctionDeclaration(
            name="fetch_page",
            description="Fetch and extract text content from a web page",
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the page to fetch",
                    },
                },
                "required": ["url"],
            },
        )


def get_tool_handlers() -> dict[str, Any]:
    """Get a mapping of tool names to their handler functions."""
    config = Config()

    search_tool = WebSearchTool(config)
    summarizer_tool = ContentSummarizerTool(config)
    fetch_tool = FetchPageTool(config)

    return {
        "web_search": search_tool.search,
        "summarize_content": summarizer_tool.summarize,
        "fetch_page": fetch_tool.fetch,
    }


def get_tool_definitions(config: Config) -> types.Tool:
    """Get all tool definitions for the agent.

    Args:
        config: Application configuration

    Returns:
        Tool object with all function declarations
    """
    search_tool = WebSearchTool(config)
    summarizer_tool = ContentSummarizerTool(config)
    fetch_tool = FetchPageTool(config)

    return types.Tool(
        function_declarations=[
            search_tool.get_function_declaration(),
            summarizer_tool.get_function_declaration(),
            fetch_tool.get_function_declaration(),
        ]
    )
