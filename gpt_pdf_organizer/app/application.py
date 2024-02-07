"""
The main application use case class.
"""

import os
import json
import shutil
from typing import Dict
from typing import List
from typing import Optional

from gpt_pdf_organizer.service.prompt_querier import PromptQuerier
from gpt_pdf_organizer.utils.file import read_files_from_path
from gpt_pdf_organizer.domain.prompt_builder import build_query_from_content
from gpt_pdf_organizer.utils.pdf import read_pdf_page
from gpt_pdf_organizer.utils.config import Config

import logging

ACCEPTED_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

class Application:

    def __init__(self, config: Config, prompt_querier: PromptQuerier):
        """
        Initialize the application.
        """
        self.config = config
        self.prompt_querier = prompt_querier
        self._initialize_logger()

    def organize(self, input_path: str, output_dir: str):
        """
        Run the application.
        """

        self._initialize_output_dir(output_dir=output_dir)

        print("Using model", self.config.llmModelName)
        print("Using max_tokens", self.config.maxNumTokens)

        files = read_files_from_path(input_path, "pdf")
        self.logger.info("processing %d files from folder %s ...",
                         (len(files), input_path))

        # store files that could not be classified
        unclassified_files = []

        for file in files:
            self.logger.info("processing file %s ...", file)
            content = self._read_first_k_tokens_from_pdf(
                pdf_path=file, k=self.config.maxNumTokens)
            if content is None:
                self.logger.warning(
                    "could not extract content from file %s, skipping ...", file)
                unclassified_files.append(file)
                self._handle_unclassified_file(file, output_dir)
                continue

            self.logger.debug(f"extracted content from file {file}, content size is {len(content)}")
            prompt = build_query_from_content(content=content)
            response = self.prompt_querier.query(prompt)
            try:
                metadata = json.loads(response)
            except json.JSONDecodeError:
                self.logger.error("could not parse response from prompt, skipping ...")
                unclassified_files.append(file)
                self._handle_unclassified_file(file, output_dir)
                continue

            if metadata['title'].strip() == "null":
                self.logger.error("could not classify file %s, skipping ...", file)
                print("Could not classify file", file)
                self._handle_unclassified_file(file, output_dir)
                continue

            filename = self._build_filename_from_attribute_values(metadata)
            final_output_dir = os.path.join(output_dir, self.build_output_dir_from_attribute_values(metadata))
            os.makedirs(final_output_dir, exist_ok=True)

            dest = os.path.join(final_output_dir, filename + ".pdf")
            if self.config.organizer.moveInsteadOfCopy:
                print("Moving file", file, "to", dest)
                shutil.move(file, dest)
            else:
                print("Copying file", file, "to", dest)
                shutil.copy(file, dest)

    def _handle_unclassified_file(self, unclassified_file: str, output_dir: str):
        """
        Handle unclassified files.
        """
        unclassified_files_output_dir = os.path.join(output_dir, "unclassified")
        os.makedirs(unclassified_files_output_dir, exist_ok=True)
        if self.config.organizer.moveInsteadOfCopy:
            print("Moving unclassified file", unclassified_file, "to", unclassified_files_output_dir)
            shutil.move(unclassified_file, unclassified_files_output_dir)
        else:
            print("Copying unclassified file", unclassified_file, "to", unclassified_files_output_dir)
            shutil.copy(unclassified_file, unclassified_files_output_dir)

    def _initialize_log_folder(self, log_folder: str):
        """
        Initialize the log folder.
        """
        os.makedirs(log_folder, exist_ok=True)

    def _get_current_python_file_path(self) -> str:
        """
        Get the path of the current Python file.
        """
        return os.path.abspath(os.curdir)

    def _initialize_logger(self) -> logging.Logger:

        # initialize the log folder
        self._initialize_log_folder(log_folder=os.path.join(
            self._get_current_python_file_path(), 'logs'))

        # create a file stream handler
        self.logger = logging.getLogger(__name__)
        file_handler = logging.FileHandler(
            os.path.join(self._get_current_python_file_path(), 'logs', 'application.log'))
        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
        file_handler.setLevel(self.config.logLevel.upper())
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        return self.logger

    def _convert_to_snake_case(self, text: str) -> str:
        """
        Convert the given text to snake case.
        """
        value = text.lower().replace(" ", "_")
        for v in value:
            if v not in ACCEPTED_CHARACTERS:
                value = value.replace(v, "")

        return value

    def _read_first_k_tokens_from_pdf(self, pdf_path: str, k: int, limit_num_pages: int = 25) -> str:
        """
        Read the first k tokens from the given PDF file.
        """
        current_text = ""
        current_page = 0
        total_tokens_read = 0
        while True:
            text = read_pdf_page(pdf_path=pdf_path,
                                 page_index=current_page)
            if text is None:
                break

            text, num_tokens_read = self.prompt_querier.clamp_text_by_tokens(
                text=text, max_tokens=k - total_tokens_read)
            total_tokens_read += num_tokens_read
            current_text += text

            if total_tokens_read >= k:
                break

            if current_page >= limit_num_pages:
                return None

            current_page += 1

        return current_text

    def _initialize_output_dir(self, output_dir: str):
        """
        Initialize the output directory.
        """
        os.makedirs(output_dir, exist_ok=True)

    def _build_filename_from_attribute_values(self, attribute_values: Dict[str, str]) -> str:
        """
        Build a filename from the given attributes.
        """
        filename = ""
        attributes = self.config.organizer.filenameFromAttributes
        separator = self.config.organizer.filenameAttributeSeparator
        for i, attribute in enumerate(attributes):
            if attribute.name.lower() not in attribute_values:
                continue

            value = self._convert_to_snake_case(
                attribute_values[attribute.name.lower()])
            if value.strip() == "null":
                value = f"unknown_{attribute.name.lower()}"

            filename += value
            if i < len(attributes) - 1:
                filename += separator

        return filename

    def build_output_dir_from_attribute_values(self, attribute_values: Dict[str, str]) -> str:
        """
        Build an output directory from the given attributes.
        """
        output_dir = ""
        attributes = self.config.organizer.subfoldersFromAttributes
        for i, attribute in enumerate(attributes):
            value = self._convert_to_snake_case(
                attribute_values[attribute.name.lower()])
            if value.strip() == "null":
                value = f"unknown_{attribute.name.lower()}"

            output_dir = os.path.join(output_dir, value)

        return output_dir
