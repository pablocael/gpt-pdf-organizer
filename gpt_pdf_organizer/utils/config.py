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
    moveInsteadOfCopy: bool = False

    def __post_init__(self):
        if self.filenameAttributeSeparator not in SEPARATOR_ALLOWED_CHARS:
            raise ValueError(f"Separator {self.separator} is not allowed. Please use one of {SEPARATOR_ALLOWED_CHARS}")

    def __str__(self):
        return self.toJSON()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

@dataclass
class Config:
    apiKey: str
    llmModelName: str
    maxNumTokens: int
    logLevel: str
    organizer: OrganizerSettings

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        if config is None:
            self._initialize({})
            return

        self._initialize(config)

    def __str__(self):
        return self.toJSON()

    def toJSON(self):
        return json.dumps(self.config, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def load_from_file(self, config_file_path: str):

        with open(config_file_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        self._initialize(config)

        return self


    def _raw_get(self, key: str, default: Optional[Any] = None):
        return reduce(lambda d, k: d.get(k, default) if isinstance(d, dict) else default, key.split("."), self.config)

    def _initialize(self, config: Dict[str, Any]):
        self.config = config
        self.apiKey = config.get("apiKey", os.environ.get("OPENAI_API_KEY"))

        if self.apiKey is None:
            raise Exception("No API key found. Please set it in config.yaml or as environment variable OPENAI_API_KEY") 

        self.logLevel = self._raw_get("logLevel", "INFO")
        self.maxNumTokens = self._raw_get("maxNumTokens", 100)
        self.llmModelName = self._raw_get("llmModelName", "gpt-3.5-turbo")

        subfoldersFromAttributes = self._raw_get("organizer.subfoldersFromAttributes", [])
        subfoldersFromAttributes = [Attribute(attr) for attr in subfoldersFromAttributes]

        filenameFromAttributes = self._raw_get("organizer.filenameFromAttributes", [])
        filenameFromAttributes = [Attribute(attr) for attr in filenameFromAttributes]

        filenameAttributeSeparator = self._raw_get("organizer.filenameAttributeSeparator", "-")

        self.organizer = OrganizerSettings(
            subfoldersFromAttributes=subfoldersFromAttributes,
            filenameFromAttributes=filenameFromAttributes,
            filenameAttributeSeparator=filenameAttributeSeparator,
            moveInsteadOfCopy=self._raw_get("organizer.moveInsteadOfCopy", False)
        )
