"""One traced model call, to confirm tracing and the model both work."""
import neatlogs

from . import tracing
from .llm import ask


@neatlogs.span(kind="WORKFLOW")
def run() -> str:
    return ask("Reply with one short sentence: what does a surgical suture do?")


if __name__ == "__main__":
    print(run())
    tracing.stop()
