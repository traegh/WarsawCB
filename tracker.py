# tracker.py
import cv2
import numpy as np
import time
from scipy.spatial import KDTree

class TargetTracker:
    def __init__(self, config):
        self.config = config
        self.current_target = None
        self.last_seen_time = 0
        self.previous_frame_gray = None
        self.last_tracked_points = None

        self.lk_params = dict(
            winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        )
        self.feature_params = dict(
            maxCorners=100,
            qualityLevel=0.05,
            minDistance=7,
            blockSize=7
        )

    def _get_best_target(self, targets, fov_center_x, fov_center_y):
        if not targets: return None
        tree = KDTree([t['center'] for t in targets])
        distance, index = tree.query((fov_center_x, fov_center_y))
        
        assist_range = self.config.get('AIM_ASSIST_RANGE')
        if distance < assist_range:
            return targets[index]
        return None

    def update(self, frame, potential_targets, fov_center_x, fov_center_y):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        best_direct_target = self._get_best_target(potential_targets, fov_center_x, fov_center_y)

        if best_direct_target:
            self.current_target = best_direct_target
            self.last_seen_time = time.time()

            mask = np.zeros_like(frame_gray)
            cv2.drawContours(mask, [best_direct_target['contour']], -1, 255, -1)
            self.last_tracked_points = cv2.goodFeaturesToTrack(frame_gray, mask=mask, **self.feature_params)
        
        elif self.current_target and self.config.get("OPTICAL_FLOW_ENABLED"):
            if self.last_tracked_points is not None and self.previous_frame_gray is not None:

                new_points, status, _ = cv2.calcOpticalFlowPyrLK(self.previous_frame_gray, frame_gray, self.last_tracked_points, None, **self.lk_params)
                
                if new_points is not None and status.sum() > 4: 
                    good_new = new_points[status == 1]
                    good_old = self.last_tracked_points[status == 1]
                    

                    new_center = np.mean(good_new, axis=0)
                    self.current_target['center'] = (int(new_center[0]), int(new_center[1]))
                    self.last_tracked_points = good_new.reshape(-1, 1, 2)
                else:
                    self.current_target = None 
            else:
                self.current_target = None 
        
        if self.current_target and (time.time() - self.last_seen_time > self.config.get("TARGET_MEMORY_DURATION")):
            self.current_target = None
            self.last_tracked_points = None

        self.previous_frame_gray = frame_gray.copy()
        return self.current_target