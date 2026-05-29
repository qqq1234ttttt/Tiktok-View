import requests
import re
import time
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def start_bot():
    print("=" * 45)
    print("      ZEFOY AUTOMATED VIEWS SCRIPT        ")
    print("=" * 45)
    
    print("\n[STEP 1] Input Zefoy Cookie")
    print("---------------------------------------")
    user_cookie = input("[?] Paste Cookie Here: ").strip()
    
    if not user_cookie:
        print("[!] Error: Cookie cannot be empty!")
        sys.exit()

    print("\n[STEP 2] Input TikTok Video URL")
    print("---------------------------------------")
    tiktok_url = input("[?] Enter TikTok Video Link: ").strip()
    
    if not tiktok_url:
        print("[!] Error: Video link cannot be empty!")
        sys.exit()

    headers = {
        'authority': 'zefoy.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': user_cookie,
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'origin': 'https://zefoy.com',
        'sec-fetch-site': 'same-origin',
    }

    session = requests.Session()
    session.headers.update(headers)

    print("\n[*] Checking session and cookie status...")
    try:
        response = session.get("https://zefoy.com/", verify=False, timeout=10)
        
        if "Enter Video URL" in response.text or "views" in response.text.lower():
            print("[+] Cookie is valid! Starting bot process...")
        else:
            print("\n[-] Error: Invalid or expired cookie!")
            print("[!] Please open Zefoy in browser, solve captcha, and get a new cookie.")
            sys.exit()

    except Exception as e:
        print(f"\n[x] Connection Error: {e}")
        sys.exit()

    while True:
        try:
            print("\n[*] Sending views request...")
            
            search_data = {'url': tiktok_url}
            res = session.post("https://zefoy.com/c2VuZC9mb2xsb3dlcnNfdGlrdG9r", data=search_data, verify=False)
            
            if "Successfully" in res.text:
                print("[>>>] Success: +1000 Views Sent!")
            else:
                print("[-] Failed: Still on cooldown or session locked.")
            
            print("[*] Cooldown: Waiting 5 minutes... (Do not close the script)")
            time.sleep(300)

        except KeyboardInterrupt:
            print("\n[!] Script stopped by user.")
            break
        except Exception as e:
            print(f"[-] An error occurred: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_bot()
