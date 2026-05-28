#!/usr/bin/env python3
"""
NetWatcher
==========

Small Flask tool for LXD + WireGuard environments.

Features:
- Discovers candidate IPs from LXD, WireGuard configs, Linux routes and ARP/neighbour table.
- Scans configured TCP ports and stores only active/open results.
- Shows hostnames, source hints and guessed service names.
- Lets you manage WireGuard peers in the server config safely with backups.

Security notes:
- This is an admin tool. Do not expose it publicly.
- WireGuard config editing requires root access or sudo/systemd permissions.
- Scanning should only be used on networks you own/control.
"""

from __future__ import annotations

import base64
import concurrent.futures
import csv
import datetime as dt
import ipaddress
import json
import os
import re
import shutil
import socket
import sqlite3
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from flask import Flask, jsonify, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.yml"
DB_FILE = BASE_DIR / "netwatcher.sqlite3"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("NETWATCHER_SECRET", "dev-change-me")

STATE = {
    "last_scan_started": None,
    "last_scan_finished": None,
    "scan_running": False,
    "last_error": None,
}

# -----------------------------
# Config helpers
# -----------------------------

def load_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        shutil.copy(BASE_DIR / "config.example.yml", CONFIG_FILE)
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_config(config: dict[str, Any]) -> None:
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False, allow_unicode=True)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def run_cmd(args: list[str] | str, timeout: int = 8, shell: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        shell=shell,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )

# -----------------------------
# Database
# -----------------------------

