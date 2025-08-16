import threading
import json
import os
import numpy as np
import logging

class SharedConfig:
    def __init__(self, filename="config.json"):
        self.lock = threading.Lock()
        self.default_filename = filename
        self.current_filepath = filename
        self.key_order = [
            "ACTIVE_COLOR_PROFILE", "FPS_LIMIT", "DEBUG_WINDOW_VISIBLE",
            "AIM_ASSIST_ENABLED", "TRIGGERBOT_ENABLED",
            "AIM_MODE",
            "WINDMOUSE_G", "WINDMOUSE_W", "WINDMOUSE_M", "WINDMOUSE_D", "TARGET_LOCK_THRESHOLD",
            "AIM_ACQUIRING_SPEED", "AIM_TRACKING_SPEED", "AIM_JITTER", "MOUSE_SENSITIVITY", "AIM_ASSIST_RANGE",
            "AIM_VERTICAL_DAMPING_FACTOR", "AIM_ASSIST_DELAY", "AIM_HEADSHOT_MODE", "HEADSHOT_OFFSET_PERCENT",
            "DEADZONE",
            "MIN_CONTOUR_AREA", "DILATE_ITERATIONS", "DILATE_KERNEL_WIDTH", "DILATE_KERNEL_HEIGHT",
            "ERODE_ITERATIONS", "ERODE_KERNEL_WIDTH", "ERODE_KERNEL_HEIGHT",
            "SANDWICH_CHECK_HEIGHT", "SANDWICH_CHECK_SCAN_WIDTH",
            "SHOT_DURATION", "SHOT_COOLDOWN", "TRIGGERBOT_DELAY_MS",
            "LOWER_YELLOW_H", "LOWER_YELLOW_S", "LOWER_YELLOW_V",
            "UPPER_YELLOW_H", "UPPER_YELLOW_S", "UPPER_YELLOW_V",
            "FOV_RESOLUTION"
        ]
        self.hardcoded_settings = {
            "FOV_RESOLUTIONS_MAP": {
                "128x128": (896, 476), "160x160": (880, 460), "192x192": (864, 444),
                "224x224": (848, 428), "256x256": (832, 412), "288x288": (816, 396),
                "320x320": (800, 380), "352x352": (784, 364), "384x384": (768, 348),
                "416x416": (752, 332), "448x448": (736, 316), "480x480": (720, 300),
                "512x512": (704, 284), "544x544": (688, 268), "576x576": (672, 252),
                "608x608": (656, 236), "640x640": (640, 220)
            }
        }
        self.color_profiles = { "purple-new": {"lower": [144, 106, 172], "upper": [151, 255, 255]}, "yellow": {"lower": [30, 113, 131], "upper": [32, 255, 255]} }
        default_profile = self.color_profiles["purple-new"]
        self.defaults = {
            "ACTIVE_COLOR_PROFILE": "purple-new", "FPS_LIMIT": 240,
            "LOWER_YELLOW_H": default_profile["lower"][0], "LOWER_YELLOW_S": default_profile["lower"][1], "LOWER_YELLOW_V": default_profile["lower"][2],
            "UPPER_YELLOW_H": default_profile["upper"][0], "UPPER_YELLOW_S": default_profile["upper"][1], "UPPER_YELLOW_V": default_profile["upper"][2],
            "is_running": False,
            "AIM_ASSIST_ENABLED": True, "TRIGGERBOT_ENABLED": True,
            "DEBUG_WINDOW_VISIBLE": True,
            "AIM_MODE": "Hybrid",
            "WINDMOUSE_G": 7.0, "WINDMOUSE_W": 3.0, "WINDMOUSE_M": 12.0, "WINDMOUSE_D": 10.0, "TARGET_LOCK_THRESHOLD": 8.0,
            "AIM_ACQUIRING_SPEED": 0.15, "AIM_TRACKING_SPEED": 0.04, "AIM_JITTER": 0.0,
            "MOUSE_SENSITIVITY": 0.350, "AIM_ASSIST_RANGE": 23,
            "AIM_VERTICAL_DAMPING_FACTOR": 0.15, "AIM_ASSIST_DELAY": 0.080,
            "AIM_HEADSHOT_MODE": True, "HEADSHOT_OFFSET_PERCENT": 18,
            "DEADZONE": 2,
            "MIN_CONTOUR_AREA": 40, "DILATE_ITERATIONS": 2, "DILATE_KERNEL_WIDTH": 3, "DILATE_KERNEL_HEIGHT": 3,
            "ERODE_ITERATIONS": 1, "ERODE_KERNEL_WIDTH": 2, "ERODE_KERNEL_HEIGHT": 2,
            "SANDWICH_CHECK_HEIGHT": 15, "SANDWICH_CHECK_SCAN_WIDTH": 5,
            "SHOT_DURATION": 0.1, "SHOT_COOLDOWN": 0.15, "TRIGGERBOT_DELAY_MS": 10,
            "FOV_RESOLUTION": "256x256"
        }
        self.settings = self.defaults.copy()
        self.settings.update(self.hardcoded_settings)
        self.load_from(self.default_filename, is_default=True)

    def get(self, key):
        with self.lock: return self.settings.get(key)
    def set(self, key, value):
        if key in self.hardcoded_settings: return
        with self.lock: self.settings[key] = value
    def get_hsv_lower(self):
        with self.lock: return np.array([self.settings['LOWER_YELLOW_H'], self.settings['LOWER_YELLOW_S'], self.settings['LOWER_YELLOW_V']])
    def get_hsv_upper(self):
        with self.lock: return np.array([self.settings['UPPER_YELLOW_H'], self.settings['UPPER_YELLOW_S'], self.settings['UPPER_YELLOW_V']])
    def get_dilate_kernel(self):
        with self.lock: return np.ones((self.settings['DILATE_KERNEL_HEIGHT'], self.settings['DILATE_KERNEL_WIDTH']), np.uint8)
    def get_erode_kernel(self):
        with self.lock: return np.ones((self.settings['ERODE_KERNEL_HEIGHT'], self.settings['ERODE_KERNEL_WIDTH']), np.uint8)
    def load_from(self, filepath, is_default=False):
        if not os.path.exists(filepath):
            if is_default: self.save_to(filepath)
            else: logging.getLogger(__name__).error(f"Config file not found at '{filepath}'"); return False
        try:
            with open(filepath, 'r') as f: loaded_settings = json.load(f)
            with self.lock:
                self.settings.update(self.defaults)
                for key, value in loaded_settings.items():
                    if key in self.settings and key not in self.hardcoded_settings:
                        self.settings[key] = value
                self.settings.update(self.hardcoded_settings)
            self.current_filepath = filepath
            logging.getLogger(__name__).info(f"Settings loaded from '{os.path.basename(filepath)}'")
            return True
        except Exception as e:
            logging.getLogger(__name__).exception(f"Error reading config file '{filepath}'")
            return False
    def save_to(self, filepath):
        with self.lock:
            settings_to_save = {key: self.settings.get(key, self.defaults.get(key)) for key in self.key_order if key in self.settings}
        with open(filepath, 'w') as f: json.dump(settings_to_save, f, indent=4)
        self.current_filepath = filepath
        logging.getLogger(__name__).info(f"Settings saved to '{os.path.basename(filepath)}'")