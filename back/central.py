import validation
import web_scraper as ws
import sentiment_analysis as sa
import summarization as su
import translation_models as tm
import visualization as vi
import sentence_splitter as ss


# Validate URL and scrape content
def master_function(story):
    print("validating URl..")
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
    print("Scraping web...")
    # Split the content into sentences
    story_content_split = ss.sentence_split(story_content)
    print("splitting sentences...")
    # Translation
    if getattr(story, "translation_language", None):
        print("Translating...")
        postTranslationStepStory = tm.translation(
            story_content, story.original_language, story.translation_language
        )
        # Make copy of translation

        isTranslation = True
    else:
        print("Skipped Translating")
        postTranslationStepStory = story_content
        isTranslation = False

    print(postTranslationStepStory)
    print(story_content)
    # Summarization
    if isTranslation:
        print("Translation Summarizing...")
        summarizationTranslated = su.summarization(postTranslationStepStory)
        print("Normal Summarizing...")
        summarization = su.summarization(story_content)

    else:
        print("Normal Summarizing...")
        summarization = su.summarization(postTranslationStepStory)

    # Sentiment Analysis
    print("Sentiment Analysis...")
    sentiment = sa.sentiment_analysis(story_content)

    sentiment_label = sentiment.get("sentiment")
    sentiment_score = sentiment.get("score")
    # Our Sentiment Analysis Model will get a label and score here and we can use it for english or translate then use it and send it back to the front end
    # ourSentimentModel = whatever we call it
    # ourSentiment_label = ourSentimentModel[0].get("label")
    # ourSentiment_score = ourSentimentModel[0].get("score")

    # # Visualization
    html_get_dep = vi.get_html_dep(story_content)

    # If there is a translation, send to Front End with translation or else do not send translation
    if isTranslation:
        # Send to Front End
        return {
            "story_content_split_sentences": story_content_split,
            "translation": postTranslationStepStory,
            "summarization": summarization,
            "summarizationTranslated": summarizationTranslated,
            "sentiment_label": sentiment_label,
            "sentiment_score": sentiment_score,
            # ourSentiment_label: ourSentiment_label,
            # ourSentiment_score: ourSentiment_score,
            "html_get_dep": html_get_dep,
        }
    else:
        return {
            "story_content_split_sentences": story_content_split,
            "summarization": summarization,
            "sentiment_label": sentiment_label,
            "sentiment_score": sentiment_score,
            # ourSentiment_label: ourSentiment_label,
            # ourSentiment_score: ourSentiment_score,
            "html_get_dep": html_get_dep,
        }
