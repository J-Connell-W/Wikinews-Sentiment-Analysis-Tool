from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    pipeline,
)

# Initialize the tokenizer for our model
our_model_tokenizer = DistilBertTokenizer.from_pretrained(
    "./Distilbert/tokenizer_distilbert_finetuned/", local_files_only=True
)


def determineModelUsage(source_language):
    if source_language == "English":
        model = DistilBertForSequenceClassification.from_pretrained(
            "./Distilbert/", local_files_only=True
        )
        tokenizer = our_model_tokenizer
    else:
        model = pipeline(
            "sentiment-analysis",
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
        )
        tokenizer = None  # No need for tokenizer outside English; pipeline manages it.
    return model, tokenizer


def sentiment_analysis(text, source_language):
    model, tokenizer = determineModelUsage(source_language)

    if source_language == "English":
        # Tokenize and process text for English
        inputs = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=512,
            return_attention_mask=True,
        )
        outputs = model(**inputs)
        logits = outputs.logits
        # Convert logits to probabilities
        probabilities = logits.softmax(dim=-1)
        prediction = probabilities.argmax(dim=1).item()
        # Interpret prediction
        sentiment = "positive" if prediction == 1 else "negative"
        score = probabilities[0, prediction].item()
    else:
        # Use pipeline for non-English texts
        result = model(text)[0]  # Assuming single result for simplicity
        sentiment = result["label"].lower()
        score = result["score"]

    return {"sentiment": sentiment, "score": score}


# Example usage
# text = "This is an example text to analyze."
# source_language = "English"  # Change as needed
# result = sentiment_analysis(text, source_language)
# print(result)
