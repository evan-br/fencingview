# FencingView - Copilot Instructions

FencingView is a computer vision library for analyzing epee fencing matches from video. It combines YOLO person detection, MediaPipe pose estimation, and custom heuristics for movement and action classification.

## Architecture Overview

The project follows a **layered pipeline** architecture with three distinct responsibilities:

### Layer 1: Vision (Raw Detection)
- **`src/fencingview/epee/vision.py`** - `FencingVision` class
  - Handles YOLO detection (class 0 = person) and MediaPipe pose extraction
  - Always returns **exactly 2 players** sorted left-to-right (Player A, Player B)
  - Converts crop-relative landmarks to frame-absolute coordinates
  - Does NOT interpret what actions are happening
  - Key outputs: bboxes, center coordinates, 33 landmark keypoints

### Layer 2: Motion Analysis (Scouting)
- **`src/fencingview/epee/scouting.py`** - Two classes:
  - `MovementTracker`: Tracks horizontal (X-axis) center movement history
    - Stores last 6 frames (configurable via `history_len`)
    - Returns "advancing", "retreating", or "stopped"
    - Direction logic is inverted for players A (left) vs B (right)
  - `ActionClassifier`: Heuristic-based pose classification
    - Currently uses bbox height ratio vs baseline for "lunge" vs "en garde" (ready)
    - Incomplete: Should use `geometry.py` angle calculations for arm/leg positions

### Layer 3: Match Orchestration
- **`src/fencingview/epee/match.py`** - `EpeeMatch` class
  - Coordinates the pipeline: Vision → Movement → Action classification
  - Maintains baseline heights (for comparing body compression during lunges)
  - **Generator pattern**: `analyze()` yields frame data instead of batch processing
  - Each frame output includes frame_id, player IDs (A/B), bboxes, actions, movements, keypoints
  - Sets baseline on first detection of each player (used for lunge detection)

### Utilities
- **`src/fencingview/common/geometry.py`** - Helper functions
  - `calculate_distance(p1, p2)`: Euclidean distance
  - `calculate_angle(a, b, c)`: Angle at vertex b (in degrees)

## What the Current Code Does (Determination Guarantees)

### Per-Frame Processing Guarantee
Every frame from the video **will undergo this deterministic pipeline**:

1. **Frame Capture**: OpenCV reads frame sequentially
2. **YOLO Detection**: Always detects people (or returns empty if <2 players)
3. **Player Extraction**: Takes ALL detected people, filters class 0 (person), sorts by X position
4. **MediaPipe Extraction**: Crops each player region, extracts 33 landmarks
5. **Coordinate Transformation**: Converts all 33 landmarks from crop-space to frame-space
6. **Baseline Assignment**: First frame of each player → stores baseline height
7. **Movement Tracking**: Updates 6-frame history of center_x, determines direction
8. **Pose Classification**: Compares current bbox height to baseline → "lunge" or "en garde"
9. **Output Yields**: Generator yields frame_data dict with all player info
10. **Optional Preview**: If `show_preview=True`, draws HUD and displays frame (press 'q' to exit)

### Data Structure Yielded Per Frame
```python
frame_data = {
    "frame_id": 42,  # Sequential frame number
    "players": {
        "A": {
            "bbox": (x1, y1, x2, y2),           # Frame coordinates
            "center": (cx, cy),                  # Bbox center
            "action": "en garde" | "lunge",    # Current pose
            "movement": "advancing" | "retreating" | "stopped",  # Direction
            "keypoints": [(gx1, gy1), ...],     # 33 landmarks in frame coords
        },
        "B": {
            # Same structure for right player
        }
    }
}
```

### Invariants (Always True)
- **Exactly 2 players or 0**: If <2 people detected, `frame_data["players"]` is empty
- **Player A always left, B always right**: Sorting by X position guarantees this
- **All coordinates are frame-absolute**: No crop-relative values leak into output
- **Baseline is set once per player, never changes**: Even if player moves far/near camera
- **Movement direction inverted for A vs B**: Same physical motion → opposite delta sign
- **Landmarks are (x, y) tuples in frame space**: Ready for geometric calculations with `geometry.py`

## Key Patterns & Conventions

