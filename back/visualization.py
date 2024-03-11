import spacy
from spacy import displacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")


# Visualization returns the html of the dependency parsing, and named entity recognition for the story content by sentence in english.
def visualize(story_content):
    options = {
        "distance": 120,
        "compact": True,
        "bg": "#d3d3d3",
    }
    colors = {"Ner-text": "#000000"}
    doc = nlp(story_content)
    sentence_spans = list(doc.sents)
    return displacy.render(
        sentence_spans, style="dep", options=options
    ), displacy.render(doc, style="ent", jupyter=False, options={"colors": colors})
