import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key() -> str:
    """Load and return the Google API key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set. Add it to your .env file.")
    return api_key
