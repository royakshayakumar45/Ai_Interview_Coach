def analyze_text(text):
    words = text.split()
    word_count = len(words)

    # filler words list
    filler_words_list = ["um", "uh", "like", "you know", "basically"]
    
    filler_count = 0
    for word in words:
        if word.lower() in filler_words_list:
            filler_count += 1

    # simple sentiment logic
    if word_count == 0:
        sentiment = "Neutral"
    elif word_count < 10:
        sentiment = "Low"
    elif word_count < 30:
        sentiment = "Medium"
    else:
        sentiment = "High"

    # confidence score (0 to 1)
    confidence = min(word_count / 50, 1)

    return filler_count, sentiment, confidence