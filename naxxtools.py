import requests
import os
import json
import time
from colorama import init, Fore, Style
import subprocess
import platform

# ========== INITIALISATION ==========
init(autoreset=True)

# ========== CONFIG ==========
logo = """
 ███▄    █  ▄▄▄      ▒██   ██▒   ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
 ██ ▀█   █ ▒████▄    ▒▒ █ █ ▒░   ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
▓██  ▀█ ██▒▒██  ▀█▄  ░░  █   ░   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
▓██▒  ▐▌██▒░██▄▄▄▄██  ░ █ █ ▒    ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
▒██░   ▓██░ ▓█   ▓██▒▒██▒ ▒██▒     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
░ ▒░   ▒ ▒  ▒▒   ▓▒█░▒▒ ░ ░▓ ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
░ ░░   ░ ▒░  ▒   ▒▒ ░░░   ░▒ ░       ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
   ░   ░ ░   ░   ▒    ░    ░       ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
         ░       ░  ░ ░    ░                  ░ ░      ░ ░      ░  ░      ░  
"""

creator = "Creator: Naxx / Yabyxy"

largeur = 80

# ========== COMPATIBILITÉ ==========
def is_windows():
    return platform.system().lower().startswith("win")

def clear_screen():
    os.system("cls" if is_windows() else "clear")

def set_title(title):
    if is_windows():
        os.system(f"title {title}")
    else:
        print(f"\33]0;{title}\a", end="", flush=True)

def run_ps(ps_cmd: str) -> str:
    try:
        if is_windows():
            out = subprocess.check_output([
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-Command", ps_cmd
            ], stderr=subprocess.STDOUT)
        else:
            if "Win32_Processor" in ps_cmd:
                cmd = "lscpu | grep 'Model name' | awk -F: '{print $2}'"
            elif "Win32_PhysicalMedia" in ps_cmd:
                cmd = "sudo hdparm -I /dev/sda | grep 'Serial Number' || echo 'No Serial'"
            elif "Win32_BaseBoard" in ps_cmd:
                cmd = "sudo dmidecode -s baseboard-serial-number || echo 'Unknown'"
            else:
                cmd = "uname -a"
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return out.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return f"Erreur: {e}"

# ========== SCRIPT PRINCIPAL ==========
while True:
    set_title("NAXTOOLS")
    clear_screen()
    # Logo et creator
    print(Fore.RED + logo)
    print(Fore.RED + creator.center(largeur))
    print("\n[1] IP Lookup")
    print("[2] Webhook Spammer")
    print("[3] Show HWID")
    print("")

    x = input("Option : ")

    # ========== IP LOOKUP ==========
    if x == "1":
        clear_screen()
        print(Fore.RED + "IP LOOKUP\n")
        ip = input("Enter IP: ")
        try:
            r = requests.get(f"https://ipapi.co{ip}/json/", timeout=10)
            r.raise_for_status()
            data = r.json()
            if 'error' in data:
                print(Fore.RED + f"Erreur: {data.get('error', 'Erreur inconnue')}")
            else:
                print("RESULTS\n\n")
                print(Fore.RED + f"Country: {data.get('country_name', 'N/A')}")
                print(Fore.RED + f"City: {data.get('city', 'N/A')}")
                print(Fore.RED + f"Region: {data.get('region', 'N/A')}")
                print(Fore.RED + f"Timezone: {data.get('timezone', 'N/A')}")
                print(Fore.RED + f"ISP: {data.get('org', 'N/A')}")
                print(Fore.RED + f"ASN: {data.get('asn', 'N/A')}")
                print(Fore.RED + f"Latitude: {data.get('latitude', 'N/A')}")
                print(Fore.RED + f"Longitude: {data.get('longitude', 'N/A')}")
                print(Fore.RED + f"Postal Code: {data.get('postal', 'N/A')}")
                print(Fore.RED + f"Currency: {data.get('currency', 'N/A')}")
        except Exception as e:
            print(Fore.RED + f"Erreur: {e}")

        input("Press enter to return...")

    # ========== WEBHOOK SPAMMER ==========
    elif x == "2":
        clear_screen()
        print(Fore.RED + "WEBHOOK SPAMMER\n")
        url = input("URL du Webhook : ")
        message = input("Message : ")
        name = input("Nom du Webhook : ")
        try:
            count = int(input("Nombre de messages à envoyer : "))
        except:
            count = 10

        print("\nMode d'envoi :")
        print("1. Normal (délai configurable)")
        print("2. Turbo (0.5s)")
        print("3. Ultra (0.2s)")
        print("4. Lightning (0.1s)")
        print("5. Tornado (0.05s)")
        mode = input("Choisissez le mode (1-5) [défaut 5] : ") or "5"

        if mode == "1":
            delay = float(input("Délai entre chaque message (en secondes) : "))
        elif mode == "2":
            delay = 0.5
        elif mode == "3":
            delay = 0.2
        elif mode == "4":
            delay = 0.1
        elif mode == "5":
            delay = 0.05
        else:
            delay = 0.05

        print("\nAffichage :")
        print("1. Temps réel")
        print("2. Silencieux")
        display_mode = input("Choisissez l'affichage (1-2) [défaut 2] : ") or "2"

        payload = {"content": message, "username": name}
        headers = {"Content-Type": "application/json"}

        success_count = 0
        failed_count = 0
        session = requests.Session()
        start_time = time.perf_counter()

        for i in range(1, count + 1):
            try:
                r = session.post(url, json=payload, headers=headers, timeout=5)
                if r.status_code == 429:
                    retry_after = float(r.headers.get("Retry-After", 1000)) / 1000
                    print(f"⚠️ Rate limit ! Attente {retry_after:.2f}s")
                    time.sleep(retry_after)
                    continue
                if r.status_code < 400:
                    success_count += 1
                    if display_mode == "1":
                        print(f"✅ Message {i}")
                else:
                    failed_count += 1
            except Exception as e:
                failed_count += 1
                if display_mode == "1":
                    print(f"❌ Message {i} failed: {e}")
            time.sleep(delay)

        end_time = time.perf_counter()
        print(f"\n✅ Succès: {success_count} | ❌ Échecs: {failed_count}")
        print(f"⏱️ Temps total: {end_time - start_time:.2f}s")
        input("Appuyez sur Entrée pour retourner au menu...")

    # ========== SHOW HWID ==========
    elif x == "3":
        clear_screen()
        print(Fore.RED + "Hardware ID\n")
        print(Fore.RED + "CPU SERIAL")
        print(run_ps("(Get-CimInstance Win32_Processor).ProcessorId"))
        print(Fore.RED + "Disk Serial")
        print(run_ps("(Get-CimInstance Win32_PhysicalMedia | Select-Object -Expand SerialNumber)"))
        print(Fore.RED + "Motherboard Serial")
        print(run_ps("(Get-CimInstance Win32_BaseBoard).SerialNumber"))
        input("Press enter to return...")

    else:
        clear_screen()
        print(Fore.RED + "Option invalide\n")
        input("Press enter to return...")
