
# Python 3.11 — amjd_lan_scanner.py — Windows 10/11 — AMJD ALAWAD LAN SCANNER v5.0

import os
import re
import sys
import csv
import json
import time
import socket
import sqlite3
import ipaddress
import platform
import subprocess

from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


APP_NAME = "AMJD ALAWAD"
VERSION = "5.0 ULTRA"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
DB_PATH = DATA_DIR / "network.db"

DATA_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

MAX_WORKERS = 64
PING_TIMEOUT = 650
PORT_TIMEOUT = 0.35

PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    53: "DNS",
    80: "HTTP",
    135: "RPC",
    139: "NETBIOS",
    443: "HTTPS",
    445: "SMB",
    554: "RTSP",
    631: "PRINTER",
    3389: "RDP",
    8080: "HTTP-ALT",
    8443: "HTTPS-ALT",
    9100: "PRINTER"
}

OUI = {
    "F4:F5:D8": "Apple",
    "AC:BC:32": "Apple",
    "28:6C:07": "Samsung",
    "FC:FC:48": "Xiaomi",
    "64:CC:2E": "Xiaomi",
    "00:1E:C2": "Dell",
    "3C:D9:2B": "HP",
    "00:50:56": "VMware",
    "B8:27:EB": "Raspberry Pi"
}


# ---------------- COLORS ----------------

class C:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BLUE = "\033[94m"


def setup_terminal():
    os.system("")
    if platform.system() == "Windows":
        os.system("chcp 65001 > nul")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    clear()
    print(C.CYAN + "=" * 78)
    print("                         AMJD ALAWAD")
    print("                       LAN SCANNER ULTRA")
    print("                           VERSION 5.0")
    print(C.GREEN + "                    WINDOWS NETWORK SCANNER")
    print(C.CYAN + "=" * 78 + C.RESET)


def pause():
    input("\nPress ENTER to continue...")


# ---------------- DATABASE ----------------

def db_connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def initialize_database():
    with db_connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                mac TEXT NOT NULL,
                vendor TEXT,
                hostname TEXT,
                device_type TEXT,
                first_seen TEXT,
                last_seen TEXT,
                scan_count INTEGER DEFAULT 1,
                discovery_method TEXT,
                open_ports TEXT
            )
        """)

        db.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            unique_device ON devices(ip, mac)
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_time TEXT,
                network TEXT,
                device_count INTEGER
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_time TEXT,
                event_type TEXT,
                ip TEXT,
                mac TEXT,
                details TEXT
            )
        """)


