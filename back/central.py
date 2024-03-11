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
    sentiment, custom_model_error_message = sa.sentiment_analysis(
        story_content, story.original_language
    )
    sentiment_label = sentiment.get("sentiment")
    sentiment_score = sentiment.get("score")
    custom_model_error = custom_model_error_message

    # Visualization
    # If the story's source language is in English, we can visualize the dependency parsing and named entity recognition in addition to the translation.
    # This is because the visualization tends to make mistakes for other languages when showing the dependency parsing and named entity recognition.
    if story.original_language == "English":
        print("Visualize...")
        html_get_dep, html_get_ner = vi.visualize(story_content)

    print(html_get_ner)
    # Return the results of the tools.
    return {
        "story_content_split_sentences": story_content_split,
        "translation": postTranslationStepStory,
        "summarization": summarization,
        "summarizationTranslated": summarizationTranslated,
        "sentiment_label": sentiment_label,
        "sentiment_score": sentiment_score,
        "html_get_dep": html_get_dep,
        "html_get_ner": html_get_ner,
        "custom_model_error": custom_model_error,
    }
