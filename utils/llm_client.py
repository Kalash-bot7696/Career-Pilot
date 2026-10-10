# utils/llm_client.py
# ---------------------------------------------------------------------------
# Centralised Groq LLM client.
# All agents call call_llm() from here — API key and model are set once.
# ---------------------------------------------------------------------------

import os
from groq import Groq
from dotenv import load_dotenv

# Load GROQ_API_KEY from the .env file in the project root
load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MODEL_NAME  = "qwen/qwen3.8-27b"       # Groq model identifier
MAX_TOKENS  = 900                       # Stay safely under 1000 OTPM free-tier limit

# ---------------------------------------------------------------------------
# Groq client (created once at import time)
# ---------------------------------------------------------------------------
def _get_client() -> Groq:
    """Return a Groq client, raising a clear error if the key is missing."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not found.  "
            "Please copy .env.example → .env and add your key."
        )
    return Groq(api_key=api_key)


# ---------------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------------
def call_llm(prompt: str, max_tokens: int = MAX_TOKENS) -> str:
    """
    Send *prompt* to the Groq chat-completion endpoint and return the
    assistant's reply as a plain string.

    Parameters
    ----------
    prompt     : The full user prompt to send.
    max_tokens : Maximum output tokens for this call (default 900).

    Returns
    -------
    str : The model's text response, or an error message prefixed with
          "⚠️ LLM Error:" so callers can surface it gracefully.
    """
    try:
        client   = _get_client()
        response = client.chat.completions.create(
            model      = MODEL_NAME,
            messages   = [{"role": "user", "content": prompt}],
            max_tokens = max_tokens,
        )
        return response.choices[0].message.content.strip()
    except EnvironmentError as env_err:
        return f"⚠️ LLM Error: {env_err}"
    except Exception as exc:
        return f"⚠️ LLM Error: {exc}"