def add_event(db, event_type, device, details):
    db.execute("""
        INSERT INTO events
        (event_time, event_type, ip, mac, details)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().astimezone().isoformat(),
        event_type,
        device["ip"],
        device["mac"],
        details
    ))


def save_scan(network, devices):
    now = datetime.now().astimezone().isoformat()

    with db_connect() as db:
        db.execute("""
            INSERT INTO scans (scan_time, network, device_count)
            VALUES (?, ?, ?)
        """, (now, str(network), len(devices)))

        for device in devices:
            ip = device["ip"]
            mac = device["mac"]

            previous = db.execute("""
                SELECT * FROM devices
                WHERE ip = ? AND mac = ?
            """, (ip, mac)).fetchone()

            ports_json = json.dumps(
                device["ports"],
                ensure_ascii=False
            )

            if previous is None:
                db.execute("""
                    INSERT INTO devices (
                        ip, mac, vendor, hostname, device_type,
                        first_seen, last_seen, scan_count,
                        discovery_method, open_ports
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                """, (
                    ip, mac,
                    device["vendor"],
                    device["hostname"],
                    device["device_type"],
                    now, now,
                    device["method"],
                    ports_json
                ))

                add_event(
                    db, "NEW_DEVICE", device,
                    "Device discovered for the first time"
                )

            else:
                if previous["open_ports"] != ports_json:
                    add_event(
                        db, "PORT_CHANGE", device,
                        "Observed open services changed"
                    )

                db.execute("""
                    UPDATE devices SET
                        vendor = ?,
                        hostname = ?,
                        device_type = ?,
                        last_seen = ?,
                        scan_count = scan_count + 1,
                        discovery_method = ?,
                        open_ports = ?
                    WHERE id = ?
                """, (
                    device["vendor"],
                    device["hostname"],
                    device["device_type"],
                    now,
                    device["method"],
                    ports_json,
                    previous["id"]
                ))


def statistics():
    with db_connect() as db:
        return {
            "devices": db.execute(
                "SELECT COUNT(*) FROM devices"
            ).fetchone()[0],
            "scans": db.execute(
                "SELECT COUNT(*) FROM scans"
            ).fetchone()[0],
            "events": db.execute(
                "SELECT COUNT(*) FROM events"
            ).fetchone()[0]
        }


# ---------------- NETWORK DISCOVERY ----------------

def normalize_network(value):
    value = value.strip()

    if "/" not in value:
        address = ipaddress.ip_address(value)

        if not isinstance(address, ipaddress.IPv4Address):
            raise ValueError("IPv4 address required")

        # This default matches the user's 255.255.255.0 subnet.
        value += "/24"

    network = ipaddress.ip_network(value, strict=False)

    if not isinstance(network, ipaddress.IPv4Network):
        raise ValueError("IPv4 network required")

    if not network.is_private:
        raise ValueError("Private network only")

    if network.num_addresses > 512:
        raise ValueError("Maximum network size is 512 addresses")

    return network


def ping_host(ip):
    command = [
        "ping", "-n", "1", "-w",
        str(PING_TIMEOUT), str(ip)
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3
        )

        return result.returncode == 0

    except (OSError, subprocess.TimeoutExpired):
        return False


def read_arp_table(network):
    found = {}

    try:
        result = subprocess.run(
            ["arp", "-a"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5
        )

        pattern = re.compile(
            r"(\d{1,3}(?:\.\d{1,3}){3})\s+"
            r"([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})"
        )

        for line in result.stdout.splitlines():
            match = pattern.search(line)

            if not match:
                continue

            ip = match.group(1)

            try:
                address = ipaddress.ip_address(ip)
                if address not in network:
                    continue
            except ValueError:
                continue

            mac = match.group(2).replace("-", ":").upper()

            if mac == "FF:FF:FF:FF:FF:FF":
                continue

            found[ip] = mac

    except (OSError, subprocess.TimeoutExpired):
        pass

    return found


def get_vendor(mac):
    if not mac or mac == "Unavailable":
        return "Unknown"

    prefix = mac.upper()[:8]
    return OUI.get(prefix, "Unknown")


def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, OSError):
        return "Unknown"


# ---------------- PORT SCAN ----------------

def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(PORT_TIMEOUT)

    try:
        result = sock.connect_ex((ip, port))

        if result == 0:
            return {
                "port": port,
                "service": PORTS[port],
                "status": "OPEN"
            }

    except OSError:
        pass

    finally:
        sock.close()

    return None


def scan_ports(ip):
    results = []

    with ThreadPoolExecutor(max_workers=15) as pool:
        futures = [
            pool.submit(check_port, ip, port)
            for port in PORTS
        ]

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception:
                pass

    return sorted(results, key=lambda item: item["port"])


# ---------------- DEVICE ANALYSIS ----------------

def classify_device(hostname, vendor, ports):
    name = hostname.lower()
    numbers = {item["port"] for item in ports}

    if "iphone" in name or "ipad" in name:
        return "Apple Device"

    if "android" in name:
        return "Android Device"

    if 631 in numbers or 9100 in numbers:
        return "Possible Printer"

    if 554 in numbers:
        return "Possible Camera"

    if 3389 in numbers:
        return "Possible Windows PC"

    if 22 in numbers:
        return "Possible Linux / SSH"

    if vendor != "Unknown":
        return vendor + " Device"

    return "Unknown Device"


def inspect_device(ip, mac, method):
    hostname = get_hostname(ip)
    vendor = get_vendor(mac)
    ports = scan_ports(ip)

    device_type = classify_device(
        hostname, vendor, ports
    )

    return {
        "ip": ip,
        "mac": mac,
        "vendor": vendor,
        "hostname": hostname,
        "device_type": device_type,
        "method": method,
        "ports": ports,
        "scan_time": datetime.now().astimezone().isoformat()
    }


# ---------------- FULL SCAN ----------------

def run_scan(network):
    print(C.YELLOW + "\n[1/3] Pinging network addresses..." + C.RESET)

    hosts = [str(ip) for ip in network.hosts()]
    alive = set()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(ping_host, ip): ip
            for ip in hosts
        }

        completed = 0

        for future in as_completed(futures):
            completed += 1

            try:
                if future.result():
                    alive.add(futures[future])
            except Exception:
                pass

            if completed % 25 == 0 or completed == len(hosts):
                print(
                    f"\rPing progress: {completed}/{len(hosts)}",
                    end="",
                    flush=True
                )

    print("\n")

    print(C.YELLOW + "[2/3] Reading Windows ARP table..." + C.RESET)

    arp_devices = read_arp_table(network)

    discovered = {}

    for ip in alive:
        discovered[ip] = {
            "mac": arp_devices.get(ip, "Unavailable"),
            "method": (
                "PING + ARP"
                if ip in arp_devices
                else "PING"
            )
        }

    for ip, mac in arp_devices.items():
        if ip not in discovered:
            discovered[ip] = {
                "mac": mac,
                "method": "ARP"
            }

    print(
        C.GREEN +
        f"Discovered addresses: {len(discovered)}" +
        C.RESET
    )

    if not discovered:
        print(C.RED + "No responding devices found." + C.RESET)
        print("Check the selected network and Wi-Fi connection.")
        return []

    print(C.YELLOW + "\n[3/3] Inspecting discovered devices..." + C.RESET)

    results = []
    items = list(discovered.items())

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(
                inspect_device,
                ip,
                info["mac"],
                info["method"]
            ): ip
            for ip, info in items
        }

        completed = 0

        for future in as_completed(futures):
            completed += 1

            try:
                results.append(future.result())
            except Exception as error:
                print(f"\nInspection error: {error}")

            print(
                f"\rInspection: {completed}/{len(items)}",
                end="",
                flush=True
            )

    results.sort(
        key=lambda item: ipaddress.ip_address(item["ip"])
    )

    print("\n")
    return results


# ---------------- DISPLAY ----------------

def show_devices(devices):
    if not devices:
        print(C.YELLOW + "\nNo results. Run a scan first." + C.RESET)
        return

    print("\n" + "=" * 112)
    print(
        f"{'NO':<5}"
        f"{'IP ADDRESS':<19}"
        f"{'MAC ADDRESS':<21}"
        f"{'VENDOR':<16}"
        f"{'DEVICE TYPE':<26}"
        f"{'METHOD'}"
    )
    print("-" * 112)

    for index, device in enumerate(devices, 1):
        print(
            f"{index:<5}"
            f"{device['ip']:<19}"
            f"{device['mac']:<21}"
            f"{device['vendor']:<16}"
            f"{device['device_type'][:25]:<26}"
            f"{device['method']}"
        )

    print("=" * 112)
    print(f"Total discovered: {len(devices)}")


def device_details(devices):
    if not devices:
        print("No current scan results.")
        return

    try:
        number = int(input("Enter device number: "))
        if number < 1 or number > len(devices):
            raise ValueError

        device = devices[number - 1]

    except ValueError:
        print(C.RED + "Invalid number." + C.RESET)
        return

    print("\n" + "=" * 65)
    print("              DEVICE DETAILS")
    print("=" * 65)

    for label, key in [
        ("IP Address", "ip"),
        ("MAC Address", "mac"),
        ("Vendor", "vendor"),
        ("Hostname", "hostname"),
        ("Device Type", "device_type"),
        ("Discovery Method", "method"),
        ("Scan Time", "scan_time")
    ]:
        print(f"{label:<23}: {device[key]}")

    print("\nOPEN TCP PORTS")

    if not device["ports"]:
        print("No tested TCP ports detected as open.")
    else:
        for item in device["ports"]:
            print(
                f"{item['port']:<8}"
                f"{item['service']:<18}"
                f"{item['status']}"
            )

    print("\nSECURITY OBSERVATIONS")

    warnings = {
        21: "FTP detected. Check whether credentials are encrypted.",
        23: "Telnet detected. Traffic is generally unencrypted.",
        445: "SMB detected. Review sharing and firewall settings.",
        3389: "RDP detected. Review remote access restrictions."
    }

    found = False

    for item in device["ports"]:
        if item["port"] in warnings:
            print(C.YELLOW + "[!] " + warnings[item["port"]] + C.RESET)
            found = True

    if not found:
        print("No listed service warnings.")


# ---------------- HISTORY ----------------

def show_history():
    with db_connect() as db:
        rows = db.execute("""
            SELECT * FROM devices
            ORDER BY last_seen DESC
        """).fetchall()

    print("\nSAVED DEVICE HISTORY\n")

    if not rows:
        print("History is empty.")
        return

    for row in rows:
        print(
            f"{row['ip']:<18}"
            f"{row['mac']:<21}"
            f"{row['vendor']:<15}"
            f"Scans: {row['scan_count']:<5}"
            f"Last: {row['last_seen']}"
        )


def show_events():
    with db_connect() as db:
        rows = db.execute("""
            SELECT * FROM events
            ORDER BY id DESC
            LIMIT 100
        """).fetchall()

    print("\nNETWORK EVENTS\n")

    if not rows:
        print("No recorded events.")
        return

    for row in rows:
        print(
            f"{row['event_time']} | "
            f"{row['event_type']} | "
            f"{row['ip']} | "
            f"{row['details']}"
        )


# ---------------- EXPORT ----------------

def export_reports(devices):
    if not devices:
        print("Run a scan first.")
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = REPORT_DIR / f"scan_{stamp}.json"
    csv_path = REPORT_DIR / f"scan_{stamp}.csv"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(
            devices,
            file,
            indent=4,
            ensure_ascii=False
        )

    fields = [
        "ip", "mac", "vendor", "hostname",
        "device_type", "method", "scan_time"
    ]

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for device in devices:
            row = {
                key: device.get(key, "")
                for key in fields
            }

            row["ports"] = ",".join(
                str(item["port"])
                for item in device["ports"]
            )

            writer.writerow(row)

    print(C.GREEN + "\nReports created:" + C.RESET)
    print(json_path)
    print(csv_path)


# ---------------- MAIN MENU ----------------

def main():
    setup_terminal()
    initialize_database()

    latest_results = []

    while True:
        header()

        stats = statistics()

        print(f"Known devices  : {stats['devices']}")
        print(f"Previous scans : {stats['scans']}")
        print(f"Network events: {stats['events']}")

        print("\n[1] Scan Wi-Fi / Private Network")
        print("[2] Show Current Devices")
        print("[3] Device Details")
        print("[4] Saved Device History")
        print("[5] Network Events")
        print("[6] Export CSV + JSON")
        print("[0] Exit")

        choice = input("\nAMJD > ").strip()

        if choice == "1":
            value = input(
                "\nNetwork CIDR or local IP "
                "[default 192.168.1.0/24]: "
            ).strip()

            if not value:
                value = "192.168.1.0/24"

            try:
                network = normalize_network(value)

                print(
                    C.CYAN +
                    f"\nTarget network: {network}" +
                    C.RESET
                )

                latest_results = run_scan(network)

                if latest_results:
                    save_scan(network, latest_results)
                    show_devices(latest_results)

                    print(
                        C.GREEN +
                        "\nScan saved successfully." +
                        C.RESET
                    )

            except Exception as error:
                print(C.RED + f"\nScan error: {error}" + C.RESET)

            pause()

        elif choice == "2":
            show_devices(latest_results)
            pause()

        elif choice == "3":
            device_details(latest_results)
            pause()

        elif choice == "4":
            show_history()
            pause()

        elif choice == "5":
            show_events()
            pause()

        elif choice == "6":
            export_reports(latest_results)
            pause()

        elif choice == "0":
            print("\nAMJD ALAWAD - Scanner closed.")
            break

        else:
            print(C.RED + "Invalid choice." + C.RESET)
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScanner stopped.")
        sys.exit(0)
