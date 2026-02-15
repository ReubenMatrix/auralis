import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR.parent / ".env"                
load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_SECRET_KEY = os.getenv("CLOUDINARY_API_SECRET")

settings = Settings()
