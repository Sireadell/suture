"""The model Suture uses to read failures and write fixes (Gemini, traced)."""
import neatlogs

from . import config, tracing

MODEL = config.get("SUTURE_MODEL", "gemini-flash-latest")

tracing.start()

from google import genai  # noqa: E402  (must come after tracing.start)

_client = neatlogs.wrap(genai.Client(api_key=config.get("GEMINI_API_KEY")))


def ask(prompt: str) -> str:
    response = _client.models.generate_content(model=MODEL, contents=prompt)
    return response.text or ""
