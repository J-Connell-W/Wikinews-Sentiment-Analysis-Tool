import web_scraper as ws
from transformers import pipeline, MarianTokenizer


# Entry Function for Translation
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


def split_into_chunks(text, max_length, model_name, translator_model):
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


def run_chunk_through_model(chunks, translator_model):
    translation = ""
    for chunk in chunks:
        translated_chunk = translator_model(chunk)
        translation += translated_chunk[0]["translation_text"] + " "

    return translation.strip()


# Translation Models


# Translating from German to English
def translation_german_to_english(story_content):
    max_length = 250
    translator_to_english = pipeline(
        "translation_de_to_en",
        model="Helsinki-NLP/opus-mt-de-en",
        max_length=max_length,
    )
    german_to_english_translation = split_into_chunks(
        story_content, max_length, "Helsinki-NLP/opus-mt-de-en", translator_to_english
    )
    return german_to_english_translation


# Translating from Spanish to English
# Accuracy rate against ChatGPT-4 (65%)
# Accuracy rate against Human Translator (poor,fair,good,very good,excellent)
def translation_spanish_to_english(story_content):
    max_length = 250
    translator_to_english = pipeline(
        "translation_es_to_en",
        model="Helsinki-NLP/opus-mt-es-en",
        max_length=max_length,
    )
    # Split the text into chunks
    chunks = split_into_chunks(story_content, max_length, "Helsinki-NLP/opus-mt-es-en")
    # Process each chunk and concatenate the results
    translation_english = ""
    for chunk in chunks:
        translated_chunk = translator_to_english(chunk)
        translation_english += translated_chunk[0]["translation_text"] + " "

    return translation_english.strip()


# Translating from Spanish to English
def translation_english_to_spanish(story_content):
    max_length = 250
    translator_to_spanish = pipeline(
        "translation_en_to_es",
        model="Helsinki-NLP/opus-mt-en-es",
        max_length=max_length,
    )
    # translation_spanish = translator_to_spanish(story_content)
    # return translation_spanish[0]["translation_text"]
    # Split the text into chunks
    chunks = split_into_chunks(story_content, max_length)

    # Process each chunk and concatenate the results
    translation_spanish = ""
    for chunk in chunks:
        translated_chunk = translator_to_spanish(chunk)
        translation_spanish += translated_chunk[0]["translation_text"] + " "

    return translation_spanish.strip()


# Translating from Chinese to English
# Accuracy rate against ChatGPT-4 ( %)
# translator_to_english = pipeline("translation_zh_to_en", model="Helsinki-NLP/opus-mt-zh-en")
# translation_english = translator_to_english(summarized_text)
# print(translation_english[0]['translation_text'])
