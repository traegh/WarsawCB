# WarsawCB
Colorbot made with love to MAKCU Discord community - educational purposes only
Shout out to:
- iHack
- Ahmad
- Jackslinsmith
- every other person who contributed to MAKCU community, making it a better place.


<p align="center">
  <img width="512" height="512" alt="WV6HgAv" src="https://github.com/user-attachments/assets/c11fb7f9-976f-494e-8feb-f4bdf72a679a" />
</p>

# ✨ WARSAW CB - The Colorbot Project ✨

<p align="center">Precise pixel targeting for a two-PC setup.</p>

---

## ⚠️ Important Note: Two-PC Setup Required ⚠️

**This software is designed exclusively for use on a dual-computer system.**
To keep your main **Gaming PC** clean and dedicated solely to the game, WARSAW CB should be run on a **separate 'Radar PC'**. This setup helps prevent software conflicts and ensures your primary gaming environment remains untainted.

## 🚀 About WARSAW CB

WARSAW CB is a colorbot tool built to assist with in-game precision. It uses efficient screen capture from your Radar PC and works with external hardware for mouse control. The project focuses on being easy to configure and lets you see what's happening in real-time.

## 🌟 What It Does

*   **Hybrid Aim Assist:** Offers a versatile aiming experience, blending smooth Windmouse movement for quick adjustments with precise classic tracking.
*   **Triggerbot:** Automatically fires when an enemy color is detected at your crosshair, after a user-defined delay.
*   **Color Detection:** Adjust HSV color ranges to identify enemies, filter by minimum size, and refine detection with dilation and erosion filters to manage image noise.
*   **Fast Screen Capture:** Captures your screen at high frame rates (100-240 FPS) using `dxcam` for smooth, real-time analysis.
*   **Visual Debugging:** See what the bot 'sees' with an optional debug window, showing detected contours and masks in real-time.
*   **Easy-to-Use Interface:** All settings are configurable through a clear graphical interface. Save and load your favorite setup profiles.

## 🎮 Getting Started (Step-by-Step)

Follow these simple steps to get WARSAW CB running:

1.  **Get the Files:**
    *   Go to the Releases section of this GitHub repository.
    *   Download the latest `.zip` file (e.g., `WARSAW_CB_vX.X.zip`).

2.  **Unpack:**
    *   Extract all contents of the downloaded `.zip` file into any folder on your 'Radar PC' (e.g., `C:\Colorbot`).

3.  **Launch the Program:**
    *   Inside the folder, find and **double-click** the `start.bat` file.

4.  **First Time Setup (Be Patient!):**
    *   The very first time you run `start.bat`, it will set up a dedicated Python environment (`venv`) and install all necessary components. This might take a few minutes, so please wait for it to finish.
    *   Future launches will be much faster.

5.  **Before You Start:**
    *   Make sure you have **Python 3.9 or newer** installed on your 'Radar PC'. When installing Python, **it's very important to check the box that says "Add Python to PATH"**.

## ⚙️ How to Adjust Settings

All bot settings can be changed easily through the graphical interface.

*   **Main Tab:** Turn features on/off, set the FPS limit for screen capture, and pick your FOV capture size (changing FOV needs a program restart!).
*   **Aiming Tab:** Adjust aim assist behavior. Try the `Hybrid` mode – it combines the natural feel of Windmouse for quick movements with the precision of Classic tracking. Set a `Deadzone` in pixels to stop the mouse from making tiny movements when it's already on target.
*   **Detection Tab:** Customize how the bot finds enemies. Set the color range (HSV values), minimum object size (`Min Contour Area`), and play with `Dilate` (to expand detected areas) and `Erode` (to clean up noise after dilation).
*   **Advanced Tab:** Control firing duration, cooldowns, and set the `Triggerbot Delay` (in milliseconds) for when it should shoot after detecting an enemy.

Feel free to experiment with all these settings to find what works best for your specific game and setup! You can save and load different configurations.

## 📚 Project Purpose & Disclaimer

This WARSAW CB project is a purely **academic and educational endeavor**. It was created to explore computer vision, image processing, and hardware interaction concepts.

*   **No Guarantees, No Responsibility:** This software is provided "as is," without any guarantees. The developers and contributors **are not responsible** for any consequences, damage, or issues that may arise from its use.
*   **Account Risk:** Using this software in online competitive games can, and very likely will, violate the game's terms of service. This could lead to permanent account bans or other penalties. We hold **no responsibility** for the status or integrity of your gaming accounts.
*   **Hardware Requirement:** This project is specifically designed to work with a dedicated hardware device from **[Makcu](https://www.makcu.com/)** for mouse input. It will not function correctly without a Makcu device connected to your Radar PC.

---
D1sc0rd: @Elusive1337
