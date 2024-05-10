import openai

from config_reader import config

api_key = config.OPENAI_API_KEY.get_secret_value()
openai.api_key = api_key