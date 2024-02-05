import os
import json
import yaml
from enum import Enum

from functools import reduce
from dataclasses import dataclass
from dataclasses import field
from gpt_pdf_organizer.domain.attribute import Attribute

from typing import Dict
from typing import Any
from typing import List
from typing import Optional

SEPARATOR_ALLOWED_CHARS = ["_", "-", " ", "."]

@dataclass
class OrganizerSettings:
    subfoldersFromAttributes: List[Attribute] = field(default_factory=list[Attribute.CONTENT_TYPE])
    filenameFromAttributes: List[Attribute] = field(default_factory=list[Attribute.TITLE])
    filenameAttributeSeparator: str = "-"

    def __post_init__(self):
        if self.filenameAttributeSeparator not in SEPARATOR_ALLOWED_CHARS:
            raise ValueError(f"Separator {self.separator} is not allowed. Please use one of {SEPARATOR_ALLOWED_CHARS}")

@dataclass
class Config:
    apiKey: str
    llmModelName: str
    organizer: OrganizerSettings
    maxNumTokens: int = 1000

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        if config is None:
            self._initialize({})
            return

        self._initialize(config)

    def load_from_file(self, config_file_path: str):

        with open(config_file_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        self._initialize(config)


    def _get(self, key: str, default: Optional[Any] = None):
        return reduce(lambda d, k: d.get(k, default) if isinstance(d, dict) else default, key.split("."), self)

    def _initialize(self, config: Dict[str, Any]):
        self.apiKey = config.get("apiKey", os.environ.get("OPENAI_API_KEY"))

        if self.apiKey is None:
            raise Exception("No API key found. Please set it in config.yaml or as environment variable OPENAI_API_KEY") 

        self.maxNumTokens = self._get("maxNumTokens", 100)
        self.llmModelName = self._get("llmModelName", "gpt-3.5-turbo")

        subfoldersFromAttributes = self._get("organizer.subfoldersFromAttributes", [])
        subfoldersFromAttributes = [Attribute(attr) for attr in subfoldersFromAttributes]

        filenameFromAttributes = self._get("organizer.filenameFromAttributes", [])
        filenameFromAttributes = [Attribute(attr) for attr in filenameFromAttributes]

        filenameAttributeSeparator = self._get("organizer.filenameAttributeSeparator", "-")

        self.organizer = OrganizerSettings(
            subfoldersFromAttributes=subfoldersFromAttributes,
            filenameFromAttributes=filenameFromAttributes,
            filenameAttributeSeparator=filenameAttributeSeparator
        )
