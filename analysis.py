from textblob import TextBlob

def analyze_sentiment(comment):
    scores = [TextBlob(c).sentiment.polarity for c in comment]
    overall_sentiment = sum(scores) / len(scores)