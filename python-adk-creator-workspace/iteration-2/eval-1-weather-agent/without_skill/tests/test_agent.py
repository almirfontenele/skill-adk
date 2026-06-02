"""Unit tests for WeatherAgent."""

import pytest
from unittest.mock import MagicMock, patch

from weather_agent.agent import WeatherAgent


@pytest.fixture()
def agent(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
    with patch("weather_agent.agent.genai.Client"):
        return WeatherAgent()


def test_agent_init_missing_key(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key"):
        WeatherAgent()


def test_agent_ask(agent):
    mock_response = MagicMock()
    mock_response.text = "It is sunny in London."
    agent._client.models.generate_content.return_value = mock_response

    answer = agent.ask("What is the weather in London?")
    assert answer == "It is sunny in London."
    agent._client.models.generate_content.assert_called_once()


def test_agent_chat(agent):
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Expect rain tomorrow in Paris."
    mock_chat.send_message.return_value = mock_response
    mock_chat.get_history.return_value = []
    agent._client.chats.create.return_value = mock_chat

    answer = agent.chat("What is the forecast for Paris?")
    assert answer == "Expect rain tomorrow in Paris."
    mock_chat.send_message.assert_called_once_with("What is the forecast for Paris?")


def test_agent_reset(agent):
    agent._history = [MagicMock()]
    agent.reset()
    assert agent._history == []
