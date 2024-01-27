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

GPT_MODEL_NAME = config.get("gptModelName")
GPT_API_KEY = os.environ.get("OPENAI_API_KEY", config.get("gptApiKey", ""))
MAX_NUM_TOKENS = config.get("maxNumTokens", 1000)