### Import Strategy
- `test_script.py` shows the pattern: Add `src` to sys.path at startup
- Models default to `yolov8n.pt` at project root (configurable via `EpeeMatch(config={"yolo_path": "..."})`

### Player Identification & Positioning Guarantee
- **Fixed assumption**: Exactly 2 players detected every frame
- **Deterministic**: Always sorted by X coordinate (left → right = A → B)
  - Player A = leftmost player (lower X values)
  - Player B = rightmost player (higher X values)
  - Sorting key: `(x1 + x2) // 2` (bounding box center X)
- **Baseline tracking prevents hardcoding player heights**

### Pose Estimation & Coordinate Calculation
The vision layer performs a **two-stage coordinate transformation**:

**Stage 1: YOLO Person Detection**
- Detects people globally in the frame (640×480 or full resolution)
- Returns bounding boxes in **frame coordinates**: `(x1, y1, x2, y2)`
- YOLO class 0 = person; all detections are filtered by confidence threshold (default 0.8)

**Stage 2: MediaPipe Pose Extraction in Crop Space**
- Extracts the bounding box region as a crop: `frame[y1:y2, x1:x2]`
- Runs MediaPipe on the crop (faster, more accurate pose within region of interest)
- MediaPipe returns **33 landmarks normalized to [0, 1]** relative to crop dimensions
- Example: shoulder at crop coordinates `(0.3, 0.2)` with crop size `[100, 200]` → `(30, 40)` in crop space

**Stage 3: Coordinate Transformation to Frame Space**
- Critical step: Convert crop-relative coordinates back to **frame-absolute coordinates**
- Formula: `global_coord = crop_offset + (landmark_normalized × crop_size)`
  - `gx = x1 + (lm.x × (x2 - x1))`
  - `gy = y1 + (lm.y × (y2 - y1))`
- Result: All 33 landmarks are now in frame pixel coordinates, comparable across frames

**MediaPipe Landmark Indices (33 points)**
- 0-10: Head/face (nose, eyes, ears)
- 11-14: Upper body (shoulders 11/12, elbows 13/14)
- 15-16: Wrists
- 17-18: Pinkies, 19-20: Index fingers, 21-22: Thumbs
- 23-24: Hips
- 25-28: Knees/ankles
- 29-32: Foot details
- **For fencing**: Indices 11-14 (shoulders/elbows) are key for arm extension detection

### Position Tracking & Movement History
- **Player center**: Calculated as `((x1 + x2) // 2, (y1 + y2) // 2)` from bbox
- **X-axis (horizontal) movement**:
  - `MovementTracker` stores center_x values in a deque (last 6 frames by default)
  - Compares earliest vs latest: `delta = current_x - first_x`
  - Threshold: 4 pixels default (tunable)
- **Direction interpretation**:
  - Player A (left): positive delta = moving right = "advancing" (toward opponent)
  - Player B (right): negative delta = moving left = "advancing" (toward opponent)

### Baseline Height Normalization
- On first frame each player is detected, their bbox height is stored: `baseline_height[player_id] = (y2 - y1)`
- Used to normalize lunge detection across video quality variations
- Lunge threshold: `current_height < baseline_height × 0.88` (12% compression indicates bent knees/lunge)
- Prevents false positives if video resolution changes or player moves closer/farther from camera

### Generator Pattern
- `match.analyze(show_preview=True)` is a generator, not a list return
- Use `for data in match.analyze()` - enables real-time processing without loading entire video
- OpenCV preview loop (`cv2.waitKey()`) breaks when user presses 'q'

### Action Classification Status
- **Incomplete**: `ActionClassifier.classify_pose()` is a stub with only height-based lunge detection
- **TODO**: Implement proper arm angle, leg extension, and stance heuristics using MediaPipe landmarks

## Development Workflow

### Setup
```bash
pip install -e .          # Install package in dev mode (reads pyproject.toml)
python test_script.py     # Run analysis on epee1.mp4
```

### Adding Features
1. **Raw detection improvements**: Modify `FencingVision.process_frame()` (YOLO/MediaPipe)
2. **Movement analysis**: Extend `MovementTracker` (more history, velocity calculations)
3. **Action classification**: Implement geometric heuristics in `ActionClassifier` using `geometry.py` angle calculations
4. **Output enhancement**: Add fields to frame_data dict in `EpeeMatch.analyze()`

### Testing
- Manual: Run `test_script.py` with a video file (`epee1.mp4`)
- Verify: Check that exactly 2 players are detected and frame data is yielded correctly
- Debug: Use `_draw_hud()` helper in `match.py` to visualize detections on preview frames

## Dependencies
- **opencv-python**: Video I/O and rendering
- **ultralytics**: YOLO v8 model loading/inference
- **mediapipe**: 33-point pose skeleton extraction
- **numpy**: Geometric calculations

## Critical Implementation Notes
1. Player "A" is always the left player, "B" is right (never swap based on metadata)
2. Baseline heights prevent false positives in lunge detection across different video qualities
3. MediaPipe landmarks are relative to crop coordinates initially—must convert to frame coordinates
4. YOLO confidence threshold defaults to 0.8 (tunable in `FencingVision.__init__`)
5. The generator pattern is intentional for real-time streaming support—don't convert to batch processing
