import back.web_scraper as ws
import transformers

urls = ["https://de.wikinews.org/wiki/Regierungskrise_in_Nordirland_beendet",
    "https://es.wikinews.org/wiki/Mandatarios_y_personalidades_reaccionan_a_la_muerte_de_Piñera",
    "https://en.wikinews.org/wiki/Margrethe_II,_Queen_of_Denmark,_announces_abdication",
    "https://en.wikinews.org/wiki/Ukrainian_missile_and_drone_strike_in_Russia_kills_at_least_21_people",
    "https://es.wikinews.org/wiki/López_Obrador_presenta_paquete_de_reformas_constitucionales"
]

# This will hold the list of lists, where each sublist is the tokens of a story
tokenized_stories = []

# Scrape the content of each URL
story_content = ws.scrape_wikinews(urls[4])
print(story_content)


# Summarization Model
# summarizer = pipeline("summarization")
# summary = summarizer(story_content)
# summarized_text = summary[0]['summary_text']
# print(summarized_text)

# Translation Models

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
translator_to_english = pipeline("translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en")
translation_english = translator_to_english(story_content)
print(translation_english[0]['translation_text'])

# Translating from Chinese to English
# Accuracy rate against ChatGPT-4 ( %)
# translator_to_english = pipeline("translation_zh_to_en", model="Helsinki-NLP/opus-mt-zh-en")
# translation_english = translator_to_english(summarized_text)
# print(translation_english[0]['translation_text'])
