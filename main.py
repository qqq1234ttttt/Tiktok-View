import requests
import re
import time
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def start_bot():
    print("=" * 45)
    print("      ZEFOY BOT VERSION 2 (AUTO-ENDPOINT)   ")
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'origin': 'https://zefoy.com',
        'referer': 'https://zefoy.com/',
    }

    session = requests.Session()
    session.headers.update(headers)

    print("\n[*] Checking Zefoy connection...")
    try:
        response = session.get("https://zefoy.com/", verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Zefoy ရဲ့ လက်ရှိ Views ပို့ပေးနေတဲ့ Form Key အမှန်ကို ရှာခြင်း
        view_form = soup.find('input', {'placeholder': 'Enter Video URL'})
        endpoint = "c2VuZC9mb2xsb3dlcnNfdGlrdG9r" # Default
        
        # Form ထဲက သီးသန့် ID တွေကို ရှာဖွေခြင်း
        forms = soup.find_all('form', action=True)
        for form in forms:
            if "views" in form.text.lower() or "c2Vu" in form['action']:
                endpoint = form['action']
                break

        if "Enter Video URL" in response.text or "views" in response.text.lower():
            print(f"[+] Connected! Using Dynamic Endpoint: {endpoint}")
        else:
            print("\n[-] Error: Session Blocked by Cloudflare Captcha!")
            print("[!] Please solve captcha in your browser first, then copy new cookie.")
            sys.exit()

    except Exception as e:
        print(f"\n[x] Connection Error: {e}")
        print("[!] Tip: Please run 'pip install beautifulsoup4' if error occurs.")
        sys.exit()

    while True:
        try:
            print("\n[*] Sending views request to server...")
            
            # Zefoy က ကာကွယ်ထားတဲ့ Token စနစ်ကို တိုက်ရိုက်ဖတ်ပြီး ပို့ခြင်း
            search_data = {'url': tiktok_url}
            res = session.post(f"https://zefoy.com/{endpoint}", data=search_data, verify=False)
            
            if "Successfully" in res.text or "views sent" in res.text.lower():
                print("[>>>] Success: Views Sent! Check your TikTok video now.")
            elif "seconds" in res.text.lower():
                # စောင့်ရမယ့် မိနစ်ကို စာသားထဲကနေ ရှာပြခြင်း
                remain = re.findall(r'(\d+)\s+seconds', res.text.lower())
                time_wait = remain[0] if remain else "300"
                print(f"[-] Cooldown Active: Need to wait {time_wait} seconds.")
            else:
                print("[-] Failed: Zefoy Server rejected the request. (Captcha/Session Lock)")
            
            print("[*] Sleeping for Cooldown... (Do not close Termux)")
            time.sleep(180) # ၃ မိနစ် စောင့်ပြီး ပြန်ပတ်မည်

        except KeyboardInterrupt:
            print("\n[!] Script stopped.")
            break
        except Exception as e:
            print(f"[-] Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_bot()
