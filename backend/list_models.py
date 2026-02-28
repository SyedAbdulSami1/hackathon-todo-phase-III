import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        models = response.json()
        for m in models.get("models", []):
            print(f"Model: {m['name']} - Methods: {m['supportedGenerationMethods']}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
