from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    pipeline,
)
import os


# Check if our fine_tuned Distilbert model exists and is in the right location which should be back/Distilbert
def check_if_Distilbert_model_exists():
    folder_path = "./Distilbert"
    if os.path.exists(folder_path):
        return True
    else:
        return False


# Determine which model to use based on the source language
def determineModelUsage(source_language):

    if source_language == "English" and check_if_Distilbert_model_exists():
        try:
            # Initialize the tokenizer for our model
            our_model_tokenizer = DistilBertTokenizer.from_pretrained(
                "./Distilbert/tokenizer_distilbert_finetuned/", local_files_only=True
            )
            model = DistilBertForSequenceClassification.from_pretrained(
                "./Distilbert/", local_files_only=True
            )
            tokenizer = our_model_tokenizer
            custom_model_load_failed_message = ""
        except:
            # Initialize the tokenizer and the model only once to avoid reloading them multiple times.
            tokenizer = DistilBertTokenizer.from_pretrained(
                "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
            )
            model = pipeline(
                "sentiment-analysis",
                model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
            )
            custom_model_load_failed_message = "Path to folder existed and source lang was english but Custom model load failed, using default model. Check if all files are present in the Distilbert folder."
    elif source_language == "English" and not check_if_Distilbert_model_exists():
        # Initialize the tokenizer and the model only once to avoid reloading them multiple times.
        tokenizer = DistilBertTokenizer.from_pretrained(
            "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        )
        model = pipeline(
            "sentiment-analysis",
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
        )
        custom_model_load_failed_message = "Path to custom Distilbert folder did not exist and source lang was english, using default model."

    else:
        # Initialize the tokenizer and the model only once to avoid reloading them multiple times.
        tokenizer = DistilBertTokenizer.from_pretrained(
            "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        )
        model = pipeline(
            "sentiment-analysis",
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
        )
        custom_model_load_failed_message = ""

    return model, tokenizer, custom_model_load_failed_message


def chunk_text(text, tokenizer, max_token_count=512):  # Leave space for special tokens
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


# Sentiment Analysis on the story to determine if the story is positive or negative
def sentiment_analysis(text, source_language):
    model, tokenizer, custom_model_load_failed_message = determineModelUsage(
        source_language
    )
    if custom_model_load_failed_message == "":
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
        return {
            "sentiment": sentiment,
            "score": score,
        }, custom_model_load_failed_message
    else:
        chunks = chunk_text(text, tokenizer)
        total_score = 0
        total_tokens = 0
        for chunk in chunks:
            # Process each chunk with the model and collect results
            result = model(chunk)[
                0
            ]  # Assuming each chunk returns a single sentiment analysis result
            chunk_tokens = tokenizer.encode(chunk, add_special_tokens=True)
            num_tokens = len(chunk_tokens)
            total_tokens += num_tokens
            score = (
                result["score"]
                if result["label"] == "POSITIVE"
                else (1 - result["score"])
            )
            total_score += (
                score * num_tokens
            )  # Weight score by number of tokens in the chunk

        average_score = total_score / total_tokens
        sentiment = "positive" if average_score >= 0.5 else "negative"
        return {
            "sentiment": sentiment,
            "score": average_score,
        }, custom_model_load_failed_message
