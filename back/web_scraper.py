import sentiment_analysis
from bs4 import BeautifulSoup
import requests
import re

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
print(scrape_wikinews(url))