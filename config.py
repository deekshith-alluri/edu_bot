from dotenv import load_dotenv
import os

load_dotenv()

_MODEL_API_KEY = os.environ.get("GOOGLE_API_KEY")
_YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
_DB_ADDR = os.environ.get("DB_ADDR")
_SECRET_KEY_FLASK = os.environ.get("FLASK_SECRET_KEY")
