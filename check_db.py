import requests, json

SUPA_URL = "https://amuopyagznrsyojqxaqp.supabase.co"
SUPA_KEY = "sb_publishable_VEEiRh3zLWxhzIwgJBcvLw_f0hABb0u"

def check_db():
    print(f"[*] Checking Supabase table 'comments'...")
    try:
        res = await_fetch = requests.get(f"{SUPA_URL}/rest/v1/comments?select=id,author,message,created_at&order=id.desc&limit=10", 
                            headers={"apikey": SUPA_KEY, "Authorization": f"Bearer {SUPA_KEY}"})
        
        if res.status_code == 200:
            data = res.json()
            print(f"[+] Found {len(data)} recent comments:")
            for row in data:
                # Sanitize for terminal
                author = row.get('author', '?').encode('ascii', 'ignore').decode('ascii')
                msg = row.get('message', '?').encode('ascii', 'ignore').decode('ascii')
                print(f"  [{row.get('id')}] {author}: {msg} ({row.get('created_at')})")
        else:
            print(f"[!] Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[!] Exception: {e}")

if __name__ == "__main__":
    check_db()
