import validation 
import sentiment_analysis as sa
import summarization as su
import translation_models as tm

# Validate URL and scrape content 
def master_function(story):
    # Check if the URL is from Wikinews
    if not validation.contains_wikinews(story.url):
        return {"message": "URL is not from Wikinews!"}    
    # Check if the URL is valid
    if not validation.website_validator(story.url):
        return {"message": "Invalid URL!"}
    # Scrape the Wikinews page
    if not validation.check_wiki(story.url):
        return {"message": "URL is not a Wikinews article!"}
    
    # Scrape the content of a URL
    story.content = sa.scrape_wikinews(story.url)

    # Translation
    translation = tm.translation(story.content, story)
    
    # Make copy of translation
    translation_copy = translation

    # Summarization 
    summarization = su.summarization(translation)

    # Sentiment Analysis
    sentiment = sa.sentiment_analysis(translation)

# Visualization 
    # Spacy (Tokenization, Lemmatization, POS Tagging)
    # Displacy 

# Send to Front End 
    

