"""Configuration management for the Calculator Bot"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the Calculator Bot application"""

    # API Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-2.5-flash")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = "calculator_bot.log"

    # Application Configuration
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30

    @classmethod
    def setup_logging(cls) -> None:
        """Configure logging for the application"""
        log_level = getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)

        # Create logger
        logger = logging.getLogger("calculator_bot")
        logger.setLevel(log_level)

        # Create formatters
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File handler
        file_handler = logging.FileHandler(cls.LOG_FILE)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set. "
                "Please set it in .env file or as an environment variable."
            )
        return True


# Initialize logger
logger = Config.setup_logging()
