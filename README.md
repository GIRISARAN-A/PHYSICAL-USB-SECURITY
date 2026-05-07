#  USB Physical Security Tool

A real-time `USB-based` physical security monitoring system built using Python for Linux environments.  
This tool continuously monitors USB device activity and validates connected devices using a predefined secret key stored inside a USB drive.

If an unauthorized USB device is detected, the system can:

- Lock the session
- Capture screenshots
- Capture webcam images
- Send intrusion alert emails
- Generate intrusion logs
- Display terminal-based security dashboard using ASCII art


#  Features

## [ + ] Authorized USB Detection
- Detects trusted USB devices
- Verifies `key.txt`
- Allows system usage

## [ ! ] Unauthorized USB Detection
If validation fails:
- Displays warning dashboard
- Locks user session continuously
- Captures screenshot
- Captures webcam image
- Sends email alert
- Saves logs

## Real-Time Monitoring
- Uses `pyudev`
- Detects USB insertion/removal instantly

# Project Workflow

```text
     USB Inserted
          ↓
Monitor detects device
          ↓
  Search for key.txt
          ↓
  Validate secret key
          ↓
      Authorized?
      _____|_____
    YES          NO
     ↓            ↓
   Allow     Intrusion Actions
   Access          ↓
               Screenshot
             Webcam Capture
               Email Alert
             Persistent Lock

```
#  Technologies Used


| Technology         | Purpose                      |
|-------------------|------------------------------|
| Python            | Main Programming Language    |
| pyudev            | USB Device Monitoring        |
| OpenCV            | Webcam Capture               |
| yagmail           | Email Alert System           |
| gnome-screenshot  | Screenshot Capture           |
| threading         | Background Protection Tasks  |
| ANSI Escape Codes | Colored Terminal UI          |


# 📦 Requirements

###  System Requirements

-   Linux (Ubuntu/Kali recommended

-   Python 3.8+

-   GNOME Desktop Environment
 
# 📚 Python Libraries

Install dependencies using:

```bash

	pip install pyudev yagmail opencv-python

```
`or`
```bash

	pip install -r requirements.txt

```
# ⚙️ Linux Package Requirements

Install screenshot utility:

```bash

	sudo apt install gnome-screenshot

```

----------

# 📁 Project Structure

```text
usb-security/
│
├── main.py
├── key.txt
├── usb_log.txt
├── screenshot_xxx.png
├── webcam_xxx.jpg
└── README.md

```

# 🔑 USB Setup

###  Step 1 — Create Key File
Find USB:
```
cd /media/....
```
Inside your USB drive create:

```text
	key.txt
```

## Step 2 — Add Secret Key

Example:

```text
ACCESS12
```

----------

## Step 3 — Update Program Secret

Inside code:

```python
SECRET_KEY = "ACCESS12"
```

Both must match exactly.



# ▶️ Running the Tool

###  Create Virtual Environment

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

----------

## Install Dependencies

```bash
pip install pyudev yagmail opencv-python

```

## Run Tool

```bash
python3 main.py
```

OR

```bash
sudo .venv/bin/python3 main.py
```

# 🔐 Security Actions

## Authorized USB

-   Displays SAFE TO USE dashboard
    
-   Allows access
    
-   Shows device information


## Unauthorized USB

-   Displays warning dashboard
    
-   Captures screenshot
    
-   Captures webcam image
    
-   Sends email alert
    
-   Locks session repeatedly


# 📧 Email Alert Configuration

Update these fields:

```python
EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
RECEIVER = "receiver@gmail.com"

```

## Gmail App Password Setup

1.  Enable 2-Step Verification
    
2.  Open Google Account
    
3.  Security → App Passwords
    
4.  Generate password
    
5.  Use generated password in script


# 📸 Screenshot Feature

Uses:

```bash
gnome-screenshot
```

Captured screenshots saved automatically.

# 📷 Webcam Capture

Uses OpenCV:

```python
cv2.VideoCapture(0)
```

Captured images stored locally.



# 📝 Log File

All intrusion activities are saved in:

```text
usb_log.txt
```

Example:

```text
========== INTRUSION DETECTED ==========
Time       : 2026-03-30 10:06:38
Reason     : Unauthorized USB detected
User       : root
System     : Linux
Hostname   : girisaran-admin
IP Address : 10.31.15.53
========================================

```

----------

# Terminal Dashboard

## Authorized USB

```text
░░▒▓█▄▀::AUTHORIZED USB::▀▄█▓▒░░
    ██▓▒░::SAFE TO USE::░▒▓██

```

----------

## Unauthorized USB

```text
░░▒▓█▄▀::UNAUTHORIZED USB!::▀▄█▓▒░░
   ██▓▒░::NOT SAFE TO USE::░▒▓██

```

----------

# 🔒 Persistent Lock System

If an unauthorized USB is detected:

```bash
loginctl lock-session
```

The session remains locked until the device is removed.


# 🌐 Information Displayed

The tool displays:

-   Time
    
-   User
    
-   System
    
-   Hostname
    
-   IP Address
    
-   USB Status
    
-   Validation Result
    
-   Intrusion Reason
    

----------

# ⚠️ Limitations

-   Currently optimized for Linux
    
-   Requires mounted USB drives
    
-   Depends on GNOME screenshot service
    
-   Email alerts require internet connection

# 🎓 Educational Purpose

This project demonstrates:

-   USB monitoring
    
-   Physical security concepts
    
-   Intrusion detection
    
-   Endpoint protection
    
-   Real-time system monitoring
    
-   Linux device interaction

----------

# 📜 License

This project is developed for educational and research purposes.
