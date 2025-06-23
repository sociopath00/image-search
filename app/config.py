from dotenv import load_dotenv
import os


load_dotenv("app/.env")

OPENAI_APIKEY = os.environ["OPENAI_APIKEY"]


