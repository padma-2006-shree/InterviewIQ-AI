import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Create a shared client instance if API key is present
client = None
if API_KEY and not API_KEY.startswith("your_"):
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL
        )
    except Exception:
        client = None


def get_openrouter_client():
    """Returns the OpenAI client configured for OpenRouter, or None if not configured."""
    global client
    if client is not None:
        return client

    curr_key = os.getenv("OPENROUTER_API_KEY", "")
    if curr_key and not curr_key.startswith("your_"):
        try:
            client = OpenAI(
                api_key=curr_key,
                base_url=BASE_URL
            )
            return client
        except Exception:
            return None
    return None
