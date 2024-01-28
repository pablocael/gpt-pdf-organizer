import os
import openai
import argparse

from gpt_pdf_organizer.app.application import Application
from gpt_pdf_organizer.infrastructure.gpt_prompt_querier import GPTPromptQuerier
from gpt_pdf_organizer.utils.config import LLM_MODEL_NAME
from gpt_pdf_organizer.utils.config import MAX_NUM_TOKENS
from gpt_pdf_organizer.utils.config import API_KEY

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, required=True)
    parser.add_argument("--output-folder", type=str, required=True)
    args = parser.parse_args()

    app = Application(
        prompt_querier=GPTPromptQuerier({
            "api_key": API_KEY,
            "model_name": LLM_MODEL_NAME,
            "max_tokens": MAX_NUM_TOKENS,
        })
    )

    app.organize(
        input_path=args.input_path,
        output_dir=args.output_folder,
    )
