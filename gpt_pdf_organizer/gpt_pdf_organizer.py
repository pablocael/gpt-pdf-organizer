#!/usr/bin/env python

import os
import openai
import argparse

from gpt_pdf_organizer.app.application import Application
from gpt_pdf_organizer.infrastructure.gpt_prompt_querier import GPTPromptQuerier
from gpt_pdf_organizer.utils.config import Config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, required=True)
    parser.add_argument("--output-folder", type=str, required=True)
    parser.add_argument("--config-file", type=str, required=False, default="./config.yaml")
    args = parser.parse_args()

    config = Config()
    config.load_from_file(args.config_file)

    print(config)

    app = Application(
        config=config,
        prompt_querier=GPTPromptQuerier({
            "api_key": config.apiKey,
            "model_name": config.llmModelName,
            "max_tokens": config.maxNumTokens,
        })
    )

    app.organize(
        input_path=args.input_path,
        output_dir=args.output_folder,
    )

if __name__ == "__main__":
    main()
