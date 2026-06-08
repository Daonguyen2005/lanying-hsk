from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_SERVER = os.getenv("DB_SERVER", "(local)")
DB_NAME = os.getenv("DB_NAME", "LanyingHSK")
DB_USERNAME = os.getenv("DB_USERNAME", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")

SECRET_KEY = os.getenv("SECRET_KEY", "lanying-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

DATABASE_URL = "sqlite:///./lanyinghsk.db"
