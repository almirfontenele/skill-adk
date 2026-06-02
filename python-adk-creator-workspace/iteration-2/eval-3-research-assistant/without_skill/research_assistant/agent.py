"""Research Assistant agent powered by Google GenAI (Gemini)."""

from __future__ import annotations

import logging
from typing import Optional

from google import genai
from google.genai import types

from research_assistant.config import Config
from research_assistant import tools as tool_module

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """You are an expert research assistant. Your job is to help users
research topics thoroughly and accurately.

When given a research query you MUST:
1. Use the search_web tool to find relevant, up-to-date information.
2. If needed, use fetch_page_content to read the full content of promising pages.
3. Use summarize_text to condense long pages before including them in your answer.
4. Synthesize the gathered information into a clear, well-structured response.
5. Always cite your sources (URLs) at the end of your response.

Be thorough but concise. If you cannot find reliable information, say so honestly.
"""


class ResearchAssistant:
    """A conversational research agent with web search and summarization capabilities."""

    def __init__(self, config: Optional[Config] = None) -> None:
        self._config = config or Config()
        self._config.validate()

        # Inject tool-level configuration
        tool_module.configure(
            serpapi_key=self._config.serpapi_key,
            max_results=self._config.max_search_results,
        )

        # Build the GenAI client
        self._client = genai.Client(api_key=self._config.gemini_api_key)

        # Tools available to the model (automatic function calling)
        self._tools: list = [
            tool_module.search_web,
            tool_module.fetch_page_content,
            tool_module.summarize_text,
        ]

        # Conversation history (multi-turn)
        self._history: list[types.Content] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def research(self, query: str) -> str:
        """Run a research query and return the assistant's response.

        Supports multi-turn conversation — previous exchanges are included
        in the context automatically.

        Args:
            query: The user's research question or topic.

        Returns:
            The assistant's response as a plain string.
        """
        logger.info("Research query: %s", query)

        # Append the new user message to history
        self._history.append(
            types.Content(role="user", parts=[types.Part(text=query)])
        )

        response = self._client.models.generate_content(
            model=self._config.gemini_model,
            contents=self._history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=self._tools,
                temperature=0.2,
                max_output_tokens=4096,
            ),
        )

        answer = response.text or ""

        # Persist the model turn for future context
        self._history.append(
            types.Content(role="model", parts=[types.Part(text=answer)])
        )

        logger.info("Response length: %d chars", len(answer))
        return answer

    def reset(self) -> None:
        """Clear conversation history to start a fresh session."""
        self._history.clear()
        logger.info("Conversation history cleared.")

    def chat(self) -> None:
        """Start an interactive REPL session in the terminal."""
        print("Research Assistant (type 'exit' or 'quit' to stop, 'reset' to clear history)")
        print("-" * 70)
        while True:
            try:
                query = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if not query:
                continue
            if query.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            if query.lower() == "reset":
                self.reset()
                print("History cleared. Starting a new conversation.")
                continue

            print("\nAssistant: ", end="", flush=True)
            try:
                answer = self.research(query)
                print(answer)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Error during research")
                print(f"[Error] {exc}")
