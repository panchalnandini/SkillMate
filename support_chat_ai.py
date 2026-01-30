# from platform_knowledge import PLATFORM_KNOWLEDGE

# # Flatten all questions for easy search
# QUESTION_MAP = {}
# for section, qa in PLATFORM_KNOWLEDGE.items():
#     for question, answer in qa.items():
#         QUESTION_MAP[question] = answer

# # Function to find best answer
# def find_best_answer(message):
#     message = message.lower()
#     best_match = None
#     max_score = 0

#     for question, answer in QUESTION_MAP.items():
#         score = sum(1 for word in question.split() if word in message)
#         if score > max_score:
#             max_score = score
#             best_match = answer

#     if best_match and max_score > 0:
#         return best_match
#     else:
#         return "I’m not fully sure about that. I’ll connect you to support."

# # Main chat function
# def support_chat(message, context=None):
#     reply = find_best_answer(message)
#     return reply

# # 🔽 TESTING
# if __name__ == "__main__":
#     print("Skill Swap Support Chat (type 'exit' to stop)\n")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "exit":
#             break
#         reply = support_chat(user_input)
#         print("Bot:", reply)


from platform_knowledge import PLATFORM_KNOWLEDGE
import difflib

# Flatten knowledge base
QUESTION_MAP = {}
for section, qa in PLATFORM_KNOWLEDGE.items():
    for question, answer in qa.items():
        QUESTION_MAP[question.lower()] = answer

# Context memory
CONTEXT_MEMORY = {}

# Fuzzy matching function
def find_best_answer(message):
    message = message.lower()
    questions = list(QUESTION_MAP.keys())
    
    # Find closest match
    best_match = difflib.get_close_matches(message, questions, n=1, cutoff=0.4)
    
    if best_match:
        return QUESTION_MAP[best_match[0]]
    else:
        return None

# Main chat function
def support_chat(user_id, message):
    if user_id not in CONTEXT_MEMORY:
        CONTEXT_MEMORY[user_id] = []
    
    CONTEXT_MEMORY[user_id].append(message)
    
    answer = find_best_answer(message)
    if answer:
        CONTEXT_MEMORY[user_id].append(answer)
        return answer
    else:
        return "I’m not fully sure about that. I’ll connect you to human support for help."

# Clear user context
def clear_context(user_id):
    if user_id in CONTEXT_MEMORY:
        CONTEXT_MEMORY[user_id] = []

# Testing
if __name__ == "__main__":
    print("Skill Swap Support Chat (type 'exit' to stop)")
    user_id = "test_user"
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        reply = support_chat(user_id, user_input)
        print("Bot:", reply)
