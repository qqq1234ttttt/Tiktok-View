import requests
import re
import time
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def start_bot():
    print("=" * 45)
    print("      KMT AUTOMATED VIEWS SCRIPT            ")
    print("=" * 45)
    
    print("\n[STEP 1] Input KMT Cookie")
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
        'authority': 'nreer.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': user_cookie,
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'origin': 'https://nreer.com',
        'referer': 'https://nreer.com/dashboard',
        'x-requested-with': 'XMLHttpRequest'
    }

    session = requests.Session()
    session.headers.update(headers)

    print("\n[*] Checking KMT connection...")
    try:
        response = session.get("https://nreer.com/dashboard", verify=False, timeout=10)
        
        if "logout" in response.text.lower() or "dashboard" in response.text.lower():
            print("[+] Cookie is valid! Connected to KMT Dashboard.")
        else:
            print("\n[-] Error: Invalid or expired cookie!")
            print("[!] Please login again, solve captcha, and get a new cookie.")
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
                print("[-] Failed: Cooldown is active. Need to wait.")
            else:
                print("[-] Failed: Request rejected by KMT Server. (Session expired or Security trigger)")
            
            print("[*] Cooldown: Waiting 5 minutes... (Do not close Termux)")
            time.sleep(300)

        except KeyboardInterrupt:
            print("\n[!] Script stopped by user.")
            break
        except Exception as e:
            print(f"[-] Error occurred: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_bot()
