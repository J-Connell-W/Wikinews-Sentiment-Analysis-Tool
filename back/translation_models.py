import web_scraper as ws
from transformers import pipeline, MarianTokenizer


# Entry Function for Translation of the Story Calls the model that is fine tuned for the specific language.
def translation(story_content, original_language, translation_language):
    if original_language == "English":
        if translation_language == "German":
            return translation_english_to_german(story_content)
        elif translation_language == "Spanish":
            return translation_english_to_spanish(story_content)
        else:
            return story_content
    elif original_language == "German":
        if translation_language == "English":
            return translation_german_to_english(story_content)
        elif translation_language == "Spanish":
            return translation_german_to_spanish(story_content)
        else:
            return story_content
    elif original_language == "Spanish":
        if translation_language == "English":
            return translation_spanish_to_english(story_content)
        elif translation_language == "German":
            return translation_spanish_to_german(story_content)
        else:
            return story_content
    else:
        return story_content


# Run through model and chunk text into max of 250 tokens, can adjust the max_length to a higher value if needed under 512
def run_through_model(text, max_length, model_name, translator_model):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        if len(tokenizer.encode(current_chunk + word)) < max_length:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
    if current_chunk:
        chunks.append(current_chunk.strip())

    translated = run_chunk_through_model(chunks, translator_model)
    return translated


# Actually Running the chunks through the model
def run_chunk_through_model(chunks, translator_model):
    translation = ""
    for chunk in chunks:
        translated_chunk = translator_model(chunk)
        translation += translated_chunk[0]["translation_text"] + " "
    return translation.strip()


# Translation Models


# Translating from English to German
def translation_english_to_german(story_content):
    max_length = 250
    translator_to_german = pipeline(
        "translation_en_to_de",
        model="Helsinki-NLP/opus-mt-en-de",
        max_length=max_length,
    )
    english_to_german_translation = run_through_model(
        story_content, max_length, "Helsinki-NLP/opus-mt-en-de", translator_to_german
    )
    return english_to_german_translation


# Translating from German to English
def translation_german_to_english(story_content):
    max_length = 250
    translator_to_english = pipeline(
        "translation_de_to_en",
        model="Helsinki-NLP/opus-mt-de-en",
        max_length=max_length,
    )
    german_to_english_translation = run_through_model(
        story_content, max_length, "Helsinki-NLP/opus-mt-de-en", translator_to_english
    )
    return german_to_english_translation


# Translating from Spanish to English
def translation_spanish_to_english(story_content):
    max_length = 250
    translator_to_english = pipeline(
        "translation_es_to_en",
        model="Helsinki-NLP/opus-mt-es-en",
        max_length=max_length,
    )
    # Split the text into chunks
    spanish_to_english_translation = run_through_model
    (story_content, max_length, "Helsinki-NLP/opus-mt-es-en", translator_to_english)
    return spanish_to_english_translation


# Translating from English to Spanish
def translation_english_to_spanish(story_content):
    max_length = 250
    translator_to_spanish = pipeline(
        "translation_en_to_es",
        model="Helsinki-NLP/opus-mt-en-es",
        max_length=max_length,
    )
    translation_english_to_spanish = run_through_model(
        story_content, max_length, "Helsinki-NLP/opus-mt-en-es", translator_to_spanish
    )
    return translation_english_to_spanish


# Translating from Spanish to German
def translation_spanish_to_german(story_content):
    max_length = 250
    translator_to_german = pipeline(
        "translation_es_to_de",
        model="Helsinki-NLP/opus-mt-es-de",
        max_length=max_length,
    )
    # Split the text into chunks
    spanish_to_german_translation = run_through_model
    (story_content, max_length, "Helsinki-NLP/opus-mt-es-de", translator_to_german)
    return spanish_to_german_translation


# Translating from Spanish to German
def translation_german_to_spanish(story_content):
    max_length = 250
    translator_to_spanish = pipeline(
        "translation_de_to_es",
        model="Helsinki-NLP/opus-mt-de-es",
        max_length=max_length,
    )
    # Split the text into chunks
    german_to_spanish_translation = run_through_model
    (story_content, max_length, "Helsinki-NLP/opus-mt-de-es", translator_to_spanish)
    return german_to_spanish_translation
