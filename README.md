# Python Keylogger (Educational Use Only)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-yellow)
![License](https://img.shields.io/badge/License-None-lightgrey)

---

## Overview

This is an **Python-based keylogger** designed purely for **educational purposes** to demonstrate the capabilities and risks of modern keylogging tools.  
It includes the following features:

- Logs **keyboard inputs** with context on the active window.
- Detects and logs **clipboard contents** when paste (Ctrl+V) occurs.
- Takes periodic **screenshots** and uploads them.
- Sends logs and screenshots securely via **Discord webhook**.
- Optionally **encrypts** logs locally with AES (Fernet).
- **Hides the console window** for stealth.
- Includes basic **sandbox detection** to avoid analysis environments.
- Configurable logging and screenshot intervals.
- Saves encrypted logs locally in `%APPDATA%`.

---

## ⚠️ WARNING

This tool is designed **for educational and authorized testing only.**  
**Unauthorized use is illegal and unethical.**  
Always get explicit permission before running this tool on any system.

---

## Features

| Feature                         | Description                                       |
| -------------------------------|-------------------------------------------------|
| Keyboard Hook                  | Logs all keystrokes, including special keys     |
| Window Focus Detection         | Logs keystrokes by active window title           |
| Clipboard Monitoring           | Detects and logs clipboard content on paste     |
| Screenshot Capture             | Takes screenshots at configurable intervals     |
| Discord Webhook Integration   | Sends logs & screenshots to your Discord server |
| Local Log Encryption           | AES encryption of saved logs with Fernet        |
| Console Hiding                 | Makes program run stealthily                      |
| Sandbox Environment Detection | Exits if running in VM or sandbox environment   |

---

## Prerequisites

- **Windows OS** (due to use of `win32api` and related modules)  
- Python 3.8 or newer  
- Install required packages:

```bash
pip install -r requirements.txt
```
