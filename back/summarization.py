from transformers import pipeline

# Summarization Model
def summarization(story_content):
    summarizer = pipeline("summarization")
    summary = summarizer(story_content)
    summarized_text = summary[0]['summary_text']
    return summarized_text
