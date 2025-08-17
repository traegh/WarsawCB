# WarsawCB
An average colorbot for dual-PC setups. Educational purposes only.

<p align="center">
  <img width="256" height="256" alt="WarsawCB Logo" src="https://github.com/user-attachments/assets/c11fb7f9-976f-494e-8feb-f4bdf72a679a" />
</p>

---

## ⚠️ Core Requirements - Read Before Starting

This project has strict requirements. If your setup does not meet them, it will not work correctly.

1.  **Two-PC Setup:** This software runs on a secondary "Radar PC," not your main Gaming PC.
2.  **Hardware Mouse:** A dedicated hardware device from **[Makcu](https://www.makcu.com/)** is **required** for mouse input. It will not work without it.
3.  **Wired Network:** Both PCs must be connected via a **wired Gigabit Ethernet** connection. Wi-Fi will introduce unacceptable latency.
4.  **Fullscreen Video Source:** The game feed on the Radar PC (e.g., from NDI Tools) **must be running in true fullscreen mode**, without any Windows UI elements like the taskbar visible.

## 🚀 Installation

1.  **Install Python:** You need **Python 3.11+**. During installation, you **MUST** check the box that says **"Add Python to PATH"**.
2.  **Unzip:** Extract the project folder to a simple location, like your Desktop.
3.  **Run:** Double-click `start.bat`. The first launch will take a few minutes to install dependencies. Subsequent launches will be fast.

## 🛠️ Troubleshooting

This is an open-source project. You are expected to solve basic issues yourself.

*   **If `start.bat` fails or closes instantly:**
    1.  Open a terminal (CMD or PowerShell) in the project folder.
    2.  Run this command manually: `pip install -r requirements.txt`
    3.  Try running `start.bat` again.

*   **If it still doesn't work:**
    1.  This is now a development issue.
    2.  Install an IDE like **PyCharm Community Edition**.
    3.  Open the project folder in the IDE, let it set up the interpreter, and run `main.py`. The IDE will tell you exactly what's wrong.

> **You have the source code. You have Google. You have AI assistants like ChatGPT, Gemini, and Claude. Use them.**

## ⚙️ Setup & Configuration

The video source setup is your responsibility. I do not provide support for OBS, screen mirroring, or other methods. I personally use a far more efficient, latency-free solution. If the bot is slow or inaccurate, your problem is **latency**.

*   **Main Tab:** Toggles for features, FPS limit, and FOV size (requires restart).
*   **Aiming Tab:** Configure `Classic` (basic) or `Windmouse \ Hybrid` (Humanized) aim assist. Set your in-game sensitivity and a `Deadzone` to prevent jitter on-target.
*   **Detection Tab:** Set HSV color ranges, minimum enemy size (`Min Contour Area`), and use `Dilate`/`Erode` to clean up visual noise.
*   **Advanced Tab:** Fine-tune fire rate and triggerbot delay.

## 🌟 Features

*   **Hybrid Aim Assist:** Blends smooth, human-like movement for flicks with precise tracking.
*   **Triggerbot:** Fires automatically when an enemy is under the crosshair, with a configurable delay.
*   **Advanced Detection:** Fine-tune enemy detection with HSV color profiles and noise filters.
*   **High-Performance Capture:** Utilizes `dxcam` for low-latency screen capture (100-240 FPS).
*   **Live Debug View:** An optional window to see exactly what the bot sees.
*   **Full GUI Control:** All settings are managed through a user-friendly interface with profile saving/loading.

## ⚖️ Disclaimer

This software is for educational purposes. Using it in online games will likely result in a **permanent ban**. You assume all risks. I am not responsible for your game accounts.

---

## A FINAL, IMPORTANT NOTE

**This code is provided as-is and is confirmed to work flawlessly on the development machine. If you encounter issues, the problem is almost certainly with your setup, environment, or latency. Do not create issues or contact me with support questions.**

D1sc0rd: @Elusive1337
