import validation
import web_scraper as ws
import sentiment_analysis as sa
import summarization as su
import translation_models as tm
import visualization as vi
import sentence_splitter as ss


# Validate URL and scrape content
def master_function(story):
    # Check if the URL is from Wikinews
    if not validation.contains_wikinews(story.id):
        return {"message": "URL is not from Wikinews!"}
    # Check if the URL is valid
    if not validation.website_validator(story.id):
        return {"message": "Invalid URL!"}
    # Scrape the Wikinews page
    if not validation.check_wiki(story.id):
        return {"message": "URL is not a Wikinews article! " + story.id}

    # Scrape the content of a URL
    story_content = ws.scrape_wikinews(story.id)

    # Split the content into sentences
    story_content_split = ss.sentence_split(story_content)
    # Translation
    translation = tm.translation(story_content, story)

    # Make copy of translation
    translation_copy = translation

    # Summarization
    summarization = su.summarization(translation)

    # Sentiment Analysis
    sentiment = sa.sentiment_analysis(translation)
    sentiment_label = sentiment[0].get("label")
    sentiment_score = sentiment[0].get("score")

    # Visualization
    html_get_dep = vi.get_html_dep(story_content)

    # Send to Front End
    return {
        "story_content_split_sentences": story_content_split,
        "translation": translation,
        "summarization": summarization,
        "sentiment_label": sentiment_label,
        "sentiment_score": sentiment_score,
        "html_get_dep": html_get_dep,
    }
