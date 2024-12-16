def evaluate_attempt(attempt, target_word):
    feedback = []
    for i, letter in enumerate(attempt):
        if letter == target_word[i]:
            feedback.append("correct")
        elif letter in target_word:
            feedback.append("present")
        else:
            feedback.append("absent")
    return feedback

