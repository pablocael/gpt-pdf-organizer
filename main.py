import os
import openai
import argparse

from gpt_pdf_organizer.utils.config import read_config
from gpt_pdf_organizer.utils.gpt import query_chatgpt
from gpt_pdf_organizer.utils.gpt import build_query_from_content
from gpt_pdf_organizer.utils.pdf import read_first_k_tokens_from_pdf
from gpt_pdf_organizer.utils.config import GPT_API_KEY
from gpt_pdf_organizer.utils.config import MAX_NUM_TOKENS

if __name__ == "__main__":

    config = read_config()
    max_num_tokens = MAX_NUM_TOKENS
    openai.api_key = GPT_API_KEY

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, required=True)
    parser.add_argument("--output-folder", type=str, required=True)
    args = parser.parse_args()

    extracted_text = read_first_k_tokens_from_pdf(pdf_path=args.input_path, k=max_num_tokens)
    prompt = build_query_from_content(extracted_text)
    print("Prompt:", prompt)

    # Query ChatGPT
    # response = query_chatgpt(prompt)
    # print("ChatGPT's Response:", response)
