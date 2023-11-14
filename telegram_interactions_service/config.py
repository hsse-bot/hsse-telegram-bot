from dotenv import load_dotenv
import os

load_dotenv()
TOKEN_API = os.getenv("TG_TOKEN")
TUNNEL_URL = os.getenv("TUNNEL_URL")
WEB_APP_HOST = os.getenv("WEB_APP_HOST")
WEB_SERVER_PORT = os.getenv("WEB_SERVER_PORT")

WEBHOOK_PATH = "/{bot_token}"
WEBHOOK_URL = f"{TUNNEL_URL}{WEBHOOK_PATH}"
SECRET_KEY = os.getenv("SECRET_KEY")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")