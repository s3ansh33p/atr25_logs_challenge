from flask import Flask, request, jsonify
import json
import re
import os

app = Flask(__name__)

REPORT_FILE = "reports.json"
VALID_TOKEN = "ADMIN_TOKEN"
DATA_FILE = "data.json"

with open(REPORT_FILE) as f:
    REPORTS = json.load(f)

@app.route("/")
def index():
    return "TrailSec Report Backend Service. Try /view_report?id=1."

@app.route("/view_report")
def view_report():
    report_id = request.args.get("id", "")

    if report_id in REPORTS:
        return REPORTS[report_id]
    return "No such report.", 404

@app.route("/matches", methods=["GET"])
def matches():
    """
    Allows users to perform regex matching against the data.json file.
    """
    token = request.args.get("token", "")
    if token != VALID_TOKEN:
        return jsonify({"error": "Invalid token."}), 403
    try:
        # Load data from data.json
        if not os.path.exists(DATA_FILE):
            return jsonify({"error": "Data file not found."}), 500

        with open(DATA_FILE) as f:
            data = json.load(f)

        # Get the regex pattern from the request
        pattern = request.args.get("pattern", "")
        if not pattern:
            return jsonify({"error": "Missing regex pattern."}), 400

        # Attempt to compile the regex pattern
        try:
            compiled_pattern = re.compile(pattern)
        except re.error:
            return jsonify({"error": "Invalid regex pattern."}), 400

        # Perform regex matching on the data
        matches = [item for item in data if compiled_pattern.search(item)]

        # Return the number of matches
        return jsonify({"matches": len(matches)})

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
