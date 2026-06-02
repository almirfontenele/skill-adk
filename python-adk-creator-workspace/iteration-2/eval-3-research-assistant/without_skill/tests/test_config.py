"""Unit tests for Config."""

import os
from unittest import mock

import pytest

from research_assistant.config import Config


class TestConfig:
    def test_defaults(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            cfg = Config()
        assert cfg.gemini_model == "gemini-2.5-flash"
        assert cfg.max_search_results == 5
        assert cfg.summary_max_words == 300

    def test_env_vars_override_defaults(self):
        env = {
            "GEMINI_API_KEY": "my-key",
            "GEMINI_MODEL": "gemini-2.0-pro",
            "MAX_SEARCH_RESULTS": "10",
            "SUMMARY_MAX_WORDS": "150",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            cfg = Config()
        assert cfg.gemini_api_key == "my-key"
        assert cfg.gemini_model == "gemini-2.0-pro"
        assert cfg.max_search_results == 10
        assert cfg.summary_max_words == 150

    def test_validate_raises_without_key(self):
        cfg = Config(gemini_api_key="")
        with pytest.raises(ValueError):
            cfg.validate()

    def test_validate_passes_with_key(self):
        cfg = Config(gemini_api_key="valid-key")
        cfg.validate()  # should not raise
