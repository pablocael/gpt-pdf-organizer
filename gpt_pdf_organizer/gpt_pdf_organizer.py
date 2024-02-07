#!/usr/bin/env python

import os
import time
import openai
import argparse

from gpt_pdf_organizer.app.application import Application
from gpt_pdf_organizer.infrastructure.gpt_prompt_querier import GPTPromptQuerier
from gpt_pdf_organizer.utils.config import Config
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, required=True)
    parser.add_argument("--output-folder", type=str, required=True)
    parser.add_argument(
        "--config-file", type=str, required=False, default="./config.yaml"
    )
    args = parser.parse_args()

    config = Config()
    config.load_from_file(args.config_file)

    app = Application(
        config=config,
        prompt_querier=GPTPromptQuerier(
            {
                "api_key": config.apiKey,
                "model_name": config.llmModelName,
                "max_tokens": config.maxNumTokens,
            }
        ),
    )

    # Define a custom progress bar layout
    progress = Progress(
        TextColumn("[bold]{task.description}"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        expand=True
    )

    with progress:
        progress.print()
        progress.print(f"[blue]---------------------------------------------------------------------------") 
        progress.print(f"[blue]GPT PDF file organizer")
        progress.print(f"[blue]---------------------------------------------------------------------------") 
        progress.print(f"[blue]source path:      {args.input_path}'")
        progress.print(f"[blue]output path:      {os.path.abspath(args.output_folder)}")
        progress.print(f"[blue]using model:      {config.llmModelName}")
        progress.print(f"[blue]using max tokens: {config.maxNumTokens}")
        progress.print(f"[blue]---------------------------------------------------------------------------") 
        progress.print()

        total_processed = 0
        task = progress.add_task("[red]processing files...", total=100)
        for _ in app.organize(
            input_path=args.input_path,
            output_dir=args.output_folder,
        ):
            task_error = app.get_error()
            task_progress = app.get_progress()
            task_message = app.get_process_message()
            # Simulate some work and update progress
            progress.print(f"[{'green' if not task_error else 'red'}]{task_message}")
            progress.update(task, completed=task_progress, refresh=True)
            total_processed += 1

        progress.update(task, description=f"[green]done processing {total_processed} files", completed=100, refresh=True)
if __name__ == "__main__":
    main()


