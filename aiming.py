import numpy as np
import random
import time
import threading

class Aimer:
    def __init__(self, config, mouse_controller):
        self.config = config
        self.mouse = mouse_controller
        self.is_aiming = False
        self.aim_thread = None
        self.stop_event = threading.Event()

    def start_aim(self, target, fov_center_x, fov_center_y, is_on_target):
        if self.is_aiming:
            return

        self.is_aiming = True
        self.stop_event.clear()
        self.aim_thread = threading.Thread(
            target=self._aim_worker, 
            args=(target, fov_center_x, fov_center_y, is_on_target), 
            daemon=True
        )
        self.aim_thread.start()

    def stop_aim(self):
        if not self.is_aiming:
            return
        
        self.stop_event.set()
        if self.aim_thread:
            self.aim_thread.join(timeout=0.05)
        self.is_aiming = False

    def _aim_worker(self, target, fov_center_x, fov_center_y, is_on_target):
        try:
            sensitivity = max(self.config.get("MOUSE_SENSITIVITY"), 0.01)
            
            if is_on_target:
                speed = self.config.get("AIM_TRACKING_SPEED")
                jitter_strength = 0
                vertical_damping = self.config.get("AIM_VERTICAL_DAMPING_FACTOR")
                target_x, target_y = target['center']
            else:
                speed = self.config.get("AIM_ACQUIRING_SPEED")
                jitter_strength = self.config.get("AIM_JITTER")
                vertical_damping = 1.0

                target_x, target_y = target['center']
                if self.config.get('AIM_HEADSHOT_MODE'):
                    _, y, _, h = target['rect']
                    offset = self.config.get("HEADSHOT_OFFSET_PERCENT") / 100.0
                    target_y = y + int(h * offset)

            if self.stop_event.is_set():
                return

            dx_raw = target_x - fov_center_x
            dy_raw = target_y - fov_center_y
            
            distance = np.hypot(dx_raw, dy_raw)
            if distance < self.config.get("DEADZONE"):
                return

            dx = dx_raw * speed
            dy = dy_raw * speed * vertical_damping
            
            jitter_x = random.uniform(-jitter_strength, jitter_strength)
            jitter_y = random.uniform(-jitter_strength, jitter_strength)
            
            move_x = (dx + jitter_x) / sensitivity
            move_y = (dy + jitter_y) / sensitivity
            
            if abs(move_x) > 0.5 or abs(move_y) > 0.5:
                self.mouse.move(move_x, move_y)
            
            time.sleep(0.001)

        finally:
            self.is_aiming = False