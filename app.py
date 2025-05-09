from flask import Flask, request, make_response
from datetime import datetime
import os
import json

app = Flask(__name__)

LOG_FILE = "audit.log"
REPORT_FILE = "reports.json"
VALID_TOKEN = "REVIEWER_SECRET_123"
FLAG = open("flag.txt").read().strip()

# Load reports from file
with open(REPORT_FILE) as f:
    REPORTS = json.load(f)

# Ensure audit log exists
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()


def log_request(endpoint):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.utcnow()}] {endpoint} requested\n")
        f.write(f"Query: {request.query_string.decode()}\n")
        f.write(f"Headers: {dict(request.headers)}\n\n")


@app.route("/")
def index():
    return "TrailSec Report Backend Service. Try /view_report?id=1 or /audit."


@app.route("/view_report")
def view_report():
    report_id = request.args.get("id", "")
    log_request("/view_report")

    if report_id in REPORTS:
        return REPORTS[report_id]
    return "No such report.", 404


@app.route("/audit")
def audit():
    token = request.headers.get("X-Reviewer-Token")
    if token != VALID_TOKEN:
        log_request("/audit")
        return "Access denied. This action will be reported.", 403

    response = make_response("Audit logs accessed.")
    response.headers["X-Flag"] = FLAG
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
