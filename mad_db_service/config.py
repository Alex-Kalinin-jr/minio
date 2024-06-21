import os
from dotenv import load_dotenv

load_dotenv()

TIMEZONE = os.getenv("TZ")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os. getenv("DB_PORT")
DB_DRIVER = os. getenv("DB_DRIVER")

DB_USER = os. getenv("POSTGRES_USER")
DB_PASSWORD = os. getenv("POSTGRES_PASSWORD")
DB_NAME = os. getenv("POSTGRES_DB")

DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"