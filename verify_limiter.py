import requests
import time

URL = "http://127.0.0.1:8008/"

print(f"🚀 Testing Rate Limiter at {URL}")
print("Sending 105 requests (Limit is 100/minute)...")

for i in range(1, 106):
    try:
        response = requests.get(URL)
        if response.status_code == 429:
            print(f"\n✅ Limit triggered at request #{i}!")
            print(f"Response: {response.json()}")
            break
        else:
            print(f".", end="", flush=True)
    except Exception as e:
        print(f"\n❌ Request failed: {e}")
        break

if response.status_code != 429:
    print("\n❌ Failed to trigger rate limit.")
