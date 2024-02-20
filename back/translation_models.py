import web_scraper as ws
import transformers
from transformers import pipeline
import models

urls = [
    "https://de.wikinews.org/wiki/Regierungskrise_in_Nordirland_beendet",
    "https://es.wikinews.org/wiki/Mandatarios_y_personalidades_reaccionan_a_la_muerte_de_Piñera",
    "https://en.wikinews.org/wiki/Margrethe_II,_Queen_of_Denmark,_announces_abdication",
    "https://en.wikinews.org/wiki/Ukrainian_missile_and_drone_strike_in_Russia_kills_at_least_21_people",
    "https://es.wikinews.org/wiki/López_Obrador_presenta_paquete_de_reformas_constitucionales",
]

# Translation Models


def translation(story_content, story):
    if story.original_language == "English" and story.translation_language == "Spanish":
        return translation_english_to_spanish(story_content)
    elif (
        story.original_language == "Spanish" and story.translation_language == "English"
    ):
        return translation_spanish_to_english(story_content)


# Translating from English to German
# Accuracy rate against ChatGPT-4 ( %)
# translator_from_german = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de")
# translation_german = translator_from_german(story_content)
# print(translation_german[0]['translation_text'])

# Translating from German to English
# Accuracy rate against ChatGPT-4 ( %)
# translator_to_english = pipeline("translation_de_to_en", model="Helsinki-NLP/opus-mt-de-en")
# translation_english = translator_to_english(translation_german[0]['translation_text'])
# print(translation_english[0]['translation_text'])


# Translating from Spanish to English
# Accuracy rate against ChatGPT-4 (65%)
# Accuracy rate against Human Translator (poor,fair,good,very good,excellent)
def translation_spanish_to_english(story_content):
    translator_to_english = pipeline(
        "translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en"
    )
    translation_english = translator_to_english(story_content)
    return translation_english[0]["translation_text"]


# Translating from Spanish to English
def translation_english_to_spanish(story_content):
    translator_to_spanish = pipeline(
        "translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es"
    )
    translation_spanish = translator_to_spanish(story_content)
    return translation_spanish[0]["translation_text"]


# Translating from Chinese to English
# Accuracy rate against ChatGPT-4 ( %)
# translator_to_english = pipeline("translation_zh_to_en", model="Helsinki-NLP/opus-mt-zh-en")
# translation_english = translator_to_english(summarized_text)
# print(translation_english[0]['translation_text'])
