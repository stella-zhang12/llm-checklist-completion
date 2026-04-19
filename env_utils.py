"""Environment utility helpers."""

import os

from pipeline_config import OPENAI_API_KEY_ALT_ENV, OPENAI_API_KEY_ENV


def get_openai_api_key():
    """Return OpenAI API key from supported environment variable names."""
    return os.getenv(OPENAI_API_KEY_ENV) or os.getenv(OPENAI_API_KEY_ALT_ENV)
