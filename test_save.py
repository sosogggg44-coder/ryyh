import requests, json

SUPA_URL = "https://amuopyagznrsyojqxaqp.supabase.co"
SUPA_KEY = "sb_publishable_VEEiRh3zLWxhzIwgJBcvLw_f0hABb0u"

def test_save():
    payload = {
        "author": "DEBUG_SYSTEM",
        "message": "Testing real-time sync visibility @ " + str(json.dumps(str(json.dumps("")))), # random unique string
        "youtube_id": "test_" + str(int(requests.get("https://www.google.com").elapsed.total_seconds() * 1000))
    }
    
    print(f"[*] Attempting to save test message to {SUPA_URL}...")
    try:
        res = requests.post(f"{SUPA_URL}/rest/v1/comments", 
                            headers={
                                "apikey": SUPA_KEY, 
                                "Authorization": f"Bearer {SUPA_KEY}", 
                                "Content-Type": "application/json", 
                                "Prefer": "return=minimal"
                            },
                            json=payload)
        
        if res.status_code in [200, 201, 204]:
            print(f"[+] Success! Status Code: {res.status_code}")
        else:
            print(f"[!] Failed! Status Code: {res.status_code}")
            print(f"[!] Response: {res.text}")
    except Exception as e:
        print(f"[!] Exception: {e}")

if __name__ == "__main__":
    test_save()
