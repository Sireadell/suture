# neatlogs Investigate result for Ward (copied from the neatlogs chat, 2026-10-11 about 19:10)

Chat: https://app.neatlogs.com/ai-search/53fcf458-64b7-4a29-927e-0c9873df9188
Prompt given: Look into the workflow ward: detection "Ward unreadable request answered" flagged traces such as 78e36935e382072a0c9fc9cd36b06ee2 (cut-off body answered with previous patient's list, status OK). Find the cause in the code and raise an incident.

Incident raised by neatlogs: "Ward workflow leaks previous patient medication records on malformed JSON request body", severity CRITICAL, type Bug, status Open.

Cause (neatlogs): in targets/ward/app.py, handle() falls back to LAST_PATIENT["id"] when json.loads fails (data = {}), so a cut-off body is answered with the previous patient's medication list, status 200.

Recommended fix (neatlogs): remove the LAST_PATIENT["id"] fallback entirely. If raw_body is invalid JSON or has no valid patient_id, reject immediately with HTTP 400 Bad Request.
