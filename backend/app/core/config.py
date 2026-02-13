import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR.parent / ".env"                
load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
