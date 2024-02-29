import web_scraper as ws
from transformers import pipeline, MarianTokenizer


def split_into_chunks(text, max_length):
    tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")
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

    return chunks


# Translation Models
def translation(story_content, story):
    if story.original_language == "English" and story.translation_language == "Spanish":
        return translation_english_to_spanish(story_content)
    elif (
        story.original_language == "Spanish" and story.translation_language == "English"
    ):
        return translation_spanish_to_english(story_content)
    else:
        return story_content


# Translating from English to German
# Accuracy rate against ChatGPT-4 ( %)
# translator_from_german = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de")
# translation_german = translator_from_german(story_content)
# print(translation_german[0]['translation_text'])


# Translating from German to English
# Accuracy rate against ChatGPT-4 ( %)
def translation_german_to_english(story_content):
    max_length = 500
    translator_to_english = pipeline(
        "translation_de_to_en",
        model="Helsinki-NLP/opus-mt-de-en",
        max_length=max_length,
    )
    translator_to_english(story_content)
    return translator_to_english
    # Split the text into chunks
    # chunks = split_into_chunks(story_content, max_length)

    # # Process each chunk and concatenate the results
    # translation_english = ""
    # for chunk in chunks:
    #     translated_chunk = translator_to_english(chunk)
    #     translation_english += translated_chunk[0]["translation_text"] + " "

    #     return translation_english.strip()


# Example list of translations
# translations = ["First translated sentence.", "Second translated sentence.", ...]

# Path to the output file
# output_file_path = 'path/to/your/output_file.txt'

# Writing the translations to a file
# with open(output_file_path, 'w', encoding='utf-8') as output_file:
#     for translation in translations:
#         output_file.write(translation + '\n')

# The file is now ready to be used with SacreBLEU

# translator_to_english = pipeline("translation_de_to_en", model="Helsinki-NLP/opus-mt-de-en")
# translation_english = translator_to_english(translation_german[0]['translation_text'])
# print(translation_english[0]['translation_text'])


# Translating from Spanish to English
# Accuracy rate against ChatGPT-4 (65%)
# Accuracy rate against Human Translator (poor,fair,good,very good,excellent)
def translation_spanish_to_english(story_content):
    max_length = 500
    translator_to_english = pipeline(
        "translation_es_to_en",
        model="Helsinki-NLP/opus-mt-es-en",
        max_length=max_length,
    )
    # Split the text into chunks
    chunks = split_into_chunks(story_content, max_length)

    # Process each chunk and concatenate the results
    translation_english = ""
    for chunk in chunks:
        translated_chunk = translator_to_english(chunk)
        translation_english += translated_chunk[0]["translation_text"] + " "

    return translation_english.strip()


# Translating from Spanish to English
def translation_english_to_spanish(story_content):
    max_length = 500
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
