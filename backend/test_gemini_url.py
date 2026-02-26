import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
model = "gemini-1.5-flash"

urls = [
    "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
    "https://generativelanguage.googleapis.com/v1/openai/chat/completions",
]

for url in urls:
    print(f"\nTesting URL: {url}")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "Say hello"}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
