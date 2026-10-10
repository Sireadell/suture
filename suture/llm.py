"""The model Suture uses to read failures and write fixes (Gemini, traced)."""
import time

import neatlogs

from . import config, tracing

MODEL = config.get("SUTURE_MODEL", "gemini-flash-latest")

tracing.start()

from google import genai  # noqa: E402  (must come after tracing.start)

_client = neatlogs.wrap(genai.Client(api_key=config.get("GEMINI_API_KEY")))


USAGE = {"input_tokens": 0, "output_tokens": 0, "calls": 0}


def ask(prompt: str) -> str:
    response = None
    for attempt in range(6):  # the model is sometimes busy (503); wait and try again
        try:
            response = _client.models.generate_content(model=MODEL, contents=prompt)
            break
        except Exception as err:
            if "503" not in str(err) and "429" not in str(err) or attempt == 5:
                raise
            time.sleep(15 * (attempt + 1))
    meta = getattr(response, "usage_metadata", None)
    if meta:
        USAGE["input_tokens"] += getattr(meta, "prompt_token_count", 0) or 0
        USAGE["output_tokens"] += (getattr(meta, "candidates_token_count", 0) or 0) + (
            getattr(meta, "thoughts_token_count", 0) or 0
        )
    USAGE["calls"] += 1
    return response.text or ""
