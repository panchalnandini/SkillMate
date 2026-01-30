import numpy as np
from sklearn.linear_model import LogisticRegression

# Initial training data
X_train = [
    [1.0, 1.0, 0.9],
    [0.9, 0.8, 0.8],
    [0.3, 0.4, 0.2],
    [0.6, 0.7, 0.6],
    [0.2, 0.3, 0.4],
]

y_train = [1, 1, 0, 1, 0]

model = LogisticRegression()
model.fit(X_train, y_train)


def predict_match_quality(skill_match, availability, trust_score):
    """
    Predicts probability of successful skill swap
    """
    features = np.array([[skill_match, availability, trust_score]])
    probability = model.predict_proba(features)[0][1]
    return round(probability, 2)

def retrain_model(skill, availability, trust, outcome):
    """
    outcome: 1 = successful swap, 0 = failed swap
    """
    X_train.append([skill, availability, trust])
    y_train.append(outcome)

    model.fit(X_train, y_train)

