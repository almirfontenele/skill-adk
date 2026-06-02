"""Unit tests for research_assistant.tools (no network calls, no API key needed)."""

from __future__ import annotations

import json
from unittest import mock

import pytest

from research_assistant import tools as tool_module


@pytest.fixture(autouse=True)
def reset_config():
    """Reset tool module globals before each test."""
    tool_module.configure(serpapi_key="", max_results=5)
    yield


# ---------------------------------------------------------------------------
# summarize_text
# ---------------------------------------------------------------------------

class TestSummarizeText:
    def test_returns_empty_message_for_blank_input(self):
        assert tool_module.summarize_text("") == "No content to summarize."
        assert tool_module.summarize_text("   ") == "No content to summarize."

    def test_respects_max_words(self):
        long_text = " ".join(["word"] * 500)
        result = tool_module.summarize_text(long_text, max_words=50)
        assert len(result.split()) <= 55  # small buffer for sentence boundary

    def test_focus_moves_relevant_sentences_first(self):
        text = (
            "The sky is blue and clear today. "
            "Python is a popular programming language for data science. "
            "Scientists discovered water on Mars last year."
        )
        result = tool_module.summarize_text(text, focus="Python programming")
        # The Python sentence should appear before the unrelated ones
        assert result.index("Python") < result.index("Mars")

    def test_short_text_returned_unchanged(self):
        text = "This is a short text."
        result = tool_module.summarize_text(text, max_words=300)
        assert text in result


# ---------------------------------------------------------------------------
# fetch_page_content
# ---------------------------------------------------------------------------

class TestFetchPageContent:
    def test_strips_html_tags(self):
        html = b"<html><body><h1>Hello</h1><p>World</p></body></html>"
        mock_resp = mock.MagicMock()
        mock_resp.read.return_value = html
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = mock.Mock(return_value=False)

        with mock.patch("urllib.request.urlopen", return_value=mock_resp):
            result = tool_module.fetch_page_content("https://example.com")

        assert "<h1>" not in result
        assert "Hello" in result
        assert "World" in result

    def test_returns_error_string_on_exception(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("timeout")):
            result = tool_module.fetch_page_content("https://example.com")
        assert "Error" in result


# ---------------------------------------------------------------------------
# search_web — DuckDuckGo fallback (no key)
# ---------------------------------------------------------------------------

class TestSearchWebDuckDuckGo:
    def _mock_ddg_response(self, abstract_text="AI is cool.", abstract_url="https://example.com"):
        payload = {
            "AbstractText": abstract_text,
            "AbstractURL": abstract_url,
            "Heading": "Artificial Intelligence",
            "RelatedTopics": [
                {"Text": "Machine learning topic text here.", "FirstURL": "https://example.com/ml"},
            ],
        }
        raw = json.dumps(payload).encode()
        mock_resp = mock.MagicMock()
        mock_resp.read.return_value = raw
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = mock.Mock(return_value=False)
        return mock_resp

    def test_returns_json_list(self):
        with mock.patch("urllib.request.urlopen", return_value=self._mock_ddg_response()):
            result = tool_module.search_web("artificial intelligence")
        parsed = json.loads(result)
        assert isinstance(parsed, list)
        assert len(parsed) >= 1

    def test_result_has_expected_keys(self):
        with mock.patch("urllib.request.urlopen", return_value=self._mock_ddg_response()):
            result = tool_module.search_web("AI")
        items = json.loads(result)
        for item in items:
            assert "title" in item
            assert "link" in item
            assert "snippet" in item

    def test_error_on_network_failure(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("network down")):
            result = tool_module.search_web("anything")
        parsed = json.loads(result)
        assert "error" in parsed


# ---------------------------------------------------------------------------
# search_web — SerpAPI path
# ---------------------------------------------------------------------------

class TestSearchWebSerpAPI:
    def setup_method(self):
        tool_module.configure(serpapi_key="fake-key", max_results=3)

    def _mock_serpapi_response(self):
        payload = {
            "organic_results": [
                {"title": "Result 1", "link": "https://r1.com", "snippet": "Snippet 1"},
                {"title": "Result 2", "link": "https://r2.com", "snippet": "Snippet 2"},
            ]
        }
        raw = json.dumps(payload).encode()
        mock_resp = mock.MagicMock()
        mock_resp.read.return_value = raw
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = mock.Mock(return_value=False)
        return mock_resp

    def test_returns_organic_results(self):
        with mock.patch("urllib.request.urlopen", return_value=self._mock_serpapi_response()):
            result = tool_module.search_web("python genai")
        items = json.loads(result)
        assert len(items) == 2
        assert items[0]["title"] == "Result 1"
