"""Starts neatlogs tracing. Must run before the model library is imported."""
import neatlogs

from . import config

_started = False


def start(workflow_name: str = "suture") -> None:
    global _started
    if _started:
        return
    neatlogs.init(
        api_key=config.get("NEATLOGS_API_KEY"),
        endpoint="https://ingest.neatlogs.com",
        workflow_name=workflow_name,
    )
    _started = True


def stop() -> None:
    if _started:
        neatlogs.flush()
        neatlogs.shutdown()
