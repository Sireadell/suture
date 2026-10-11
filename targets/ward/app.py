"""Ward: a DEMO clinic assistant. FAKE PATIENTS ONLY, no real people and no real medical data.
A nurse sends a patient id and Ward answers with that patient's medication list. This is the
first draft, written the way a quick first version usually is, and it is the agent Suture is
pointed at in the Ward demo. Do not use it for anything real."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import neatlogs

TRACING = bool(os.environ.get("NEATLOGS_API_KEY"))
if TRACING:
    neatlogs.init(
        api_key=os.environ["NEATLOGS_API_KEY"],
        endpoint="https://ingest.neatlogs.com",
        workflow_name="ward",
    )

# Invented patients and invented medicines for the demo.
PATIENTS = {
    "P-1001": {"label": "Demo patient 1", "medications": [
        {"name": "Metformin", "dose": "500 mg twice a day"},
        {"name": "Lisinopril", "dose": "10 mg once a day"},
    ]},
    "P-1002": {"label": "Demo patient 2", "medications": [
        {"name": "Levothyroxine", "dose": "75 mcg every morning"},
    ]},
    "P-1003": {"label": "Demo patient 3", "medications": [
        {"name": "Warfarin", "dose": "5 mg every evening"},
        {"name": "Atorvastatin", "dose": "20 mg at night"},
        {"name": "Omeprazole", "dose": "20 mg before breakfast"},
    ]},
}


@neatlogs.span(kind="TOOL", tool_name="lookup_medications")
def lookup_medications(patient_id):
    return PATIENTS.get(patient_id)


@neatlogs.span(kind="TOOL", tool_name="write_answer")
def write_answer(patient_id, patient):
    names = ", ".join(f"{m['name']} {m['dose']}" for m in patient["medications"])
    return f"{patient['label']} ({patient_id}) takes: {names}."


@neatlogs.span(kind="WORKFLOW")
def handle(raw_body):
    try:
        data = json.loads(raw_body)
    except Exception:
        raise ValueError("request body is not readable JSON")
    patient_id = data.get("patient_id") if isinstance(data, dict) else None
    if not isinstance(patient_id, str) or not patient_id:
        raise ValueError("request body has no patient_id")
    patient = lookup_medications(patient_id)
    if patient is None:
        raise LookupError(f"unknown patient {patient_id!r}")
    return {
        "patient_id": patient_id,
        "medications": patient["medications"],
        "answer": write_answer(patient_id, patient),
        "demo": "fake patients, demo data only",
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"agent": "ward", "status": "ok", "demo": "fake patients, demo data only"})

    def do_POST(self):
        length = int(self.headers.get("content-length") or 0)
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        try:
            self._send(200, handle(raw))
        except ValueError as err:
            self._send(400, {"error": str(err)})
        except LookupError as err:
            self._send(404, {"error": str(err)})

    def log_message(self, *args):
        pass


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    finally:
        if TRACING:
            neatlogs.flush()
            neatlogs.shutdown()


if __name__ == "__main__":
    main()
