import requests, time, re, os, json

SUPA_URL = "https://amuopyagznrsyojqxaqp.supabase.co"
SUPA_KEY = "sb_publishable_VEEiRh3zLWxhzIwgJBcvLw_f0hABb0u"
VIDEO_ID = "6_9ZiuONXt0"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.youtube.com",
    "Referer": f"https://www.youtube.com/watch?v={VIDEO_ID}"
}

def get_yt_config():
    print(f"[*] Fetching YouTube config for {VIDEO_ID}...")
    try:
        r = requests.get(f"https://www.youtube.com/watch?v={VIDEO_ID}", headers=HEADERS, timeout=15)
        html = r.text
        key = (re.search(r'"INNERTUBE_API_KEY"\s*:\s*"([^"]+)"', html) or [None,None])[1]
        ver = (re.search(r'"clientVersion"\s*:\s*"([^"]+)"', html) or [None,"2.20240301"])[1]
        vis = (re.search(r'"visitorData"\s*:\s*"([^"]+)"', html) or [None,""])[1]
        patterns = [
            r'"invalidationContinuationData"\s*:\s*\{[^}]{0,300}?"continuation"\s*:\s*"([^"]+)"',
            r'"timedContinuationData"\s*:\s*\{[^}]{0,300}?"continuation"\s*:\s*"([^"]+)"',
            r'"continuation"\s*:\s*"([^"]{20,})"',
        ]
        cont = next((re.search(p, html).group(1) for p in patterns if re.search(p, html)), None)
        return key, ver, vis, cont
    except Exception as e:
        print(f"[!] Error: {e}")
        return None, None, None, None

def test_sync():
    key, ver, vis, cont = get_yt_config()
    if not cont:
        print("[!] Could not find continuation. Is the stream live?")
        return

    print(f"[+] Continuation found: {cont[:20]}...")
    try:
        r = requests.post(f"https://www.youtube.com/youtubei/v1/live_chat/get_live_chat?key={key}", 
                          json={"context":{"client":{"clientName":"WEB","clientVersion":ver,"visitorData":vis}}, "continuation":cont},
                          headers={"Content-Type":"application/json"}, timeout=10)
        data = r.json()
        actions = data.get("continuationContents",{}).get("liveChatContinuation",{}).get("actions",[])
        print(f"[*] Found {len(actions)} actions.")
        
        for a in actions:
            if "addChatItemAction" in a:
                item = a["addChatItemAction"].get("item", {})
                renderer = item.get("liveChatTextMessageRenderer", {})
                if renderer:
                    author = renderer.get("authorName",{}).get("simpleText","?")
                    txt = "".join(r.get("text","") for r in renderer.get("message",{}).get("runs",[]))
                    print(f"  [MSG] {author}: {txt}")
            elif "markChatItemAsDeletedAction" in a:
                target_id = a["markChatItemAsDeletedAction"].get("targetItemId")
                print(f"  [DEL] Target ID: {target_id}")
    except Exception as e:
        print(f"[!] Error during chat fetch: {e}")

if __name__ == "__main__":
    test_sync()
