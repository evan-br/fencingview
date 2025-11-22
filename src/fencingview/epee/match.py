import cv2
import os
from .vision import FencingVision
from .scouting import MovementTracker, ActionClassifier


class EpeeMatch:
    """
    Orchestrate the complete fencing analysis pipeline.
    
    Coordinates three layers:
    1. Vision: YOLO detection + MediaPipe pose extraction
    2. Scouting: Movement tracking + action classification
    3. Analysis: Frame-by-frame results via generator
    
    The analyze() method yields frame data dict for each processed frame,
    enabling real-time streaming and memory-efficient batch processing.
    
    Attributes:
        video_path (str): Path to input video file
        config (dict): Configuration parameters
        vision (FencingVision): Vision layer instance
        trackers (dict): Movement trackers for each player
        baselines (dict): Baseline heights for lunge detection
        
    Example:
        >>> match = EpeeMatch("path/to/match.mp4")
        >>> for frame_data in match.analyze(show_preview=True):
        ...     print(f"Frame {frame_data['frame_id']}: {frame_data['players']}")
    """
    
    def __init__(self, video_path, config=None):
        """
        Initialize match analysis pipeline.
        
        Args:
            video_path (str): Path to video file (MP4, AVI, MOV, etc.)
            config (dict, optional): Configuration dictionary with keys:
                - "yolo_path" (str): Path to YOLO model file.
                  Default: "yolov8n.pt"
                  
        Raises:
            FileNotFoundError: If video_path does not exist
            ValueError: If video_path is None or empty
        """
        if not video_path:
            raise ValueError("video_path cannot be None or empty")
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        self.video_path = video_path
        self.config = config or {}
        
        # Initialize vision layer
        model_path = self.config.get("yolo_path", "yolov8n.pt")
        self.vision = FencingVision(yolo_model_path=model_path)
        
        # Initialize scouting layer
        self.trackers = {"A": MovementTracker(), "B": MovementTracker()}
        self.baselines = {"A": None, "B": None}

    def analyze(self, show_preview=True):
        """
        Process video frame-by-frame and yield analysis results.
        
        This is a generator function that processes frames sequentially without
        loading the entire video into memory. Press 'q' in preview window to exit.
        
        Args:
            show_preview (bool): Display video with HUD overlay. Default: True
            
        Yields:
            dict: Frame data with structure:
                {
                    "frame_id": int,  # Sequential frame number
                    "players": {
                        "A": {  # Left player
                            "bbox": (x1, y1, x2, y2),
                            "center": (cx, cy),
                            "action": "en garde" | "lunge",
                            "movement": "advancing" | "retreating" | "stopped",
                            "keypoints": [(x, y), ...]  # 33 MediaPipe points
                        },
                        "B": { ... }  # Right player
                    }
                }
                
                If <2 players detected, frame_data["players"] is empty.
                
        Raises:
            FileNotFoundError: If video cannot be opened
            RuntimeError: If vision processing fails
            
        Note:
            Baseline heights set on first detection of each player (never changes).
            This prevents false positives if video quality varies.
        """
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {self.video_path}")

        print(f"[FencingView] Starting analysis of: {self.video_path}")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Layer 1: Vision
                players = self.vision.process_frame(frame)
                frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                frame_data = {"frame_id": frame_id, "players": {}}

                # Process only if exactly 2 players detected
                if len(players) == 2:
                    for p in players:
                        pid = p["id"]
                        cx = p["center"][0]
                        bbox_h = p["bbox"][3] - p["bbox"][1]
                        
                        # Layer 2: Baseline height (first detection only)
                        if self.baselines[pid] is None:
                            self.baselines[pid] = bbox_h
                        
                        # Layer 2: Movement tracking
                        self.trackers[pid].update(cx)
                        mov_dir = self.trackers[pid].get_direction(pid)
                        
                        # Layer 2: Pose classification
                        pose = ActionClassifier.classify_pose(
                            p["landmarks"],
                            bbox_h,
                            self.baselines[pid]
                        )
                        
                        # Compile results
                        frame_data["players"][pid] = {
                            "bbox": p["bbox"],
                            "center": p["center"],
                            "action": pose,
                            "movement": mov_dir,
                            "keypoints": p["landmarks"]
                        }

                        # Optional: Draw HUD overlay
                        if show_preview:
                            self._draw_hud(frame, p, mov_dir, pose)

                # Display preview if requested
                if show_preview:
                    cv2.imshow("FencingView v0.0.1", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                # Yield results to caller
                yield frame_data
                
        finally:
            cap.release()
            if show_preview:
                cv2.destroyAllWindows()
            print("[FencingView] Analysis completed")

    def _draw_hud(self, frame, player_data, movement, pose):
        """
        Draw visual HUD overlay on frame for debugging.
        
        Internal helper function. Displays:
        - Bounding box with player label
        - Movement direction
        - Pose classification
        
        Args:
            frame (np.ndarray): Video frame to draw on (modified in-place)
            player_data (dict): Player detection data
            movement (str): Movement classification
            pose (str): Pose classification
        """
        x1, y1, x2, y2 = player_data["bbox"]
        
        # Color: Green for A (left), Orange for B (right)
        color = (0, 255, 0) if player_data["id"] == "A" else (0, 128, 255)
        
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Draw label: "A/B: movement | pose"
        label = f"{player_data['id']}: {movement} | {pose}"
        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )
