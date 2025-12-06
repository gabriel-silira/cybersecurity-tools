from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse
import socket
import requests
import random
import string

# funções
def _load_wordlist(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {path}")
        return []

def _resolve_host(host: str):
    try:
        return socket.gethostbyname(host)
    except Exception:
        return None

def _http_head(host: str, timeout: int = 4):
    for scheme in ("https://", "http://"):
        url = scheme + host
        try:
            r = requests.head(url, timeout=timeout, allow_redirects=True)
            return r.status_code
        except Exception:
            continue
    return None

def _http_get(url: str, timeout: int = 4):
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True)
        return r.status_code, len(r.content)
    except Exception:
        return None, 0

def _normalize_domain(domain: str):
    if not domain:
        return ""
    d = domain.strip()
    if d.startswith("http://") or d.startswith("https://"):
        d = urlparse(d).netloc
    return d.strip().strip("/")

def _random_token(n=20):
    import random, string
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))

# wildcard check
def _detect_wildcard(domain: str, tries: int = 2):
    ips = set()
    resolved = 0
    for _ in range(tries):
        candidate = f"{_random_token()}.{domain}"
        ip = _resolve_host(candidate)
        if ip:
            ips.add(ip)
            resolved += 1
    return (resolved > 0, list(ips))

# scan de subdomains
def scan_subdomains(domain: str, lists_dir: str = "listas", workers: int = 25, timeout: int = 4, do_http: bool = True):
    domain = _normalize_domain(domain)
    if not domain:
        print("[ERRO] Domínio inválido para scan_subdomains.")
        return []

    base = Path(__file__).parent / lists_dir
    subs = _load_wordlist(base / "subdomains.txt")
    results = []

    if not subs:
        print(f"[ERRO] Nenhum subdomínio carregado de {base / 'subdomains.txt'}")
        return results

    wildcard, ips = _detect_wildcard(domain, tries=2)
    if wildcard:
        results.append({"host": "__WILDCARD_DETECTED__", "ip": ",".join(ips), "http_status": None})
        print(f"[AVISO] Possível wildcard DNS detectado para {domain} (IPs: {ips}).")

    with ThreadPoolExecutor(max_workers=max(4, workers)) as exe:
        futures = {exe.submit(_resolve_host, f"{sub}.{domain}"): sub for sub in subs}
        for fut in as_completed(futures):
            sub = futures[fut]
            ip = fut.result()
            if ip:
                host = f"{sub}.{domain}"
                status = None
                if do_http:
                    status = _http_head(host, timeout=timeout)
                results.append({"host": host, "ip": ip, "http_status": status})
                print(f"[+] {host} -> {ip}  HTTP: {status}")
    return results

# scan de paths
def scan_paths(base: str, lists_dir: str = "listas", workers: int = 25, timeout: int = 4):
    if not base:
        print("[ERRO] Base inválida para scan_paths.")
        return []

    if not urlparse(base).scheme:
        base = "https://" + _normalize_domain(base)
    else:
        parsed = urlparse(base)
        base = f"{parsed.scheme}://{parsed.netloc}"

    lists_path = Path(__file__).parent / lists_dir
    paths = _load_wordlist(lists_path / "paths.txt")
    results = []

    if not paths:
        print(f"[ERRO] Nenhum path carregado de {lists_path / 'paths.txt'}")
        return results

    with ThreadPoolExecutor(max_workers=max(4, workers)) as exe:
        futures = {}
        for p in paths:
            target = urljoin(base.rstrip("/") + "/", p.lstrip("/"))
            futures[exe.submit(_http_get, target, timeout)] = (p, target)
        for fut in as_completed(futures):
            p, target = futures[fut]
            status, size = fut.result()
            if status and status < 400:
                results.append({"path": p, "url": target, "http_status": status, "size": size})
                print(f"[{status}] {target}  size={size}")
    return results

# scanner main fallback
def scanner_main(domain: str):
    domain = domain.strip()
    if not domain:
        print("[ERRO] Informe um domínio válido para scanner_main.")
        return

    print(f"\n=== Iniciando scanner em {domain} ===\n")

    sub_results = scan_subdomains(domain, lists_dir="listas", workers=20, timeout=4, do_http=True)
    path_results = scan_paths(domain, lists_dir="listas", workers=20, timeout=4)

    print("\n--- Resumo ---")
    if sub_results:
        sub_count = len([r for r in sub_results if r.get("host") != "__WILDCARD_DETECTED__"])
        print(f"Subdomínios encontrados: {sub_count}")
    else:
        print("Subdomínios encontrados: 0")

    if path_results:
        print(f"Paths encontrados: {len(path_results)}")
    else:
        print("Paths encontrados: 0")

    print("\n=== Scanner concluído ===\n")
