import os
import requests
import json
from dotenv import load_dotenv
from pipeline_config import OPENAI_API_KEY_ENV

# 1. Setup
load_dotenv()
api_key = os.getenv(OPENAI_API_KEY_ENV)

# 2. Define the endpoint (Using standard OpenAI endpoint, which HDSI proxies)
url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# 3. Minimal cheap payload to check balance
payload = {
    "model": "gpt-4o-mini",  # Use the cheapest model for this check
    "messages": [{"role": "user", "content": "Hi"}],
    "max_tokens": 1
}

print("--- Checking Harvard HDSI Credit Balance ---")

try:
    response = requests.post(url, headers=headers, json=payload)
    
    # 4. Check for success
    if response.status_code == 200:
        data = response.json()
        
        # 5. Extract Custom Harvard Fields
        # The keys are explicitly named in your FAQ image
        used = data.get("your Harvard credits used this transaction", "N/A")
        remaining = data.get("your Harvard credits still available", "N/A")
        
        print(f"\n✅ Request Successful!")
        print(f"Credits Used This Call:   ${used}")
        print(f"Credits Remaining:        ${remaining}")
        
    elif response.status_code == 429:
        print(f"\n❌ Error 429: Rate Limit / Quota Exceeded")
        print("Diagnosis: You have likely run out of credits.")
        print("According to HDSI FAQ: 'Once the $ amount... has been reached... all subsequent API calls... receive a 429 error.'")
        
    else:
        print(f"\n⚠️ Unexpected Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"\n❌ Connection Error: {e}")
