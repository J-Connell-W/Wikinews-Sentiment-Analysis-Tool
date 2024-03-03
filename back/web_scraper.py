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

    # Iterate through all elements and stop when one of these ID's are found in any of the selected tags
    for element in target_div.find_all(
        ["p", "li", "span", "a"]
    ):  # Search through <p>, <li>, <span>, and <a> tags.
        # Define the array of specific IDs outside the loop for clarity and efficiency.
        specific_ids = [
            "Fuentes",
            "Sources",
            "Related_news",
            "Sister_links",
            "Noticia_relacionada",
            "Quellen",
        ]

        # Check if the element is a <span> or <a> tag and if its id is in the specific_ids array.
        if element.get("id") in specific_ids:
            break

        # Additional check for <a> tags to see if their text is "Kommentar abgeben".
        if element.name == "a" and element.text.strip() == "Kommentar abgeben":
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
