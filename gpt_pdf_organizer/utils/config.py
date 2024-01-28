import os
import yaml

def fill_defaults(config):
    config.setdefault("gptModelName", "gpt-3.5-turbo")
    return config

def read_config():
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return fill_defaults(config.get("config", {}))

config = read_config()

LLM_MODEL_NAME = config.get("llmModelName")
API_KEY = os.environ.get("OPENAI_API_KEY", config.get("apiKey", ""))
MAX_NUM_TOKENS = config.get("maxNumTokens", 1000)
SUBFOLDERS_FROM_ATTRIBUTES = config.get("organizer",{}).get("subfoldersFromAttributes", ["content_type"])
FILENAMES_FROM_ATTRIBUTES = config.get("organizer",{}).get("filenameFromAttributes", [])
FILENAMES_FROM_ATTRIBUTES = FILENAMES_FROM_ATTRIBUTES if FILENAMES_FROM_ATTRIBUTES else ["title"]
ATTRIBUTES_SEPARATOR = "".join(x for x in config.get("organizer",{}).get("attributesSeparator", "-") if x.isalnum())
