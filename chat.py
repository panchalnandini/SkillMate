# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # ---------------- DEMO TOKEN ----------------
# DEMO_TOKEN = "skillswap-demo-token"

# def check_token(req):
#     return req.headers.get("Authorization") == DEMO_TOKEN


# # ---------------- IN-MEMORY CHAT STORAGE ----------------
# # structure:
# # [
# #   { sender, receiver, message }
# # ]
# MESSAGES = []


# # ---------------- ROOT ----------------
# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({"status": "SkillMate Chat Backend Running 🚀"})


# # ---------------- SEND MESSAGE ----------------
# @app.route("/messages/send", methods=["POST"])
# def send_message():
#     if not check_token(request):
#         return jsonify({"error": "Unauthorized"}), 403

#     data = request.get_json()

#     sender = data.get("sender")
#     receiver = data.get("receiver")
#     message = data.get("message")

#     if not sender or not receiver or not message:
#         return jsonify({"error": "Missing fields"}), 400

#     MESSAGES.append({
#         "sender": sender,
#         "receiver": receiver,
#         "message": message
#     })

#     return jsonify({"status": "Message sent"}), 200


# # ---------------- GET MESSAGES ----------------
# @app.route("/messages/get", methods=["GET"])
# def get_messages():
#     if not check_token(request):
#         return jsonify({"error": "Unauthorized"}), 403

#     return jsonify(MESSAGES), 200


# # ---------------- RUN SERVER ----------------
# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime  # ← add this

app = Flask(__name__)
CORS(app)

DEMO_TOKEN = "skillswap-demo-token"
MESSAGES = []

def check_token(req):
    return req.headers.get("Authorization") == DEMO_TOKEN


@app.route("/messages/send", methods=["POST"])
def send_message():
    if not check_token(request):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    sender = data.get("sender")
    receiver = data.get("receiver")
    message = data.get("message")

    if not sender or not receiver or not message:
        return jsonify({"error": "Missing fields"}), 400

    # Add timestamp
    MESSAGES.append({
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "timestamp": datetime.now().strftime("%I:%M %p")  # e.g., 10:45 AM
    })

    return jsonify({"status": "Message sent"}), 200


@app.route("/messages/get", methods=["GET"])
def get_messages():
    if not check_token(request):
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(MESSAGES), 200


if __name__ == "__main__":
    app.run(debug=True)
