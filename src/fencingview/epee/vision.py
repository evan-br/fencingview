import cv2
import numpy as np
from ultralytics import YOLO
import mediapipe as mp


class FencingVision:
    """
    Extract raw detection data from video frames.
    
    Responsible exclusively for:
    - YOLO person detection (class 0)
    - MediaPipe 33-point pose skeleton extraction
    - Coordinate transformation (crop-space to frame-space)
    
    Always returns exactly 2 players (sorted left-to-right as A and B).
    
    Attributes:
        yolo: Loaded YOLO model instance
        pose: MediaPipe Pose extractor
        conf: YOLO confidence threshold (0.0-1.0)
        
    Example:
        >>> vision = FencingVision(yolo_model_path="yolov8n.pt", conf_threshold=0.8)
        >>> players = vision.process_frame(frame)
        >>> print(len(players))  # 0, 1, or 2
    """
    
    def __init__(self, yolo_model_path="yolov8n.pt", conf_threshold=0.8):
        """
        Initialize FencingVision with YOLO and MediaPipe models.
        
        Args:
            yolo_model_path (str): Path to YOLO model file.
                Default: "yolov8n.pt" (nano model, auto-downloaded if not found)
            conf_threshold (float): YOLO detection confidence threshold.
                Range: [0.0, 1.0]. Default: 0.8
                
        Raises:
            RuntimeError: If YOLO model cannot be loaded
            ValueError: If conf_threshold is outside valid range
            
        Note:
            MediaPipe uses model_complexity=1 (balanced speed/accuracy)
            for real-time processing.
        """
        if not isinstance(conf_threshold, (int, float)) or not (0.0 <= conf_threshold <= 1.0):
            raise ValueError(f"conf_threshold must be in [0.0, 1.0], got {conf_threshold}")
        
        print(f"[FencingView] Loading YOLO model from: {yolo_model_path}")
        try:
            self.yolo = YOLO(yolo_model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load YOLO model: {e}")
            
        print("[FencingView] Loading MediaPipe Pose model...")
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, model_complexity=1)
        self.conf = conf_threshold
        print("[FencingView] Models loaded successfully")

    def process_frame(self, frame):
        """
        Extract player data from a single video frame.
        
        Performs:
        1. YOLO person detection on full frame
        2. Sorts detections by X-coordinate (left to right)
        3. Extracts top-2 bounding boxes
        4. MediaPipe pose estimation on each bbox crop
        5. Transforms landmarks from crop-space to frame-space
        
        Args:
            frame (np.ndarray): BGR image array from OpenCV (HxWx3)
            
        Returns:
            list[dict]: List of detected players (0, 1, or 2 players).
                Each dict contains:
                - "id" (str): "A" (left) or "B" (right)
                - "bbox" (tuple): (x1, y1, x2, y2) in frame coordinates
                - "center" (tuple): (cx, cy) center point
                - "landmarks" (list): [(x, y), ...] 33 MediaPipe points
                
        Raises:
            ValueError: If frame is None or has invalid shape
            
        Note:
            - Always returns exactly 2 players or empty list (never 1)
            - Landmarks are in absolute frame coordinates (not crop-relative)
            - Player A is always left, Player B always right
        """
        if frame is None or not isinstance(frame, np.ndarray):
            raise ValueError("frame must be a numpy ndarray")
        
        if len(frame.shape) != 3 or frame.shape[2] != 3:
            raise ValueError(f"frame must be (H, W, 3), got {frame.shape}")
        
        h, w = frame.shape[:2]
        
        # 1. YOLO Detection on full frame
        results = self.yolo(frame, verbose=False, conf=self.conf)[0]
        
        detected_boxes = []
        for box in results.boxes:
            cls = int(box.cls[0])
            if cls == 0:  # Person class ID in COCO
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detected_boxes.append((x1, y1, x2, y2))

        # 2. Need at least 2 players for analysis
        if len(detected_boxes) < 2:
            return []
            
        # 3. Sort left-to-right by center X coordinate
        detected_boxes.sort(key=lambda b: (b[0] + b[2]) // 2)
        
        # 4. Take only top-2 (ignore extras like referees, audience)
        main_players_boxes = detected_boxes[:2]

        players_data = []
        
        for idx, bbox in enumerate(main_players_boxes):
            x1, y1, x2, y2 = bbox
            
            # 5. Extract crop and apply bounds checking
            crop = frame[max(0, y1):min(h, y2), max(0, x1):min(w, x2)]
            if crop.size == 0:
                continue
                
            # 6. MediaPipe pose on crop
            crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            pose_result = self.pose.process(crop_rgb)
            
            landmarks_global = []
            if pose_result.pose_landmarks:
                for lm in pose_result.pose_landmarks.landmark:
                    # Transform: crop-relative [0,1] to frame-absolute pixel coords
                    gx = int(x1 + lm.x * (x2 - x1))
                    gy = int(y1 + lm.y * (y2 - y1))
                    landmarks_global.append((gx, gy))
            
            players_data.append({
                "id": "A" if idx == 0 else "B",
                "bbox": bbox,
                "center": ((x1 + x2) // 2, (y1 + y2) // 2),
                "landmarks": landmarks_global
            })
            
        return players_data