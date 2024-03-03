from transformers import DistilBertTokenizer, pipeline
import re

# Initialize the tokenizer and the model only once to avoid reloading them multiple times.
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def chunk_text_by_tokens(text, max_token_count=512):
    """
    Split the text into chunks based on a maximum token count.
    """
    # Tokenize the text
    tokens = tokenizer.tokenize(text)

    # Chunk tokens
    chunks = [
        tokens[i : i + max_token_count] for i in range(0, len(tokens), max_token_count)
    ]

    # Decode tokens to text for each segment
    chunk_texts = [tokenizer.convert_tokens_to_string(chunk) for chunk in chunks]

    return chunk_texts


def format_summary(summary):
    """
    Formats a summary to ensure proper sentence casing and punctuation.
    Assumes that sentences end with '.', '?', or '!', and capitalizes the first letter of each sentence.
    """

    # Function to capitalize the first letter of a sentence
    def capitalize_first_letter(sentence):
        return sentence[0].upper() + sentence[1:] if sentence else sentence

    # Split the summary into sentences based on '.', '?', and '!', then strip and capitalize them
    sentences = re.split("([.!?])", summary)
    formatted_sentences = []

    # Process each sentence and following punctuation mark
    for i in range(0, len(sentences) - 1, 2):
        sentence = capitalize_first_letter(sentences[i].strip())
        punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""
        formatted_sentences.append(f"{sentence}{punctuation}")

    # Handle the last sentence if there's no trailing punctuation
    if sentences and len(sentences) % 2 != 0:
        last_sentence = capitalize_first_letter(sentences[-1].strip())
        formatted_sentences.append(last_sentence)

    # Combine the formatted sentences into a single paragraph
    formatted_paragraph = " ".join(formatted_sentences).strip()

    # Ensure the paragraph ends with a period if it doesn't end with any sentence-ending punctuation
    if formatted_paragraph and not formatted_paragraph[-1] in ".!?":
        formatted_paragraph += "."

    return formatted_paragraph


def summarization(text):
    """
    Summarize the text by first chunking it into segments that fit within the model's token limit,
    then summarizing each chunk. Returns a formatted paragraph from the summaries of each chunk.
    """
    # Split the text into chunks that are within the token limit
    chunks = chunk_text_by_tokens(text, 350)

    formatted_summaries = []
    for chunk in chunks:

        # Summarize each chunk. Note: the summarizer can accept a string directly.
        chunk_summary = summarizer(chunk)
        # Format each summary and add to the list
        formatted_summary = format_summary(chunk_summary[0]["summary_text"])
        formatted_summaries.append(formatted_summary)

    # Combine formatted summaries into a single paragraph
    final_paragraph = " ".join(formatted_summaries)
    return final_paragraph
