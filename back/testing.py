import sacrebleu
import sentence_splitter as ss
from sacrebleu.metrics import BLEU, CHRF, TER
import translation_models as tm


# Calculate BLEU score (uses detokenized sentences)
def calculate_bleu(hypotheses, references):
    bleu = sacrebleu.corpus_bleu(hypotheses, [references])
    print(bleu.score)

english_sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Artificial intelligence is a fascinating field of study.",
    "The sun sets in the west.",
    "Music can change the world.",
    "Books are the best companions.",
    "A healthy mind resides in a healthy body.",
    "Technology is advancing rapidly.",
    "Education is the key to success.",
    "The journey of a thousand miles begins with a single step.",
    "Time and tide wait for no one."
]

german_sentences = [
    "Der schnelle braune Fuchs springt über den faulen Hund.",
    "Künstliche Intelligenz ist ein faszinierendes Studiengebiet.",
    "Die Sonne geht im Westen unter.",
    "Musik kann die Welt verändern.",
    "Bücher sind die besten Begleiter.",
    "In einem gesunden Körper wohnt ein gesunder Geist.",
    "Die Technologie schreitet rasch voran.",
    "Bildung ist der Schlüssel zum Erfolg.",
    "Die Reise von tausend Meilen beginnt mit einem einzigen Schritt.",
    "Zeit und Gezeiten warten auf niemanden."
]

def german_period():
    german_appended = " ".join(german_sentences)
    german_english = tm.translation_german_to_english(german_appended)
    ss.sentence_split(german_english)
    for sentence in german_english:
        sentence += "."
    return german_english

german_translation = german_period()

calculate = calculate_bleu(german_translation, english_sentences)
# print(calculate)

help(sacrebleu.corpus_bleu)

# print(f"Source file: {src}")
# print(f"Reference file: {ref}")

# print(sacrebleu.get_available_testsets())

# import nltk

# # Sample reference and candidate sentences
# reference = "The cat is on the mat".split()
# candidate = "The cat is on the mat".split()

# # Calculate BLEU score
# bleu_score = nltk.translate.bleu_score.sentence_bleu([reference], candidate)

# corpus_bleu_score = nltk.translate.bleu_score.corpus_bleu([[reference]], [candidate])

# print("Corpus BLEU Score:", corpus_bleu_score)
