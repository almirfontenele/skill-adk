"""Command-line interface for the Research Assistant."""

from __future__ import annotations

import argparse
import logging
import sys

from research_assistant.agent import ResearchAssistant
from research_assistant.config import Config


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="research-assistant",
        description="AI-powered research assistant with web search and summarization.",
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Research query to answer. If omitted, starts an interactive session.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Gemini model ID to use (overrides GEMINI_MODEL env var).",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=None,
        help="Maximum number of web search results (overrides MAX_SEARCH_RESULTS).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable debug logging.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    config = Config()
    if args.model:
        config.gemini_model = args.model
    if args.max_results:
        config.max_search_results = args.max_results

    try:
        config.validate()
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    assistant = ResearchAssistant(config)

    if args.query:
        # Single-shot mode
        try:
            answer = assistant.research(args.query)
            print(answer)
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    else:
        # Interactive chat mode
        assistant.chat()

    return 0


if __name__ == "__main__":
    sys.exit(main())
