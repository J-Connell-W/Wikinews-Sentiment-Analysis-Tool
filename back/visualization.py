import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import re 

nlp = spacy.load("en_core_web_sm")
doc = nlp(story_content)
sentance_spans = list(doc.sents)
doc_list = [token for token in doc if not token.is_stop]
help(displacy.serve)

# Get Jupyter notebook to display displacy
displacy.render(doc.sents, style="dep")
for token in doc:
    print(token.text, token.lemma, token.pos, token.tag, token.dep,
            token.shape_, token.is_alpha, token.is_stop)

# Lemmatization 
doc_list_lemma = [token.lemma_ for token in doc_list]
print(doc_list_lemma)

# Word Frequency
words = [
    token.text
    for token in doc
    if not token.is_stop and not token.is_punct
]
print(Counter(words).most_common(5))

# POS Tagging 
for token in doc_list:
    print(
        f"""
TOKEN: {str(token)}
=====
TAG: {str(token.tag_):10} POS: {token.pos_}
EXPLANATION: {spacy.explain(token.tag_)}"""
)