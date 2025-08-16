import cv2
import numpy as np
import threading
import time
import logging
import dxcam
from screeninfo import get_monitors

from config import SharedConfig
from hardware import MakcuController
from detection import Detector, visualize_detection, verify_on_target
from aiming import Aimer

logger = logging.getLogger(__name__)

class TriggerbotCore:
    def __init__(self, config: SharedConfig):
        self.config = config
        self.mouse_controller = None
        self.detector = None
        self.aimer = None
        self.camera = None
        self.capture_region = {}
        
        self.last_shot_time = 0
        self.trigger_activated_at = 0
        
        self.debug_windows_active = False
        self.wnd_mask = "Debug: Mask"
        self.wnd_vision = "Debug: Vision"
        
        self.aim_target_first_seen_time = 0

    def setup(self):
        logger.info("Setting up bot core...")
        self.mouse_controller = MakcuController(self.config)
        if not self.mouse_controller.is_connected:
            logger.error("Controller not found, setup failed.")
            return False
        
        self.detector = Detector(self.config)
        self.aimer = Aimer(self.config, self.mouse_controller)
        
        try:
            fov_res_str = self.config.get("FOV_RESOLUTION")
            fov_w, fov_h = map(int, fov_res_str.split('x'))
            
            monitor = get_monitors()[0]
            screen_w, screen_h = monitor.width, monitor.height
            
            capture_left = (screen_w - fov_w) // 2
            capture_top = (screen_h - fov_h) // 2
            
            self.capture_region = (
                capture_left, capture_top, 
                capture_left + fov_w, capture_top + fov_h
            )
            
            self.camera = dxcam.create(output_color="BGR")
            if self.camera is None:
                raise Exception("Failed to create dxcam instance.")
            
            self.camera.start(target_fps=0, region=self.capture_region)
            logger.info(f"Screen capture started for region: {self.capture_region}")
        except Exception as e:
            logger.critical(f"Failed to initialize screen capture: {e}")
            return False
            
        return True

    def shoot_burst(self, duration):
        if self.mouse_controller:
            threading.Thread(target=self._shoot_worker, args=(duration,), daemon=True).start()
    
    def _shoot_worker(self, duration):
        self.mouse_controller.press_left()
        time.sleep(duration)
        self.mouse_controller.release_left()

    def run_one_frame(self):
        frame_start_time = time.perf_counter()
        try:
            show_debug = self.config.get("DEBUG_WINDOW_VISIBLE")
            fov_w = self.capture_region[2] - self.capture_region[0]
            fov_h = self.capture_region[3] - self.capture_region[1]

            if show_debug and not self.debug_windows_active:
                cv2.namedWindow(self.wnd_mask, cv2.WINDOW_NORMAL); cv2.moveWindow(self.wnd_mask, 0, 0)
                cv2.namedWindow(self.wnd_vision, cv2.WINDOW_NORMAL); cv2.moveWindow(self.wnd_vision, fov_w, 0)
                cv2.setWindowProperty(self.wnd_mask, cv2.WND_PROP_TOPMOST, 1); cv2.setWindowProperty(self.wnd_vision, cv2.WND_PROP_TOPMOST, 1)
                self.debug_windows_active = True
            elif not show_debug and self.debug_windows_active:
                cv2.destroyAllWindows(); self.debug_windows_active = False

            frame = self.camera.get_latest_frame()
            if frame is None or not hasattr(frame, 'shape') or frame.size == 0:
                if show_debug:
                    black_screen = np.zeros((fov_h, fov_w, 3), dtype=np.uint8)
                    cv2.putText(black_screen, "NO SIGNAL", (10, fov_h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    cv2.imshow(self.wnd_mask, black_screen); cv2.imshow(self.wnd_vision, black_screen)
                    cv2.waitKey(1)
                return

            potential_targets, processed_mask = self.detector.run(frame)
            
            crosshair_x = fov_w // 2
            crosshair_y = fov_h // 2
            
            scan_height = self.config.get("SANDWICH_CHECK_HEIGHT")
            scan_width = self.config.get("SANDWICH_CHECK_SCAN_WIDTH")
            is_on_target = verify_on_target(processed_mask, crosshair_x, crosshair_y, scan_height, scan_width)

            if self.config.get("TRIGGERBOT_ENABLED"):
                if is_on_target:
                    if self.trigger_activated_at == 0:
                        self.trigger_activated_at = time.time()
                    
                    delay_ms = self.config.get('TRIGGERBOT_DELAY_MS')
                    if (time.time() - self.trigger_activated_at) * 1000 >= delay_ms:
                        shot_d = self.config.get('SHOT_DURATION')
                        shot_c = self.config.get('SHOT_COOLDOWN')
                        if (time.time() - self.last_shot_time) > (shot_d + shot_c):
                            self.shoot_burst(shot_d)
                            self.last_shot_time = time.time()
                else:
                    self.trigger_activated_at = 0

            if self.config.get("AIM_ASSIST_ENABLED"):
                target_in_range = None
                if potential_targets:
                    distances = [np.hypot(t['center'][0] - crosshair_x, t['center'][1] - crosshair_y) for t in potential_targets]
                    best_index = np.argmin(distances)
                    if distances[best_index] < self.config.get("AIM_ASSIST_RANGE"):
                        target_in_range = potential_targets[best_index]
                
                aim_delay = self.config.get('AIM_ASSIST_DELAY')
                if target_in_range:
                    if self.aim_target_first_seen_time == 0:
                        self.aim_target_first_seen_time = time.time()
                    
                    if time.time() - self.aim_target_first_seen_time > aim_delay:
                        self.aimer.start_aim(target_in_range, crosshair_x, crosshair_y, is_on_target)
                    else:
                        self.aimer.stop_aim()
                else:
                    self.aim_target_first_seen_time = 0
                    self.aimer.stop_aim()
            
            if show_debug:
                mask_display = cv2.cvtColor(processed_mask, cv2.COLOR_GRAY2BGR)
                vision_display = visualize_detection(frame.copy(), potential_targets)
                
                trigger_color = (0, 255, 0) if is_on_target else (0, 0, 255)
                
                scan_x_start = max(0, crosshair_x - scan_width // 2)
                scan_x_end = min(fov_w, crosshair_x + scan_width // 2 + 1)
                
                for display in [mask_display, vision_display]:
                    cv2.rectangle(display, (scan_x_start, max(0, crosshair_y - scan_height)), (scan_x_end, crosshair_y), trigger_color, 1)
                    cv2.rectangle(display, (scan_x_start, crosshair_y + 1), (scan_x_end, min(fov_h, crosshair_y + scan_height + 1)), trigger_color, 1)
                cv2.imshow(self.wnd_mask, mask_display); cv2.imshow(self.wnd_vision, vision_display)
                if cv2.waitKey(1) & 0xFF == ord('q'): self.config.set('is_running', False)
        
        except Exception as e:
            logger.exception("An unhandled exception occurred during a frame run")
            self.config.set('is_running', False)
        
        finally:
            target_fps = self.config.get("FPS_LIMIT")
            if target_fps > 0:
                target_frame_time = 1 / target_fps
                elapsed_time = time.perf_counter() - frame_start_time
                sleep_time = target_frame_time - elapsed_time
                if sleep_time > 0:
                    time.sleep(sleep_time)

    def cleanup(self):
        logger.info("Cleaning up bot core resources...")
        if self.aimer: self.aimer.stop_aim()
        if self.camera: self.camera.stop()
        cv2.destroyAllWindows()
        if self.mouse_controller: self.mouse_controller.disconnect()