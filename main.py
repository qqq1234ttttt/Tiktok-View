import requests
import re
import time
import sys
import urllib3
from urllib.parse import unquote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_clean_cookie(raw_cookie):
    """Extension မှရလာသော Cookie ထဲမှ nreer အတွက် လိုအပ်သော Cookie သီးသန့်ကို ခွဲထုတ်ခြင်း"""
    cookie_dict = {}
    parts = raw_cookie.split(';')
    for part in parts:
        if '=' in part:
            name, value = part.split('=', 1)
            name = name.strip()
            value = value.strip()
            if name not in ['useragent', '_uafec'] and name != '':
                cookie_dict[name] = value
                
    clean_str = "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])
    return clean_str

def start_bot():
    print("=" * 45)
    print("      KMT AUTOMATED VIEWS SCRIPT v3.1       ")
    print("=" * 45)
    
    print("\n[STEP 1] Input KMT Cookie (From FPlus Extension)")
    print("---------------------------------------")
    raw_cookie = input("[?] Paste Cookie Here: ").strip()
    
    if not raw_cookie:
        print("[!] Error: Cookie cannot be empty!")
        sys.exit()

    user_cookie = extract_clean_cookie(raw_cookie)

    print("\n[STEP 2] Input TikTok Video URL")
    print("---------------------------------------")
    tiktok_url = input("[?] Enter TikTok Video Link: ").strip()
    
    if not tiktok_url:
        print("[!] Error: Video link cannot be empty!")
        sys.exit()

    headers = {
        'host': 'nreer.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': user_cookie,
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'origin': 'https://nreer.com',
        'referer': 'https://nreer.com/dashboard',
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    session = requests.Session()
    session.headers.update(headers)

    print("\n[*] Checking KMT connection...")
    try:
        response = session.get("https://nreer.com/dashboard", verify=False, timeout=10)
        
        if "logout" in response.text.lower() or "dashboard" in response.text.lower() or "views" in response.text.lower():
            print("[+] Connected! Extension Cookie bypass successful.")
        else:
            print("\n[-] Error: Invalid or expired cookie!")
            print("[!] Please open nreer.com in browser, make sure you are in dashboard, and re-copy cookie.")
            sys.exit()

    except Exception as e:
        print(f"\n[x] Connection Error: {e}")
        sys.exit()

    while True:
        try:
            print("\n[*] Sending views request to KMT server...")
            
            post_data = {
                'url': tiktok_url,
                'loop_name': 'views'
            }
            
            res = session.post("https://nreer.com/api/send_views", data=post_data, verify=False)
            
            if "success" in res.text.lower() or "sent" in res.text.lower():
                print("[>>>] Success: Views Sent! Check your TikTok video.")
            elif "wait" in res.text.lower() or "seconds" in res.text.lower():
                print("[-] Failed: Cooldown is active or rate limit reached.")
            else:
                print("[-] Server response processed. Please verify on TikTok.")
            
            # Cooldown အချိန်ကို ၃ မိနစ် (၁၈၀ စက္ကန့်) သို့ လျှော့ချပြင်ဆင်ထားပါသည်
            print("[*] Cooldown: Waiting 3 minutes... (Do not close Termux)")
            time.sleep(180)

        except KeyboardInterrupt:
            print("\n[!] Script stopped by user.")
            break
        except Exception as e:
            print(f"[-] Error occurred: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_bot()
