from typing import Optional, Dict
import numpy as np


class PoseEstimator:
    def __init__(self) -> None:
        self.enabled = False

    def get_pose(self, frame: np.ndarray) -> Optional[Dict]:
        return None

    def draw_pose(self, frame: np.ndarray, pose_results: Dict) -> np.ndarray:
        return frame
