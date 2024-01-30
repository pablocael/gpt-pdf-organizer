import os
import yaml
from functools import reduce

from typing import Dict
from typing import Any
from typing import List
from typing import Optional


# funtion to set in dict using string of keys separate by dot

class Config:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        if config is None:
            self._initialize({'config': {}})
            return

        self._initialize(config)

    def load(self, config_path: str):uuu

        with open("config.yaml", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        self._initialize(config)

    def _initialize(self, config: Dict[str, Any]):

        assert "config" in config, "'config' key must be present in config file as parent of all other keys"

        self.config = config
        self._fill_defaults(config.get("config", {}))

    def get(self, composite_access_key: str, default: Any = None):
        map_list = composite_access_key.split(".")
        return reduce(lambda d, k: d.get(k, default) if isinstance(d, dict) else default, map_list, self.config)
    
    def set(self, keys, value):
        parent = self._get_parent(keys)
        d[last_key] = value

    def _get_parent(self, keys):
        keys = keys.split(".")
        last_key = keys.pop()
        d = self.config
        for key in keys:
            d = d.setdefault(key, {})
        return d

    def _set_default(self, keys, value):
        parent = self._get_parent(keys)
        parent.setdefault(last_key, value)

    def _fill_defaults(config):
        self._set_default("llmModelName", "gpt-3.5-turbo")
        self._set_default("maxNumTokens", 1000)
        self._set_default("organizer.subfoldersFromAttributes", ["content_type"])
        self._set_default("organizer.filenameFromAttributes", ["title"])
        self._set_default("organizer.attributesSeparator", "-")

        # filter invalid subfolder attributes
        subfolders_from_attributes = [x for x in self.get("organizer.subfoldersFromAttributes") if x in ["content_type", "author", "year"]]
        self.set("organizer.subfoldersFromAttributes", subfolders_from_attributes)

        # filter invalid filename attributes
        filenames_from_attributes = [x for x in self.get("organizer.filenameFromAttributes") if x in ["content_type", "title", "author", "year"]]
        if "title" not in filenames_from_attributes:
            filenames_from_attributes.append("title")
        self.set("organizer.filenameFromAttributes", filenames_from_attributes)

        # filter invalid separators
        attributes_separator = "".join(x for x in self.get("organizer.attributesSeparator") if x in ["-", "_", "."])
        self.set("organizer.attributesSeparator", attributes_separator)

        env_api_key = os.environ.get("OPENAI_API_KEY")
        if env_api_key is not None:
            self.set("apiKey", env_api_key)

