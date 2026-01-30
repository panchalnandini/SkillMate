from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)
CORS(app)

# ==========================================
# 🧠 1. AI MODEL SETUP (Trains on Startup)
# ==========================================

# Initial training data for the demo
# Features: [Skill Match (0-1), Availability (0-1), Trust Score (0-1)]
X_train = [
    [1.0, 1.0, 0.9], # Perfect match
    [0.9, 0.8, 0.8], # Good match
    [0.3, 0.4, 0.2], # Bad match
    [0.6, 0.7, 0.6], # Average match
    [0.2, 0.3, 0.4], # Bad match
]

# Labels: 1 = Success, 0 = Fail
y_train = [1, 1, 0, 1, 0]

print("⏳ Training Matchmaking Model...")
model = LogisticRegression()
model.fit(X_train, y_train)
print("✅ AI Model Trained & Ready!")


# ==========================================
# 🔌 2. API ROUTES
# ==========================================

# ---------------- ROOT ----------------
@app.route("/messages/get", methods=["GET"])
def get_messages():
    return jsonify([
        {"sender": "Ruhi", "receiver": "Rohan", "message": "Hi!", "time": "10:42 AM"},
        {"sender": "Rohan", "receiver": "Ruhi", "message": "Hello!", "time": "10:44 AM"}
    ])

@app.route("/messages/send", methods=["POST"])
def send_message():
    data = request.json
    print("Received:", data)
    return jsonify({"status": "ok"})


# ---------------- FAKE USERS ----------------
USERS = {
    "rohansharma88@gmail.com": {
        "password": "123456",
        "role": "learner"
    }
}

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = USERS.get(email)

    if not user or user["password"] != password:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "token": "skillswap-demo-token",
        "email": email,
        "role": user["role"]
    })

# ---------------- TOKEN CHECK ----------------
def check_token(req):
    token = req.headers.get("Authorization")
    return token == "skillswap-demo-token"

# ---------------- SUPPORT CHAT ----------------
def support_chat_logic(user_id, message):
    return f"Hello {user_id}, support received: {message}"

@app.route("/support-chat", methods=["POST"])
def support_chat_route():
    data = request.get_json()
    user_id = data.get("user_id", "guest")
    message = data.get("message", "")
    reply = support_chat_logic(user_id, message)
    return jsonify({"reply": reply})


# ---------------- AI MATCHMAKING (NEW!) ----------------
# This is the endpoint your "Match Engine" HTML will call
@app.route('/predict_match', methods=['POST'])
def predict_match():
    try:
        data = request.json
        
        # 1. Get features from frontend
        skill = float(data.get('skill_match', 0))
        avail = float(data.get('availability', 0))
        trust = float(data.get('trust_score', 0))

        # 2. Prepare for AI Model
        features = np.array([[skill, avail, trust]])

        # 3. Predict Probability (index [0][1] is the success %)
        probability = model.predict_proba(features)[0][1]
        
        # 4. Format as percentage
        match_percentage = round(probability * 100, 1)

        print(f"🔮 AI Prediction: Inputs({skill}, {avail}, {trust}) -> {match_percentage}%")

        return jsonify({
            "status": "success",
            "match_percentage": match_percentage
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# ---------------- MATCH SKILLS (Old/Simple) ----------------
@app.route("/match", methods=["GET"])
def match_skills():
    if not check_token(request):
        return jsonify({"message": "Unauthorized"}), 403

    return jsonify([
        {"name": "Amit", "skill": "React"},
        {"name": "Sara", "skill": "UI/UX"}
    ])


# ---------------- AI CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat_ai():
    if not check_token(request):
        return jsonify({"message": "Unauthorized"}), 403

    user_msg = request.get_json().get("message")
    return jsonify({
        "reply": f"AI response to: {user_msg}"
    })


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)