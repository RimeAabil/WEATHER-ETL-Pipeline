import requests
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(env_path)

api_url = os.getenv("API_URL")
api_key = os.getenv("WEATHER_STACK_API")


print("API_URL =", api_url)
print("API_KEY =", api_key)
