import cv2
import numpy as np

class Detector:
    def __init__(self, config):
        self.config = config

    def run(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_bound = self.config.get_hsv_lower()
        upper_bound = self.config.get_hsv_upper()
        color_mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

        dilate_kernel = self.config.get_dilate_kernel()
        dilate_iter = self.config.get('DILATE_ITERATIONS')
        dilated_mask = cv2.dilate(color_mask, dilate_kernel, iterations=dilate_iter)

        erode_kernel = self.config.get_erode_kernel()
        erode_iter = self.config.get('ERODE_ITERATIONS')
        processed_mask = cv2.erode(dilated_mask, erode_kernel, iterations=erode_iter)

        contours, _ = cv2.findContours(processed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        valid_targets = []
        if contours:
            for c in contours:
                if cv2.contourArea(c) > self.config.get("MIN_CONTOUR_AREA"):
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        x, y, w, h = cv2.boundingRect(c)
                        valid_targets.append({'contour': c, 'center': (cx, cy), 'rect': (x, y, w, h)})
        
        return valid_targets, processed_mask

def verify_on_target(mask, scan_center_x, scan_center_y, scan_height, scan_width):
    mask_h, mask_w = mask.shape[:2]
    
    scan_x_start = max(0, scan_center_x - scan_width // 2)
    scan_x_end = min(mask_w, scan_center_x + scan_width // 2 + 1)
    
    y_above_start = max(0, scan_center_y - scan_height)
    y_above_end = max(0, scan_center_y)
    
    y_below_start = min(mask_h, scan_center_y + 1)
    y_below_end = min(mask_h, scan_center_y + scan_height + 1)
    
    is_pixel_above = False
    if y_above_end > y_above_start:
        scan_area_above = mask[y_above_start:y_above_end, scan_x_start:scan_x_end]
        is_pixel_above = np.any(scan_area_above)
        
    is_pixel_below = False
    if y_below_end > y_below_start:
        scan_area_below = mask[y_below_start:y_below_end, scan_x_start:scan_x_end]
        is_pixel_below = np.any(scan_area_below)
        
    return is_pixel_above and is_pixel_below

def visualize_detection(debug_img, targets):
    for target in targets:
        x, y, w, h = target['rect']
        cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(debug_img, target['center'], 3, (0, 0, 255), -1)
    return debug_img