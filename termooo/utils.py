def evaluate_attempt(attempt, target_word):
    feedback = []
    for i, letter in enumerate(attempt):
        if letter == target_word[i]:
            feedback.append("correto")
        elif letter in target_word:
            feedback.append("presente")
        else:
            feedback.append("ausente")
    return feedback

