import os

from dotenv import load_dotenv

load_dotenv()


class Creds:
    USERNAME = os.getenv("U_NAME")
    APP_PASSWORD = os.getenv("APP_PASSWORD")
