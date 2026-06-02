"""Tests for tool implementations."""

import pytest

from research_assistant.config import Config
from research_assistant.tools import (
    WebSearchTool,
    ContentSummarizerTool,
    FetchPageTool,
)


class TestWebSearchTool:
    """Tests for WebSearchTool."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()
        self.tool = WebSearchTool(self.config)

    def test_search_with_valid_query(self):
        """Test search with valid query."""
        result = self.tool.search("python programming")
        assert "results" in result
        assert "query" in result
        assert result["query"] == "python programming"

    def test_search_with_empty_query(self):
        """Test search with empty query."""
        result = self.tool.search("")
        assert "error" in result
        assert result["results"] == []

    def test_search_with_none_query(self):
        """Test search with None query."""
        result = self.tool.search(None)
        assert "error" in result
        assert result["results"] == []

    def test_search_with_custom_num_results(self):
        """Test search with custom number of results."""
        result = self.tool.search("python", num_results=3)
        assert len(result["results"]) <= 3

    def test_get_function_declaration(self):
        """Test function declaration generation."""
        declaration = self.tool.get_function_declaration()
        assert declaration.name == "web_search"
        assert "query" in declaration.parameters_json_schema["properties"]


class TestContentSummarizerTool:
    """Tests for ContentSummarizerTool."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()
        self.tool = ContentSummarizerTool(self.config)

    def test_summarize_with_valid_content(self):
        """Test summarization with valid content."""
        content = (
            "This is a test. It contains multiple sentences. "
            "Each sentence has words. This tests summarization."
        )
        result = self.tool.summarize(content)
        assert "summary" in result
        assert len(result["summary"]) > 0
        assert result["original_length"] > 0

    def test_summarize_with_empty_content(self):
        """Test summarization with empty content."""
        result = self.tool.summarize("")
        assert "error" in result
        assert result["summary"] == ""

    def test_summarize_with_custom_length(self):
        """Test summarization with custom length."""
        content = "Word. " * 20
        result = self.tool.summarize(content, length=10)
        assert "summary" in result
        assert "original_length" in result

    def test_get_function_declaration(self):
        """Test function declaration generation."""
        declaration = self.tool.get_function_declaration()
        assert declaration.name == "summarize_content"
        assert "content" in declaration.parameters_json_schema["properties"]


class TestFetchPageTool:
    """Tests for FetchPageTool."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()
        self.tool = FetchPageTool(self.config)

    def test_fetch_with_empty_url(self):
        """Test fetch with empty URL."""
        result = self.tool.fetch("")
        assert "error" in result
        assert result["content"] == ""

    def test_fetch_with_none_url(self):
        """Test fetch with None URL."""
        result = self.tool.fetch(None)
        assert "error" in result
        assert result["content"] == ""

    def test_get_function_declaration(self):
        """Test function declaration generation."""
        declaration = self.tool.get_function_declaration()
        assert declaration.name == "fetch_page"
        assert "url" in declaration.parameters_json_schema["properties"]
