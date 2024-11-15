# exam/nlp_service.py

import spacy
from textblob import TextBlob
import language_tool_python

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

def analyze_text(text):
    suggestions = []

    # Stop word analysis
    doc = nlp(text)
    for token in doc:
        if token.is_stop:
            suggestions.append(f"Consider removing '{token.text}' for clarity.")

    # Sentiment analysis using TextBlob
    blob = TextBlob(text)
    sentiment = blob.sentiment

    # Grammar and spelling checks using LanguageTool
    matches = tool.check(text)
    grammar_suggestions = [
        {
            "error": match.message,
            "suggestions": match.replacements,
            "offset": match.offset,
            "length": match.errorLength
        }
        for match in matches
    ]

    return {
        "text": text,
        "stop_word_suggestions": suggestions,
        "sentiment": {
            "polarity": sentiment.polarity,
            "subjectivity": sentiment.subjectivity
        },
        "grammar_suggestions": grammar_suggestions
    }
