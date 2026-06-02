"""Configuration and client setup for the Weather Agent."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_api_key() -> str:
    """
    Retrieve the Google API key from environment variables.

    Returns:
        str: The Google API key.

    Raises:
        ValueError: If GOOGLE_API_KEY is not set in the environment.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables. "
            "Please set it in your .env file or as an environment variable."
        )
    return api_key


def get_client():
    """
    Initialize and return a Google Generative AI client.

    Returns:
        google.genai.Client: Configured client instance.
    """
    from google import genai

    api_key = get_api_key()
    return genai.Client(api_key=api_key)
