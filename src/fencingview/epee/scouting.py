from collections import deque
import math
import numpy as np
from ..common.geometry import calculate_angle


class MovementTracker:
    """
    Track player horizontal movement to classify direction.
    
    Maintains a history of center_x positions (default 6 frames) and compares
    current vs oldest position to determine movement direction.
    
    Direction logic is inverted for left/right players:
    - Player A (left): positive X delta = advancing toward opponent
    - Player B (right): negative X delta = advancing toward opponent
    
    Attributes:
        history (deque): Last N center_x values
        threshold (int): Pixel delta threshold for classification
        
    Example:
        >>> tracker = MovementTracker(history_len=6, threshold_px=4)
        >>> tracker.update(320)  # center_x = 320
        >>> tracker.update(325)  # center_x = 325
        >>> direction = tracker.get_direction("A")  # "stopped" initially
    """
    
    def __init__(self, history_len=6, threshold_px=4):
        """
        Initialize movement tracker.
        
        Args:
            history_len (int): Number of frames to track. Default: 6
            threshold_px (int): Pixel movement threshold for classification.
                Default: 4 pixels
        """
        self.history = deque(maxlen=history_len)
        self.threshold = threshold_px

    def update(self, center_x):
        """
        Update position history with current frame's center X coordinate.
        
        Args:
            center_x (float): Horizontal center position of bounding box
        """
        self.history.append(center_x)

    def get_direction(self, player_side="A"):
        """
        Classify movement direction based on position history.
        
        Args:
            player_side (str): "A" (left player) or "B" (right player)
            
        Returns:
            str: One of "advancing" (advancing), "retreating" (retreating),
                or "stopped" (stopped)
                
        Note:
            Requires at least 2 frames in history. Returns "stopped" if insufficient.
        """
        if len(self.history) < 2:
            return "stopped"
        
        delta = self.history[-1] - self.history[0]
        
        # Direction logic inverted for each player
        if player_side == "A":
            # Left player: positive delta = advancing toward right (opponent)
            if delta > self.threshold:
                return "advancing"
            if delta < -self.threshold:
                return "retreating"
        else:
            # Right player: negative delta = advancing toward left (opponent)
            if delta < -self.threshold:
                return "advancing"
            if delta > self.threshold:
                return "retreating"
            
        return "stopped"


class ActionClassifier:
    """
    Heuristic-based pose classification for epee fencing.
    
    Currently uses simple bbox height ratio vs baseline to classify poses.
    
    Note: This version uses height-based heuristics for efficiency. 
    Angle-based classification is planned for future releases
    
    Poses:
        - "en garde": Ready position (baseline height)
        - "lunge": Lunge position (body compressed ~12%)
        - "unknown": Cannot classify (missing landmarks)
    """
    
    @staticmethod
    def classify_pose(landmarks, bbox_height, baseline_height=None):
        """
        Classify current pose based on body measurements.
        
        Args:
            landmarks (list): MediaPipe 33-point landmarks [(x,y), ...].
                Can be empty if detection failed.
            bbox_height (int): Current bounding box height in pixels
            baseline_height (int, optional): Reference height from first detection.
                Used for lunge detection. Default: None
                
        Returns:
            str: Pose classification: "en garde", "lunge", or "unknown"
            
        Raises:
            ValueError: If bbox_height is negative or zero
            
        Note:
            Lunge threshold: bbox_height < baseline_height × 0.88 (12% compression)
            This prevents false positives from slight camera movements.
            
            Note: This version only uses height. Does not use arm/leg angle data yet.
        """
        if not landmarks:
            return "unknown"
        
        if bbox_height <= 0:
            raise ValueError(f"bbox_height must be positive, got {bbox_height}")
        
        # TEMPORARY: Simple height-based heuristic
        # TODO: Implement proper angle-based classification
        # - Use calculate_angle() from geometry module
        # - Check elbow angle (indices 13, 14)
        # - Check knee angle (indices 25, 26)
        # - Combine multi-frame history
        
        if baseline_height is not None and baseline_height > 0:
            height_ratio = bbox_height / baseline_height
            
            # Lunge detection: 12% body compression
            if height_ratio < 0.88:
                return "lunge"
        
        return "en garde"  # Default to ready position
