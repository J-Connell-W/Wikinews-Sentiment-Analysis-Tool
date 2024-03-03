from transformers import DistilBertTokenizer, pipeline

# Initialize the tokenizer and the model only once to avoid reloading them multiple times.
tokenizer = DistilBertTokenizer.from_pretrained(
    "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
)
sentiment_model = pipeline(
    "sentiment-analysis",
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
)


def chunk_text(text, max_token_count=512):  # Leave space for special tokens
    # Directly work with token ids to ensure precise control over chunk sizes
    token_ids = tokenizer.encode(text, add_special_tokens=True)
    # Calculate the actual chunk size, accounting for special tokens
    chunk_size = max_token_count - 2  # Reserving space for [CLS] and [SEP]
    chunks = []

    for i in range(0, len(token_ids), chunk_size):
        # Extract the token ids for this chunk
        chunk_token_ids = token_ids[i : i + chunk_size]
        # Prepend [CLS] and append [SEP] tokens
        chunk_with_special_tokens = (
            [tokenizer.cls_token_id] + chunk_token_ids + [tokenizer.sep_token_id]
        )
        # Decode the chunk back to text
        chunk_text = tokenizer.decode(
            chunk_with_special_tokens, skip_special_tokens=True
        )
        chunks.append(chunk_text)
    return chunks


def sentiment_analysis(text):
    chunks = chunk_text(text)
    total_score = 0
    total_tokens = 0
    for chunk in chunks:
        # Process each chunk with the model and collect results
        result = sentiment_model(chunk)[
            0
        ]  # Assuming each chunk returns a single sentiment analysis result
        chunk_tokens = tokenizer.encode(chunk, add_special_tokens=True)
        num_tokens = len(chunk_tokens)
        total_tokens += num_tokens
        score = (
            result["score"] if result["label"] == "POSITIVE" else (1 - result["score"])
        )
        total_score += (
            score * num_tokens
        )  # Weight score by number of tokens in the chunk

    average_score = total_score / total_tokens
    sentiment = "positive" if average_score >= 0.5 else "negative"

    return {"sentiment": sentiment, "score": average_score}
