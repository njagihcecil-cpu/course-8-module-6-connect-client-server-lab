from flask import Flask, jsonify, request
from flask_cors import CORS

from data import events

app = Flask(__name__)
CORS(app)


# ---------- helper functions ----------

def find_event_by_id(event_id):
    """Return the event dict matching event_id, or None if not found."""
    return next((e for e in events if e["id"] == event_id), None)


def next_id():
    """Generate the next available id for a new event."""
    return max((e["id"] for e in events), default=0) + 1


# ---------- routes ----------

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Event Catalog API!"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events), 200


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = find_event_by_id(event_id)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404
    return jsonify(event), 200


@app.route("/events", methods=["POST"])
def add_event():
    data = request.get_json(silent=True)

    if not data or not str(data.get("title", "")).strip():
        return jsonify({"error": "Field 'title' is required"}), 400

    new_event = {"id": next_id(), "title": data["title"].strip()}
    events.append(new_event)
    return jsonify(new_event), 201


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)