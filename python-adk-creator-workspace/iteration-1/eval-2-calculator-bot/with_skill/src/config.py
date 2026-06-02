"""Configuration module for the Calculator Bot.

Handles environment setup and API client initialization.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_api_key() -> str:
    """
    Retrieve the Google API key from environment variables.

    Returns:
        str: The Google API key

    Raises:
        ValueError: If GOOGLE_API_KEY is not set in the environment
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment. "
            "Please set it in your .env file or export it as an environment variable."
        )
    return api_key


def get_client():
    """
    Initialize and return a Google Generative AI client.

    Returns:
        google.genai.Client: The configured API client
    """
    try:
        import google.genai as genai
    except ImportError:
        raise ImportError(
            "google-genai is not installed. "
            "Please run: pip install -r requirements.txt"
        )

    api_key = get_api_key()
    return genai.Client(api_key=api_key)


# Model configuration
MODEL_ID = "gemini-2.5-flash"
