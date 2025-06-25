import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # General Config
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # WhatsApp Cloud API
    WA_VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN")
    WA_ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN")
    WA_PHONE_ID = os.getenv("WA_PHONE_ID")

    # OpenAI API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Optional: MessageBird or any other service keys
    MESSAGEBIRD_API_KEY = os.getenv("MESSAGEBIRD_API_KEY", None)
