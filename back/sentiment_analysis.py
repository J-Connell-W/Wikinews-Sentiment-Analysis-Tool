import pandas as pd
import spacy
from spacy import displacy
from collections import Counter
from transformers import pipeline
import torch 
from transformers import T5Tokenizer, T5Model, T5ForConditionalGeneration
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
#import web_scraper as ws
#import translation_models
import sentiment_analysis
from bs4 import BeautifulSoup
import requests
import re
import transformers
import sentencepiece

urls = ["https://de.wikinews.org/wiki/Regierungskrise_in_Nordirland_beendet",
    "https://es.wikinews.org/wiki/Mandatarios_y_personalidades_reaccionan_a_la_muerte_de_Piñera",
    "https://en.wikinews.org/wiki/Margrethe_II,_Queen_of_Denmark,_announces_abdication",
    "https://en.wikinews.org/wiki/Ukrainian_missile_and_drone_strike_in_Russia_kills_at_least_21_people",
    "https://es.wikinews.org/wiki/López_Obrador_presenta_paquete_de_reformas_constitucionales"
]

def scrape_wikinews(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    target_div = soup.select_one(
        "#mw-content-text > div.mw-content-ltr.mw-parser-output"
    )
    if not target_div:
        target_div = soup.select_one("#bodyContent")
        if not target_div:
            print("Target div not found.")
            return ""

    # Remove all table tags and their children from target_div
    for table in target_div.find_all("table"):
        table.decompose()

    div_to_remove = target_div.find("div", {"class": "infobox"})
    if div_to_remove:
        div_to_remove.decompose()

    content = []

    def get_element_text(element):
        """Extracts and constructs text from an element, handling nested tags appropriately."""
        pieces = []
        for child in element.children:
            if child.name == "a":
                pieces.append(
                    child.get_text(strip=True)
                )  # Adding spaces around hyperlinks
            elif child.string:
                pieces.append(child.string)
        return "".join(pieces).strip()

    # Iterate through all elements and stop when 'Fuentes' ID is found in a span
    for element in target_div.find_all(["p", "li", "span"]):
        if element.name == "span" and element.get("id") in [
            "Fuentes",
            "Sources",
            "Related_news",
            "Sister_links",
            "Noticia_relacionada",
        ]:
            break
        if element.name in ["p", "li"]:
            text = get_element_text(element)
            content.append(text)
    # Remove dates and extra elements
    date_regex_es = re.compile(r"\b\d{1,2} de [a-z]+ de \d{4}\b", re.IGNORECASE)
    date_regex_en = re.compile(
        r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), (January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}$",
        re.IGNORECASE,
    )

    content = [
        text
        for text in content
        if not re.match(date_regex_es, text) and not re.match(date_regex_en, text)
    ]

    if content and "Have an opinion on this story? Share it!" in content[-1]:
        content.pop()

    all_text = " ".join(content)
    return all_text


# Example usage
url = "https://es.wikinews.org/wiki/CBF_y_FIFA_lamentan_la_muerte_de_Carlos_Alberto_Torres,_excapit%C3%A1n_de_la_Selecci%C3%B3n_Brasile%C3%B1a"
# print(scrape_wikinews(url))

# Scrape the content of each URL
story_content = scrape_wikinews(urls[1])
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
# translator_to_english = pipeline("translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en", max_length=600)
# translation_english = translator_to_english(story_content)
# print(translation_english[0]['translation_text'])

# Translating from Chinese to English
# Accuracy rate against ChatGPT-4 ( %)
# translator_to_english = pipeline("translation_zh_to_en", model="Helsinki-NLP/opus-mt-zh-en")
# translation_english = translator_to_english(summarized_text)
# print(translation_english[0]['translation_text'])