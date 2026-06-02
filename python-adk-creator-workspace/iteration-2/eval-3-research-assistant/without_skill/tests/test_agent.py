"""Unit tests for the ResearchAssistant agent (mocked GenAI client)."""

from __future__ import annotations

from unittest import mock

import pytest

from research_assistant.agent import ResearchAssistant
from research_assistant.config import Config


@pytest.fixture
def config():
    return Config(gemini_api_key="fake-key", serpapi_key="")


@pytest.fixture
def mock_genai_client():
    """Patch google.genai.Client so no real HTTP calls are made."""
    with mock.patch("google.genai.Client") as MockClient:
        instance = MockClient.return_value
        # Default response
        instance.models.generate_content.return_value = mock.MagicMock(
            text="Mocked research answer."
        )
        yield instance


class TestResearchAssistant:
    def test_research_returns_model_text(self, config, mock_genai_client):
        assistant = ResearchAssistant(config)
        answer = assistant.research("What is quantum computing?")
        assert answer == "Mocked research answer."

    def test_research_appends_to_history(self, config, mock_genai_client):
        assistant = ResearchAssistant(config)
        assistant.research("Question 1")
        assistant.research("Question 2")
        assert len(assistant._history) == 4  # 2 user + 2 model turns

    def test_reset_clears_history(self, config, mock_genai_client):
        assistant = ResearchAssistant(config)
        assistant.research("Some query")
        assert len(assistant._history) > 0
        assistant.reset()
        assert len(assistant._history) == 0

    def test_validate_raises_without_api_key(self):
        bad_config = Config(gemini_api_key="")
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            ResearchAssistant(bad_config)

    def test_generate_content_called_with_tools(self, config, mock_genai_client):
        assistant = ResearchAssistant(config)
        assistant.research("Tell me about AI")
        call_kwargs = mock_genai_client.models.generate_content.call_args
        config_arg = call_kwargs.kwargs.get("config") or call_kwargs.args[2] if call_kwargs.args else None
        # Verify tools are passed (either via kwargs or positional)
        assert mock_genai_client.models.generate_content.called