def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scanned_at TEXT NOT NULL,
                ip TEXT NOT NULL,
                hostname TEXT,
                port INTEGER NOT NULL,
                service TEXT,
                source TEXT,
                latency_ms REAL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_scan_latest ON scan_results(scanned_at, ip, port)")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS discovered_hosts (
                ip TEXT PRIMARY KEY,
                hostname TEXT,
                source TEXT,
                last_seen TEXT NOT NULL
            )
            """
        )

# -----------------------------
# Discovery
# -----------------------------

@dataclass
class Target:
    ip: str
    source: set[str] = field(default_factory=set)
    hostname: str | None = None


def add_ip(targets: dict[str, Target], ip_text: str, source: str, hostname: str | None = None) -> None:
    try:
        ip = ipaddress.ip_address(ip_text.strip())
        if ip.version != 4:
            return
        if ip.is_loopback or ip.is_multicast or ip.is_unspecified:
            return
        key = str(ip)
        if key not in targets:
            targets[key] = Target(ip=key)
        targets[key].source.add(source)
        if hostname and not targets[key].hostname:
            targets[key].hostname = hostname
    except ValueError:
        return


def add_network(targets: dict[str, Target], net_text: str, source: str, max_hosts: int = 4096) -> None:
    try:
        network = ipaddress.ip_network(net_text.strip(), strict=False)
        if network.version != 4:
            return
        # Safety cap: prevent accidental huge scans.
        if network.num_addresses > max_hosts:
            return
        for ip in network.hosts():
            add_ip(targets, str(ip), source)
    except ValueError:
        return


def parse_network_list(items: list[str] | None) -> list[ipaddress._BaseNetwork]:
    networks: list[ipaddress._BaseNetwork] = []
    for raw in items or []:
        text = str(raw).strip()
        if not text:
            continue
        try:
            if "/" in text:
                networks.append(ipaddress.ip_network(text, strict=False))
            else:
                networks.append(ipaddress.ip_network(f"{text}/32", strict=False))
        except ValueError:
            continue
    return networks


def should_keep_target(ip_text: str, scanner: dict[str, Any]) -> bool:
    """Final safety filter before scanning. Prevents accidental public scans."""
    try:
        ip = ipaddress.ip_address(ip_text)
    except ValueError:
        return False

    if ip.version != 4:
        return False
    if ip.is_loopback or ip.is_multicast or ip.is_unspecified:
        return False

    # Default: only RFC1918/private/link-local networks are scanned.
    # This prevents cases where a default/public route becomes a /24 scan target.
    if scanner.get("private_only", True) and not (ip.is_private or ip.is_link_local):
        return False

    excluded = parse_network_list(scanner.get("exclude_targets", []))
    if any(ip in net for net in excluded):
        return False

    return True


def filter_targets(targets: dict[str, Target], scanner: dict[str, Any]) -> dict[str, Target]:
    return {ip: target for ip, target in targets.items() if should_keep_target(ip, scanner)}


def discover_from_lxd(targets: dict[str, Target]) -> None:
    """Discover running LXD instance addresses and LXD-managed bridge subnets."""
    if shutil.which("lxc") is None:
        return

    result = run_cmd(["lxc", "list", "--format", "json"], timeout=10)
    if result.returncode == 0 and result.stdout.strip():
        try:
            instances = json.loads(result.stdout)
            for inst in instances:
                name = inst.get("name")
                state = (inst.get("status") or "").lower()
                if state and state != "running":
                    continue
                for net_values in (inst.get("stateful") or {}).values():
                    pass
                for iface in (inst.get("state", {}) or {}).get("network", {}).values():
                    for addr in iface.get("addresses", []):
                        if addr.get("family") == "inet":
                            add_ip(targets, addr.get("address", ""), "lxd-instance", name)
                # Some LXD versions include state only when --format=json with columns; fallback below.
        except Exception:
            pass

    result = run_cmd(["lxc", "network", "list", "--format", "json"], timeout=10)
    if result.returncode == 0 and result.stdout.strip():
        try:
            networks = json.loads(result.stdout)
            for net in networks:
                cfg = net.get("config", {}) or {}
                ipv4 = cfg.get("ipv4.address")
                if ipv4 and ipv4 not in ("none", "auto"):
                    add_network(targets, ipv4, f"lxd-network:{net.get('name')}")
        except Exception:
            pass


def discover_from_lxd_fallback(targets: dict[str, Target]) -> None:
    """Fallback parser for `lxc list -c ns4 --format csv`."""
    if shutil.which("lxc") is None:
        return
    result = run_cmd(["lxc", "list", "-c", "ns4", "--format", "csv"], timeout=10)
    if result.returncode != 0:
        return
    for parts in csv.reader(result.stdout.splitlines()):
        parts = [p.strip() for p in parts]
        if len(parts) < 3:
            continue
        name, status, ipv4s = parts[0], parts[1].lower(), parts[2]
        if status != "running":
            continue
        # Example field: "10.251.167.110 (eth0)" or multiple addresses separated by spaces.
        for ip_match in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", ipv4s):
            add_ip(targets, ip_match, "lxd-instance", name)


def parse_wireguard_config(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {"interface": {}, "peers": []}
    if not path.exists():
        return data

    current: dict[str, Any] | None = None
    current_type: str | None = None
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line == "[Interface]":
                current = data["interface"]
                current_type = "interface"
                continue
            if line == "[Peer]":
                current = {}
                data["peers"].append(current)
                current_type = "peer"
                continue
            if current is None or "=" not in line:
                continue
            key, value = line.split("=", 1)
            current[key.strip()] = value.strip()
            current["_type"] = current_type
    return data


def discover_from_wireguard(targets: dict[str, Target], wg_path: Path) -> None:
    parsed = parse_wireguard_config(wg_path)
    iface_addr = parsed.get("interface", {}).get("Address")
    if iface_addr:
        for addr in iface_addr.split(","):
            add_network(targets, addr.strip(), "wg-interface")
    for peer in parsed.get("peers", []):
        allowed = peer.get("AllowedIPs", "")
        pub = peer.get("PublicKey", "")[:10]
        for item in allowed.split(","):
            item = item.strip()
            if not item:
                continue
            if "/" in item:
                # /32 is one peer IP; /24 might be remote LXD subnet.
                add_network(targets, item, f"wg-allowed:{pub}")
            else:
                add_ip(targets, item, f"wg-allowed:{pub}")


def discover_from_routes(targets: dict[str, Target]) -> None:
    result = run_cmd(["ip", "-4", "route"], timeout=5)
    if result.returncode != 0:
        return
    for line in result.stdout.splitlines():
        first = line.split()[0] if line.split() else ""
        if first in ("default", "broadcast", "throw", "unreachable"):
            continue
        if "/" in first:
            add_network(targets, first, "linux-route")


def discover_from_neigh(targets: dict[str, Target]) -> None:
    result = run_cmd(["ip", "-4", "neigh"], timeout=5)
    if result.returncode != 0:
        return
    for line in result.stdout.splitlines():
        parts = line.split()
        if parts:
            add_ip(targets, parts[0], "arp-neigh")


def discover_from_etc_hosts(targets: dict[str, Target]) -> None:
    hosts_file = Path("/etc/hosts")
    if not hosts_file.exists():
        return
    for raw in hosts_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            add_ip(targets, parts[0], "etc-hosts", parts[1])


def discover_targets(config: dict[str, Any]) -> dict[str, Target]:
    targets: dict[str, Target] = {}
    scanner = config.get("scanner", {})
    discovery = scanner.get("discovery", {})
    wg_cfg = config.get("wireguard", {})

    if discovery.get("lxd", True):
        discover_from_lxd(targets)
        discover_from_lxd_fallback(targets)
    if discovery.get("wireguard", True):
        discover_from_wireguard(targets, Path(wg_cfg.get("config_path", "/etc/wireguard/wg0.conf")))
    if discovery.get("linux_routes", True):
        discover_from_routes(targets)
    if discovery.get("arp_neigh", True):
        discover_from_neigh(targets)
    if discovery.get("etc_hosts", True):
        discover_from_etc_hosts(targets)

    for item in scanner.get("manual_targets", []) or []:
        if "/" in str(item):
            add_network(targets, str(item), "manual")
        else:
            add_ip(targets, str(item), "manual")

    return filter_targets(targets, scanner)

# -----------------------------
# Scanning
# -----------------------------

def reverse_dns(ip: str) -> str | None:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def service_name(port: int) -> str:
    try:
        return socket.getservbyport(port, "tcp")
    except Exception:
        known = {
            22: "ssh", 53: "dns", 80: "http", 443: "https", 5432: "postgresql",
            6379: "redis", 8000: "http-alt", 8080: "http-alt", 8443: "https-alt",
            8200: "vault", 51820: "wireguard/udp",
        }
        return known.get(port, "unknown")


def scan_port(ip: str, port: int, timeout: float) -> tuple[bool, float | None]:
    start = time.perf_counter()
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            return True, latency_ms
    except Exception:
        return False, None


def perform_scan() -> None:
    config = load_config()
    scanner = config.get("scanner", {})
    ports = [int(p) for p in scanner.get("ports", [])]
    timeout = float(scanner.get("timeout_seconds", 0.6))
    max_workers = int(scanner.get("max_concurrency", 512))

    STATE["scan_running"] = True
    STATE["last_scan_started"] = now_iso()
    STATE["last_error"] = None
    scan_time = now_iso()

    try:
        targets = discover_targets(config)
        with db() as conn:
            for t in targets.values():
                hostname = t.hostname or reverse_dns(t.ip)
                t.hostname = hostname
                conn.execute(
                    """
                    INSERT INTO discovered_hosts(ip, hostname, source, last_seen)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(ip) DO UPDATE SET
                        hostname=excluded.hostname,
                        source=excluded.source,
                        last_seen=excluded.last_seen
                    """,
                    (t.ip, hostname, ", ".join(sorted(t.source)), scan_time),
                )

        jobs: list[tuple[str, int]] = [(ip, port) for ip in sorted(targets) for port in ports]
        open_rows: list[tuple[str, str, str | None, int, str, str, float]] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            future_map = {
                pool.submit(scan_port, ip, port, timeout): (ip, port)
                for ip, port in jobs
            }
            for future in concurrent.futures.as_completed(future_map):
                ip, port = future_map[future]
                is_open, latency_ms = future.result()
                if not is_open:
                    continue
                target = targets[ip]
                open_rows.append((scan_time, ip, target.hostname, port, service_name(port), ", ".join(sorted(target.source)), latency_ms or 0.0))

        with db() as conn:
            conn.executemany(
                """
                INSERT INTO scan_results(scanned_at, ip, hostname, port, service, source, latency_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                open_rows,
            )
            # Keep DB small.
            conn.execute(
                "DELETE FROM scan_results WHERE id NOT IN (SELECT id FROM scan_results ORDER BY id DESC LIMIT 20000)"
            )

        STATE["last_scan_finished"] = now_iso()
    except Exception as exc:
        STATE["last_error"] = str(exc)
    finally:
        STATE["scan_running"] = False


