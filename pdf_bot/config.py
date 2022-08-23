import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.



class Config:
    BOT_TOKEN = os.environ["BOT_TOKEN"]  # from @botfather
    API_ID = int(os.environ["API_ID"])  # from https://my.telegram.org/apps
    API_HASH = os.environ["API_HASH"]  # from https://my.telegram.org/apps
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
