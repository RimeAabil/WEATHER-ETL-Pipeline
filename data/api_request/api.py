import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Look for .env in current directory or project root
load_dotenv() # System env take precedence
env_path = Path(__file__).resolve().parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).resolve().parents[1] / ".env"
if not env_path.exists():
    env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(env_path)

api_url = os.getenv("API_URL")
api_key = os.getenv("WEATHER_STACK_API")

def fetch_data():
    print("Fetching weather data from WeatherStack ...")
    try:
        response = requests.get(
            api_url,
            params={
            "access_key": api_key,
            "query": "New York"
            },
        timeout=10
        )
        response.raise_for_status()
        print("API response retreived successfully")
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")
        return None


def fetch_mock_data():
    return {
        'request': {'type': 'City', 'query': 'New York, '
    'United States of America', 'language': 'en', 
    'unit': 'm'},
        'location': {'name': 'New York', 
                               'country': 'United States of America', 
                               'region': 'New York', 'lat': '40.714', 
                               'lon': '-74.006', 'timezone_id': 'America/New_York', 
                               'localtime': '2026-01-27 07:53', 'localtime_epoch': 1769500380,
                                 'utc_offset': '-5.0'},

        'current': {'observation_time': '12:53 PM', 
                                             'temperature': -9, 'weather_code': 113, 
                                             'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'], 
                                             'weather_descriptions': ['Clear '], 'astro': {'sunrise': '07:11 AM', 'sunset': '05:08 PM', 'moonrise': '11:32 AM',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
                                            'moonset': '02:06 AM', 'moon_phase': 'Waxing Gibbous', 'moon_illumination': 59}, 
                                            'air_quality': {'co': '301.85', 'no2': '18.35', 'o3': '62', 'so2': '8.35', 'pm2_5': '15.35', 'pm10': '15.45', 'us-epa-index': '1', 'gb-defra-index': '1'},
                                            'wind_speed': 17, 'wind_degree': 261, 'wind_dir': 'W', 'pressure': 1020, 'precip': 0, 'humidity': 48, 'cloudcover': 0, 'feelslike': -16, 'uv_index': 0, 'visibility': 16, 'is_day': 'yes'}}