def scanner_loop() -> None:
    while True:
        perform_scan()
        config = load_config()
        interval = int(config.get("scanner", {}).get("interval_seconds", 60))
        time.sleep(max(10, interval))

# -----------------------------
# WireGuard config editing
# -----------------------------

VALID_BASE64_RE = re.compile(r"^[A-Za-z0-9+/]{42,44}={0,2}$")


def normalize_allowed_ips(value: str) -> str:
    items: list[str] = []
    for raw in value.split(","):
        item = raw.strip()
        if not item:
            continue
        # Validate IP/network.
        ipaddress.ip_network(item, strict=False)
        items.append(item)
    return ", ".join(items)


def generate_wg_keys() -> dict[str, str]:
    """Use `wg` if available; fallback to random base64 placeholders for offline drafting."""
    if shutil.which("wg"):
        private = run_cmd(["wg", "genkey"], timeout=5)
        if private.returncode != 0:
            raise RuntimeError(private.stderr.strip() or "wg genkey failed")
        private_key = private.stdout.strip()
        public = subprocess.run(
            ["wg", "pubkey"],
            input=private_key + "\n",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            check=False,
        )
        if public.returncode != 0:
            raise RuntimeError(public.stderr.strip() or "wg pubkey failed")
        psk = run_cmd(["wg", "genpsk"], timeout=5)
        if psk.returncode != 0:
            raise RuntimeError(psk.stderr.strip() or "wg genpsk failed")
        return {"private_key": private_key, "public_key": public.stdout.strip(), "preshared_key": psk.stdout.strip()}

    # Fallback allows UI development without wireguard-tools installed.
    def b64() -> str:
        return base64.b64encode(os.urandom(32)).decode("ascii")
    return {"private_key": b64(), "public_key": b64(), "preshared_key": b64()}


