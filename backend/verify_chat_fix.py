import requests
import json
import uuid
import time

def test_chat():
    base_url = "http://localhost:8001" # Using the temporary backend
    
    # 1. Create a unique user
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "testpassword123"
    email = f"{username}@example.com"
    
    print(f"--- Step 1: Registering user {username} ---")
    reg_url = f"{base_url}/api/auth/register"
    reg_data = {
        "username": username,
        "email": email,
        "password": password,
        "full_name": "Test User"
    }
    
    try:
        reg_response = requests.post(reg_url, json=reg_data)
        print(f"Register Status: {reg_response.status_code}")
        if reg_response.status_code != 200:
            print(f"Register failed: {reg_response.text}")
            return
    except Exception as e:
        print(f"Connection failed (is the server on 8001 running?): {e}")
        return

    # 2. Login to get token
    print("\n--- Step 2: Logging in ---")
    login_url = f"{base_url}/api/auth/login"
    login_data = {
        "username": username,
        "password": password
    }
    # OAuth2 expects form data
    login_response = requests.post(login_url, data=login_data)
    print(f"Login Status: {login_response.status_code}")
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    auth_data = login_response.json()
    token = auth_data["token"]
    user_data = auth_data["user"]
    user_id = user_data["id"]
    print(f"Got token for user {user_id}")

    # 3. Test Chat
    print("\n--- Step 3: Testing Chat ---")
    chat_url = f"{base_url}/api/{user_id}/chat"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    chat_data = {
        "message": "Hello! List my tasks please.",
    }
    
    print(f"Sending message to {chat_url}...")
    chat_response = requests.post(chat_url, headers=headers, json=chat_data)
    print(f"Chat Status: {chat_response.status_code}")
    if chat_response.status_code == 200:
        print(f"Chat Response Body: {json.dumps(chat_response.json(), indent=2)}")
    else:
        print(f"Chat failed: {chat_response.text}")

if __name__ == "__main__":
    test_chat()
