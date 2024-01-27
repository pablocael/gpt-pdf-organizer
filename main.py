import re
import yaml
import openai
import tiktoken
import argparse
import pdfplumber

GPT_MODEL_NAME = "gpt-3.5-turbo"

def first_words_within_k_tokens(text: str, k: int):

    # Tokenize the text
    word_count = 0
    token_count = 0

    words = text.split()
    encoder = tiktoken.encoding_for_model(GPT_MODEL_NAME)

    for i, word in enumerate(words):
        # Count the tokens for the current word

        word_tokens = len(encoder.encode((word)))

        # Check if adding this word exceeds the token limit
        if token_count + word_tokens > k:
            break

        # Add the word's tokens to the total count and increment word count
        token_count += word_tokens
        word_count += 1

    # Join the words that fit within the token and word limits
    selected_text = ' '.join(words[:word_count])
    return selected_text, token_count

def read_config():
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config.get("config", {})

def read_first_k_tokens(pdf_path: str, k: int):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        page_index = 0
        total_tokens = 0
        current_text = ""
        while True:
            page = pdf.pages[page_index]
            text = page.extract_text()
            text, token_count = first_words_within_k_tokens(text, k - total_tokens)
            current_text += text
            total_tokens += token_count

            if total_tokens >= k:
                break

            page_index += 1

    # Split text into words and get the first N words
    return current_text

def query_chatgpt(prompt):

    client = openai.OpenAI()

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",  # or the latest available model
      max_tokens=1000,
      messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message

if __name__ == "__main__":

    config = read_config()

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, required=True)
    args = parser.parse_args()

    max_num_tokens = config.get("maxNumTokens", 1000)
    openai.api_key = config.get("openaiApiKey", None)

    extracted_text = read_first_k_tokens(args.input_path, max_num_tokens)

    # Query ChatGPT
    prompt = f"Based on this text extract of the first {max_num_tokens} words of this PDF, what is the likely content type of this PDF, a Book, an Article or Other? If its a book, also answer the year of publication, otherwise the year should be 'Unknown'. Answer exactly one of the in the format (CONTENT_TYPE, YEAR, TITLE). The CONTENT_TYPE is one of (Book, Article or Other). Extract: '{extracted_text}'"
    print("ChatGPT's Prompt:", prompt)
    response = query_chatgpt(prompt)
    print("ChatGPT's Response:", response)
