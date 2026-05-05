import pyudev
import os
import time
import yagmail
import cv2
import getpass
import platform
import socket
import threading
from datetime import datetime
from datetime import datetime
import getpass
import platform
import socket

def show_intrusion(reason):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = getpass.getuser()
    system = platform.system()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    print("\n[!] [INTRUSION DETECTED] [::]")
    print("               ")
    print(f"[+] Time       : {now}")
    print(f"[+] Reason     : {reason}")
    print(f"[+] User       : {user}")
    print(f"[+] System     : {system}")
    print(f"[+] Hostname   : {hostname}")
    print(f"[+] IP Address : {ip}")
    print("             \n")
# ========= CONFIG =========
SECRET_KEY = "ACCESS12"

EMAIL = "reciver@gmail.com"
APP_PASSWORD = "imqnmkiqrsnqhqiq"
RECEIVER = "sender03@gmail.com"

LOG_FILE = "usb_log.txt"
# ==========================

processed_devices = set()
current_intrusion_device = None
device_map = {}

# ===== ANSI COLORS =====
BOLD = "\033[1m"
RED = "\033[31m"
ORANGE = "\033[33m"
BABY_GREEN = "\033[38;5;157m"
RESET = "\033[0m"

# ================= ASCII =================

AUTHORIZED_ART = ( "\033[0m" + r"""
       ░░▒▓█▄▀::AUTHORIZED USB::▀▄█▓▒░░


               ▄█████████▄▄▄▄
              ▐ ██▓""" +BOLD + "\033[32m"  + r"""200""" + RESET + r"""▓████▀█        ▄▀
               ▀█████████▀▀▀▀     ▀▄▀


          ██▓▒░::SAFE TO USE::░▒▓██

""")

AUTHORIZED_NOTE = (
    BOLD + ORANGE + "Note: " + RESET + """The inserted USB device has been successfully authenticated using the predefined security key. The system has verified the presence and integrity of the key file, confirming that the device is trusted. No suspicious or malicious activity has been detected during the validation process. Therefore, access is permitted and the USB device is considered safe for use within the system.\n
"""
)


UNAUTHORIZED_ART = (
   "\033[0m" + r"""

      ░░▒▓█▄▀::UNAUTHORIZED USB!::▀▄█▓▒░░
   
           
             ▄█████████▄▄▄▄        █ █
            ▐ ███▓""" + "\033[31m" + r"""#!""" + RESET + r"""▓████▀█         █
             ▀█████████▀▀▀▀        █ █


         ██▓▒░::NOT SAFE TO USE::░▒▓██

""")

UNAUTHORIZED_NOTE = (
    BOLD + RED + "Warning: " + RESET + """An unauthorized USB device has been detected. The system could not verify the presence or validity of the required security key, indicating that the device is not trusted. This may pose a potential security risk such as data theft or malware injection. As a precautionary measure, the system has restricted access and initiated security actions to protect the system.\n
"""
)


REMOVED_ART = r"""
        ██▓▒░::USB NOT FOUND!::░▒▓██


                         / ██▓▒░
           ▄█████████▄▄▄   ██▓▒░
          ▐ ██████████▀█ ~ ██▓▒░
           ▀█████████▀▀▀   ██▓▒░
                         \ ██▓▒░


          ██▓▒░::USB EJECTED::░▒▓██


""" + BOLD + ORANGE + """Note: """ + RESET + """The USB device has been removed from the system. Any previously detected activity associated with the device has been terminated, and the system has returned to its normal monitoring state. Continuous surveillance is maintained to detect any new device connections.
"""



# =========================================


def get_active_user():
    return os.getenv("SUDO_USER") or getpass.getuser()


def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    user = get_active_user()

    cmd = f'sudo -u {user} DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u {user})/bus gnome-screenshot -f {filename}'
    os.system(cmd)

    return filename


def capture_webcam():
    filename = f"webcam_{int(time.time())}.jpg"

    cam = cv2.VideoCapture(0)
    time.sleep(2)

    ret, frame = cam.read()
    if ret:
        cv2.imwrite(filename, frame)

    cam.release()
    return filename


