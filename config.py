from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "eventease")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAM8sijmYSn8dUvNzx5YSPl6KebrkZjhvA")


# config.py

# from pydantic_settings import BaseSettings
# from fastapi_mail import ConnectionConfig

# class Settings(BaseSettings):
#     # ... your other settings like JWT_SECRET ...

#     # Add these new mail settings
#     MAIL_USERNAME: str
#     MAIL_PASSWORD: str
#     MAIL_FROM: str
#     MAIL_PORT: int
#     MAIL_SERVER: str
#     MAIL_STARTTLS: bool
#     MAIL_SSL_TLS: bool

#     class Config:
#         env_file = ".env"

# settings = Settings()

# # Create the mail connection configuration
# conf = ConnectionConfig(
#     MAIL_USERNAME = settings.MAIL_USERNAME,
#     MAIL_PASSWORD = settings.MAIL_PASSWORD,
#     MAIL_FROM = settings.MAIL_FROM,
#     MAIL_PORT = settings.MAIL_PORT,
#     MAIL_SERVER = settings.MAIL_SERVER,
#     MAIL_STARTTLS = settings.MAIL_STARTTLS,
#     MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
#     USE_CREDENTIALS = True,
#     VALIDATE_CERTS = True
# )