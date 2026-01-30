from ml_match_ai import predict_match_quality
from ml_match_ai import predict_match_quality, retrain_model


# STEP 1: Sample Users (Fake Data)
users = [
    {
        "id": 1,
        "name": "Bhavya",
        "skills_offered": ["DSA", "C", "Problem Solving"],
        "skills_wanted": ["Python", "AI"],
        "availability": ["Sat", "Sun"],
        "rating": 4.6
    },
    {
        "id": 2,
        "name": "Ankit",
        "skills_offered": ["Python", "AI"],
        "skills_wanted": ["DSA"],
        "availability": ["Sat"],
        "rating": 4.4
    }
]

# STEP 2: Skill Similarity
def skill_similarity(wanted, offered):
    matched = set(wanted) & set(offered)
    return len(matched) / max(len(wanted), 1)



def generate_ai_explanation(user, candidate, reason):
    explanation = []

    if reason["skill_match"] > 0.7:
        explanation.append("Strong skill compatibility")
    elif reason["skill_match"] > 0.3:
        explanation.append("Moderate skill compatibility")

    if reason["availability_match"] > 0.5:
        explanation.append("Good availability overlap")

    if reason["trust_score"] > 0.8:
        explanation.append("Highly trusted user")

    return explanation


# STEP 3: Mutual Skill Swap Check
def is_mutual_swap(user_a, user_b):
    return (
        set(user_a["skills_wanted"]) & set(user_b["skills_offered"])
        and
        set(user_b["skills_wanted"]) & set(user_a["skills_offered"])
    )

# STEP 4: Availability Match
def availability_score(a, b):
    overlap = set(a) & set(b)
    return len(overlap) / max(len(a), 1)

# STEP 5: Final Match Score
def calculate_match_score(user, candidate):
    skill = skill_similarity(user["skills_wanted"], candidate["skills_offered"])
    time = availability_score(user["availability"], candidate["availability"])
    trust = candidate["rating"] / 5

    final_score = predict_match_quality(skill, time, trust)


    return final_score, {
        "skill_match": skill,
        "availability_match": time,
        "trust_score": trust
    }

# STEP 6: Match Engine
def find_matches(current_user, all_users):
    matches = []

    for u in all_users:
        if u["id"] == current_user["id"]:
            continue

        if is_mutual_swap(current_user, u):
            score, reason = calculate_match_score(current_user, u)
            matches.append({
    "name": u["name"],
    "score": score,
    "reason": reason,
    "ai_explanation": generate_ai_explanation(current_user, u, reason)
})



    return sorted(matches, key=lambda x: x["score"], reverse=True)

# STEP 7: RUN AI
current_user = users[0]
results = find_matches(current_user, users)

print("\n=== SKILL SWAP AI RESULTS ===")
for r in results:
    print(f"\n🤖 Matched with: {r['name']}")
    print(f"AI Score: {r['score']}")
    print("AI Reasoning:")

    for text in r["ai_explanation"]:
        print(" -", text)

    print("Detailed Scores:")
    for k, v in r["reason"].items():
        print(f"   {k}: {round(v,2)}")

    

def update_trust_score(user, session_rating):
    """
    Updates trust score using simple moving average logic
    """
    old_rating = user["rating"]
    new_rating = round((old_rating + session_rating) / 2, 2)
    user["rating"] = new_rating


    print("\n=== SESSION FEEDBACK ===")

# Simulate user giving feedback after session
session_rating = 5  # user gave 5-star feedback

partner = users[1]  # Ankit
print(f"Before Feedback Trust Score: {partner['rating']}")

update_trust_score(partner, session_rating)

print(f"After Feedback Trust Score: {partner['rating']}")