def log_event(reason="Unauthorized USB"):
    now = datetime.now()

    user = getpass.getuser()
    system = platform.system() + " " + platform.release()
    hostname = socket.gethostname()

    try:
        ip = socket.gethostbyname(hostname)
    except:
        ip = "Unknown"

    with open(LOG_FILE, "a") as f:
        f.write(f"Intrusion attempt at {now}\n")

    with open(LOG_FILE, "a") as f:
        f.write("\n========== INTRUSION DETECTED ==========\n")
        f.write(f"Time       : {now}\n")
        f.write(f"Reason     : {reason}\n")
        f.write(f"User       : {user}\n")
        f.write(f"System     : {system}\n")
        f.write(f"Hostname   : {hostname}\n")
        f.write(f"IP Address : {ip}\n")
        f.write("========================================\n\n")


def send_email(log, attachments):
    try:
        yag = yagmail.SMTP(EMAIL, APP_PASSWORD)
        yag.send(RECEIVER, "🚨 USB Intrusion Detected", log, attachments)
    except Exception as e:
        print("Email error:", e)


def get_mount_points(base_device):
    mounts = []
    for _ in range(5):
        with open("/proc/mounts", "r") as f:
            for line in f:
                if base_device in line:
                    mounts.append(line.split()[1])
        if mounts:
            return list(set(mounts))
        time.sleep(1)
    return []


def is_usb_present(base_device):
    return os.path.exists(base_device)


def persistent_lock():
    global current_intrusion_device

    print("[#] Persistent protection activated...")

    while True:
        if not current_intrusion_device:
            break

        if not is_usb_present(current_intrusion_device):
            print("[✓] USB removed. Stopping protection.")
            print(REMOVED_ART)
            current_intrusion_device = None
            break

        os.system("loginctl lock-session")
        time.sleep(5)


def check_usb(base_device):
    mount_points = get_mount_points(base_device)

    authorized = False

    for mount_path in mount_points:
        key_path = os.path.join(mount_path, "key.txt")

        if os.path.exists(key_path):
            try:
                with open(key_path, "r") as f:
                    if f.read().strip() == SECRET_KEY:
                        authorized = True
                        break
            except:
                pass

    if authorized:
        print(f"[✔] USB Authorized ({base_device})")
       #  show_intrusion("FOUND")
        print(AUTHORIZED_ART)
        # print(AUTHORIZED_NOTE)
        show_intrusion("FOUND")
        print(AUTHORIZED_NOTE)
        return

    print(f"[!] USB Unauthorized ({base_device})")
   # show_intrusion("NOT FOUND")
    print(UNAUTHORIZED_ART)
  #  print(UNAUTHORIZED_NOTE)
    show_intrusion("NOT FOUND")
    print(UNAUTHORIZED_NOTE)
    screenshot = take_screenshot()
    webcam = capture_webcam()

    log_event("Unauthorized USB detected")

    message = f"""
🚨 USB Intrusion Detected

Time: {datetime.now()}
User: {getpass.getuser()}
"""

    send_email(message, [screenshot, webcam, LOG_FILE])

    global current_intrusion_device
    current_intrusion_device = base_device

    threading.Thread(target=persistent_lock, daemon=True).start()


def monitor_usb():
    global processed_devices, device_map, current_intrusion_device

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    print("[::] Monitoring USB devices...")

    for action, device in monitor:

        if device.device_node is None:
            continue

        base_device = device.device_node.rstrip("0123456789")

        if action == "add" and device.device_type == "partition":

            time.sleep(2)

            if base_device not in processed_devices:
                processed_devices.add(base_device)
                check_usb(base_device)

        elif action == "remove":

            if base_device in processed_devices:

                processed_devices.discard(base_device)

                if base_device in device_map:
                    device_map.pop(base_device, None)

                if current_intrusion_device == base_device:
                    current_intrusion_device = None

                print(f"[::] USB Removed ({base_device}) → Monitoring continues")
                print(REMOVED_ART)


if __name__ == "__main__":
    try:
        monitor_usb()
    except KeyboardInterrupt:
        print("\n[✓] USB monitoring stopped safely")
        print("[✓] Exiting cleanly...")
