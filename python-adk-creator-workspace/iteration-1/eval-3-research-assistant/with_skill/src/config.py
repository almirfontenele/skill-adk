"""Configuration and client setup for the Research Assistant."""

import os
from pathlib import Path

from dotenv import load_dotenv


def load_environment():
    """Load environment variables from .env file."""
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    else:
        # Try loading from parent directory
        load_dotenv()


def get_api_key() -> str:
    """Get the Google API key from environment variables.

    Returns:
        str: The Google API key

    Raises:
        ValueError: If GOOGLE_API_KEY is not set
    """
    load_environment()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment. "
            "Please set it in .env file or export as environment variable."
        )
    return api_key


def get_client():
    """Get an authenticated Google Generative AI client.

    Returns:
        google.genai.Client: Authenticated client instance
    """
    import google.genai as genai

    api_key = get_api_key()
    genai.configure(api_key=api_key)
    return genai
