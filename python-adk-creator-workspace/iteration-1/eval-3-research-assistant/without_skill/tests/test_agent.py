"""Tests for agent implementation."""

import pytest

from research_assistant.agent import ResearchAgent
from research_assistant.config import Config


class TestResearchAgent:
    """Tests for ResearchAgent."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()

    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = ResearchAgent(self.config)
        assert agent.config is not None
        assert agent.client is not None
        assert agent.tools is not None
        assert agent.tool_handlers is not None

    def test_agent_with_default_config(self):
        """Test agent initialization with default config."""
        agent = ResearchAgent()
        assert agent.config is not None

    def test_tool_handlers_available(self):
        """Test that tool handlers are available."""
        agent = ResearchAgent(self.config)
        assert "web_search" in agent.tool_handlers
        assert "summarize_content" in agent.tool_handlers
        assert "fetch_page" in agent.tool_handlers

    def test_execute_tool_with_unknown_tool(self):
        """Test executing unknown tool."""
        agent = ResearchAgent(self.config)
        result = agent._execute_tool("unknown_tool", {})
        assert "error" in result
        assert "Unknown tool" in result["error"]

    def test_execute_tool_with_error(self):
        """Test executing tool that raises error."""
        agent = ResearchAgent(self.config)
        # Calling tool with invalid args should handle gracefully
        result = agent._execute_tool("web_search", {"invalid_arg": "value"})
        # Should return error or empty results
        assert "error" in result or "results" in result
