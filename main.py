import base64
import os
import sys
import ssl
import re
import time
import random
import threading
import requests
import hashlib
import json
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar

# pystyle handling
try:
    from pystyle import Colorate, Colors, Center, Write, Col
except ImportError:
    print("[-] 'pystyle' library package မရှိသေးပါ။ 'pip install pystyle' ဖြင့် အရင်သွင်းပါ။")
    sys.exit(1)

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

r = requests.Session()
r.cookies.set_policy(BlockCookies())

class Gorgon:
    def __init__(self, params: str, data: str, cookies: str, unix: int) -> None:
        self.unix = unix
        self.params = params
        self.data = data
        self.cookies = cookies

    def hash(self, data: str) -> str:
        try:
            _hash = str(hashlib.md5(data.encode()).hexdigest())
        except Exception:
            _hash = str(hashlib.md5(data).hexdigest())
        return _hash

    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str = base_str + self.hash(self.data) if self.data else base_str + str('0' * 32)
        base_str = base_str + self.hash(self.cookies) if self.cookies else base_str + str('0' * 32)
        return base_str

    def get_value(self) -> dict:
        base_str = self.get_base_string()
        return self.encrypt(base_str)

    def encrypt(self, data: str) -> dict:
        unix = self.unix
        length = 20
        key = [223, 119, 185, 64, 185, 155, 132, 131, 209, 185, 203, 209, 247, 194, 185, 133, 195, 208, 251, 195]
        param_list = []

        for i in range(0, 12, 4):
            temp = data[8 * i:8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2:(j + 1) * 2], 16)
                param_list.append(H)

        param_list.extend([0, 6, 11, 28])
        H = int(hex(unix), 16)
        param_list.append((H & 4278190080) >> 24)
        param_list.append((H & 16711680) >> 16)
        param_list.append((H & 65280) >> 8)
        param_list.append((H & 255) >> 0)
        eor_result_list = []

        for (A, B) in zip(param_list, key):
            eor_result_list.append(A ^ B)

        for i in range(length):
            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % length]
            E = C ^ D
            F = self.rbit_algorithm(E)
            H = (F ^ 4294967295 ^ length) & 255
            eor_result_list[i] = H

        result = ''
        for param in eor_result_list:
            result += self.hex_string(param)

        return {'X-Gorgon': '0404b0d30000' + result, 'X-Khronos': str(unix)}

    def rbit_algorithm(self, num):
        result = ''
        tmp_string = bin(num)[2:]
        while len(tmp_string) < 8:
            tmp_string = '0' + tmp_string
        for i in range(0, 8):
            result = result + tmp_string[7 - i]
        return int(result, 2)

    def hex_string(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2:
            tmp_string = '0' + tmp_string
        return tmp_string

    def reverse(self, num):
        tmp_string = self.hex_string(num)
        return int(tmp_string[1:] + tmp_string[:1], 16)

def send(did, iid, cdid, openudid):
    global reqs, _lock, __aweme_id
    for x in range(10):  
        try:  
            params  = f"device_id={did}&iid={iid}&device_type=SM-G973N&app_name=musically_go&host_abi=armeabi-v7a&channel=googleplay&device_platform=android&version_code=160904&device_brand=samsung&os_version=9&aid=1340"  
            payload = f"item_id={__aweme_id}&play_delta=1"  
            sig     = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()  

            # ၅ စက္ကန့်အတွင်း Response မပြန်ရင် ပိတ်သွားအောင် timeout ထည့်ထားသည်
            response = requests.post(  
                url = ("https://api16-va.tiktokv.com/aweme/v1/aweme/stats/?" + params),  
                data    = payload,  
                headers = {
                    'cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47',
                    'x-gorgon': sig['X-Gorgon'],
                    'x-khronos': sig['X-Khronos'],
                    'user-agent': 'okhttp/3.10.0.1'
                },  
                verify  = False,
                timeout = 5
            )  
              
            try:  
                reqs += 1  
                _lock.acquire()  
                print(Colorate.Horizontal(Colors.green_to_white, f"+ - sent views {response.json()['log_pb']['impr_id']} {__aweme_id} {reqs}"))  
                _lock.release()  
            except Exception as inner_e:  
                if _lock.locked():
                    _lock.release()
                print(f"[-] Response Read Error: {inner_e} | Raw Response: {response.text[:100]}")
                continue  
        except Exception as e:  
            # Loading မှာ ရပ်မနေစေရန် Background Error များကို ဖော်ပြပေးမည့်နေရာ
            print(f"[-] Thread Network Error: {e}")

def rpsm_loop():
    global rps, rpm, reqs
    while True:
        initial = reqs
        time.sleep(1.5)
        rps = round((reqs - initial) / 1.5, 1)
        rpm = round(rps * 60, 1)

if __name__ == "__main__":
    os.system("clear")

    txt = """\n\n╭╮╱╱╭━━━┳━╮╱╭┳━━━╮╭━━╮╭━━━┳━━━━╮\n┃┃╱╱┃╭━╮┃┃╰╮┃┃╭━╮┃┃╭╮┃┃╭━╮┃╭╮╭╮┃\n┃┃╱╱┃┃╱┃┃╭╮╰╯┃┃╱┃┃┃╰╯╰┫┃╱┃┣╯┃┃╰╯\n┃┃╱╭┫╰━╯┃┃╰╮┃┃╰━╯┃┃╭━╮┃┃╱┃┃╱┃┃\n┃╰━╯┃╭━╮┃┃╱┃┃┃╭━╮┃┃╰━╯┃╰━╯┃╱┃┃\n╰━━━┻╯╱╰┻╯╱╰━┻╯╱╰╯╰━━━┻━━━╯╱╰╯\n"""
    print(Colorate.Vertical(Colors.DynamicMIX((Col.light_green, Col.purple)), Center.XCenter(txt)))

    try:  
        # Termux မှာ ပိတ်မနေအောင် ပုံမှန် input အဖြစ် ပြောင်းလဲထားသည်
        link = input("\n\n            ? = Link Tiktok > ")
        if len(re.findall(r"(\d{18,19})", link)) == 1:
            __aweme_id = str(re.findall(r"(\d{18,19})", link)[0])
        else:
            print("[*] Link ကို စစ်ဆေးနေပါသည်...")
            __aweme_id = str(re.findall(r"(\d{18,19})", requests.head(link, allow_redirects=True, timeout=5).url)[0])
    except Exception as e:  
        print(f"\n[x] Invalid link သို့မဟုတ် Link ဖတ်မရပါ: {e}")  
        sys.exit(0)  
      
    print("\n[+] Starting Bot...")  
      
    _lock = threading.Lock()  
    reqs = 0  
    rpm = 0  
    rps = 0  
      
    threading.Thread(target=rpsm_loop, daemon=True).start()  

    # devices.txt စစ်ဆေးခြင်း
    if not os.path.exists('devices.txt'):
        print("[!] Error: 'devices.txt' file မရှိပါ။ အရင်ဆောက်ပေးပါ။")
        sys.exit(1)

    with open('devices.txt', 'r') as f:
        devices = f.read().splitlines()  
    
    if not devices or len(devices) == 0:
        print("[!] Error: 'devices.txt' ထဲမှာ ဘာ data မှ မရှိပါ။")
        sys.exit(1)

    print(f"[+] Device {len(devices)} ခု တွေ့ရှိပြီး စတင်ပတ်နေပါပြီ။\n")

    while True:  
        device = random.choice(devices)  
        if not device.strip():
            continue
            
        if threading.active_count() < 100:  
            try:
                did, iid, cdid, openudid = device.split(':')  
                threading.Thread(target=send, args=[did, iid, cdid, openudid]).start()
            except ValueError:
                print(f"[-] 'devices.txt' ထဲက ဒီစာကြောင်း ပုံစံမမှန်ပါ -> {device}")
                continue
        time.sleep(0.1) # Termux Crash မဖြစ်စေရန် စက္ကန့်ပိုင်း ထိန်းထားသည်