def render_wireguard_config(parsed: dict[str, Any]) -> str:
    lines: list[str] = ["[Interface]"]
    for key, value in parsed.get("interface", {}).items():
        if key.startswith("_"):
            continue
        lines.append(f"{key} = {value}")
    lines.append("")

    for peer in parsed.get("peers", []):
        lines.append("[Peer]")
        for key in ("PublicKey", "PresharedKey", "AllowedIPs", "Endpoint", "PersistentKeepalive"):
            if peer.get(key):
                lines.append(f"{key} = {peer[key]}")
        extra_keys = [k for k in peer.keys() if not k.startswith("_") and k not in {"PublicKey", "PresharedKey", "AllowedIPs", "Endpoint", "PersistentKeepalive"}]
        for key in extra_keys:
            lines.append(f"{key} = {peer[key]}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def load_wg_parsed() -> tuple[Path, dict[str, Any]]:
    cfg = load_config().get("wireguard", {})
    path = Path(cfg.get("config_path", "/etc/wireguard/wg0.conf"))
    return path, parse_wireguard_config(path)


def backup_and_write_wg(path: Path, parsed: dict[str, Any]) -> None:
    cfg = load_config().get("wireguard", {})
    backup_dir = Path(cfg.get("backup_dir", "/etc/wireguard/netwatcher-backups"))
    backup_dir.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup_name = f"{path.name}.{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}.bak"
        shutil.copy2(path, backup_dir / backup_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(render_wireguard_config(parsed), encoding="utf-8")
    os.chmod(tmp, 0o600)
    tmp.replace(path)

    if cfg.get("auto_apply", False):
        command = cfg.get("apply_command", "wg-quick down wg0 && wg-quick up wg0")
        result = run_cmd(command, timeout=20, shell=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "WireGuard apply failed")

# -----------------------------
# Flask views
# -----------------------------

@app.route("/")
def dashboard():
    with db() as conn:
        latest_scan = conn.execute("SELECT scanned_at FROM scan_results ORDER BY scanned_at DESC LIMIT 1").fetchone()
        rows = []
        if latest_scan:
            rows = conn.execute(
                """
                SELECT ip, hostname, group_concat(port || '/' || service, ', ') AS open_ports,
                       source, min(latency_ms) AS latency_ms
                FROM scan_results
                WHERE scanned_at = ?
                GROUP BY ip, hostname, source
                ORDER BY ip
                """,
                (latest_scan["scanned_at"],),
            ).fetchall()
        discovered_count = conn.execute("SELECT count(*) AS c FROM discovered_hosts").fetchone()["c"]
    return render_template("dashboard.html", rows=rows, state=STATE, discovered_count=discovered_count)


@app.route("/scan", methods=["POST"])
def scan_now():
    if not STATE["scan_running"]:
        threading.Thread(target=perform_scan, daemon=True).start()
    return redirect(url_for("dashboard"))


@app.route("/api/latest")
def api_latest():
    with db() as conn:
        latest_scan = conn.execute("SELECT scanned_at FROM scan_results ORDER BY scanned_at DESC LIMIT 1").fetchone()
        if not latest_scan:
            return jsonify({"scanned_at": None, "hosts": []})
        rows = conn.execute(
            """
            SELECT ip, hostname, port, service, source, latency_ms
            FROM scan_results
            WHERE scanned_at = ?
            ORDER BY ip, port
            """,
            (latest_scan["scanned_at"],),
        ).fetchall()
    return jsonify({"scanned_at": latest_scan["scanned_at"], "hosts": [dict(r) for r in rows]})


@app.route("/wireguard")
def wireguard_page():
    path, parsed = load_wg_parsed()
    return render_template("wireguard.html", path=path, parsed=parsed, error=request.args.get("error"), ok=request.args.get("ok"))


@app.route("/wireguard/peer/add", methods=["POST"])
def wg_add_peer():
    try:
        path, parsed = load_wg_parsed()
        public_key = request.form.get("public_key", "").strip()
        preshared_key = request.form.get("preshared_key", "").strip()
        allowed_ips = normalize_allowed_ips(request.form.get("allowed_ips", ""))
        endpoint = request.form.get("endpoint", "").strip()
        keepalive = request.form.get("persistent_keepalive", "").strip()
        if not public_key:
            raise ValueError("PublicKey fehlt")
        peer = {"PublicKey": public_key, "AllowedIPs": allowed_ips}
        if preshared_key:
            peer["PresharedKey"] = preshared_key
        if endpoint:
            peer["Endpoint"] = endpoint
        if keepalive:
            peer["PersistentKeepalive"] = keepalive
        parsed["peers"].append(peer)
        backup_and_write_wg(path, parsed)
        return redirect(url_for("wireguard_page", ok="Peer gespeichert"))
    except Exception as exc:
        return redirect(url_for("wireguard_page", error=str(exc)))


@app.route("/wireguard/peer/update/<int:index>", methods=["POST"])
def wg_update_peer(index: int):
    try:
        path, parsed = load_wg_parsed()
        peer = parsed["peers"][index]
        peer["AllowedIPs"] = normalize_allowed_ips(request.form.get("allowed_ips", ""))
        if request.form.get("preshared_key"):
            peer["PresharedKey"] = request.form.get("preshared_key", "").strip()
        if request.form.get("endpoint"):
            peer["Endpoint"] = request.form.get("endpoint", "").strip()
        elif "Endpoint" in peer:
            peer.pop("Endpoint")
        if request.form.get("persistent_keepalive"):
            peer["PersistentKeepalive"] = request.form.get("persistent_keepalive", "").strip()
        elif "PersistentKeepalive" in peer:
            peer.pop("PersistentKeepalive")
        backup_and_write_wg(path, parsed)
        return redirect(url_for("wireguard_page", ok="Peer aktualisiert"))
    except Exception as exc:
        return redirect(url_for("wireguard_page", error=str(exc)))


@app.route("/wireguard/peer/delete/<int:index>", methods=["POST"])
def wg_delete_peer(index: int):
    try:
        path, parsed = load_wg_parsed()
        parsed["peers"].pop(index)
        backup_and_write_wg(path, parsed)
        return redirect(url_for("wireguard_page", ok="Peer gelöscht"))
    except Exception as exc:
        return redirect(url_for("wireguard_page", error=str(exc)))


@app.route("/wireguard/generate")
def wg_generate():
    return jsonify(generate_wg_keys())


@app.route("/settings", methods=["GET", "POST"])
def settings():
    cfg = load_config()
    if request.method == "POST":
        ports = []
        for p in request.form.get("ports", "").replace("\n", ",").split(","):
            p = p.strip()
            if p:
                ports.append(int(p))
        manual_targets = []
        for t in request.form.get("manual_targets", "").replace("\n", ",").split(","):
            t = t.strip()
            if t:
                manual_targets.append(t)
        exclude_targets = []
        for t in request.form.get("exclude_targets", "").replace("\n", ",").split(","):
            t = t.strip()
            if t:
                exclude_targets.append(t)
        cfg.setdefault("scanner", {})["interval_seconds"] = int(request.form.get("interval_seconds", "60"))
        cfg["scanner"]["ports"] = ports
        cfg["scanner"]["manual_targets"] = manual_targets
        cfg["scanner"]["exclude_targets"] = exclude_targets
        cfg["scanner"]["private_only"] = request.form.get("private_only") == "on"
        cfg.setdefault("wireguard", {})["config_path"] = request.form.get("wg_config_path", "/etc/wireguard/wg0.conf")
        cfg["wireguard"]["auto_apply"] = request.form.get("auto_apply") == "on"
        save_config(cfg)
        return redirect(url_for("settings"))
    return render_template("settings.html", config=cfg)


def main() -> None:
    init_db()
    threading.Thread(target=scanner_loop, daemon=True).start()
    cfg = load_config().get("web", {})
    app.run(host=cfg.get("host", "0.0.0.0"), port=int(cfg.get("port", 8080)))


if __name__ == "__main__":
    main()
