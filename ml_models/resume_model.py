def resume_score(text):
    score = len(text.split())  # simple logic
    return {
        "score": score,
        "message": "Resume analyzed successfully"
    }