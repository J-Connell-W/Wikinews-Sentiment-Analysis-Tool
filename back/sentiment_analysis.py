from transformers import pipeline

# Sentiment Analysis Model
def sentiment_analysis(story_content):
    sentiment_analysis_model = pipeline("sentiment-analysis")
    return sentiment_analysis_model(story_content)

