# FencingView 🤺

Computer Vision library for analyzing **epee fencing matches** from video.

Combines YOLO person detection, MediaPipe pose estimation, and custom heuristics to extract:
- **Player detection and tracking** (left/right)
- **Movement classification** (advancing, retreating, stopped)
- **Pose estimation** (en garde, lunge)
- **Keypoint landmarks** (33 MediaPipe pose points)

## Features

- ⚡ **Real-time processing** via generator pattern
- 🎯 **Deterministic 2-player detection** (always left/right)
- 📊 **Frame-by-frame analysis** with absolute coordinates
- 🧠 **MediaPipe pose extraction** and coordinate transformation
- 🚀 **Modular architecture** (Vision → Scouting → Analysis)

## Requirements

- Python ≥ 3.9
- YOLO v8 model (`yolov8n.pt`, automatically downloaded on first use)
- Video file in common formats (MP4, AVI, MOV, etc.)

## Installation

```bash
pip install fencingview
```

## Quick Start

```python
from fencingview import EpeeMatch

# Load and analyze video
match = EpeeMatch("path/to/epee_match.mp4")

# Process frame-by-frame
for frame_data in match.analyze(show_preview=True):
    players = frame_data["players"]
    
    if "A" in players and "B" in players:
        player_a = players["A"]
        player_b = players["B"]
        
        print(f"Frame {frame_data['frame_id']}")
        print(f"  Player A: {player_a['action']} - {player_a['movement']}")
        print(f"  Player B: {player_b['action']} - {player_b['movement']}")
    
    # Press 'q' to exit preview window
```

## Output Format

Each frame yields a dictionary with detected players:

```python
frame_data = {
    "frame_id": 42,  # Sequential frame number
    "players": {
        "A": {  # Left player
            "bbox": (x1, y1, x2, y2),                          # Bounding box in frame
            "center": (cx, cy),                                 # Center point
            "action": "en garde" | "lunge",                   # Current pose
            "movement": "advancing" | "retreating" | "stopped",   # Direction
            "keypoints": [(x1, y1), (x2, y2), ...],            # 33 MediaPipe landmarks
        },
        "B": { ... }  # Right player (same structure)
    }
}
```

**Coordinates**: All `(x, y)` are in **frame pixel space** (absolute, not relative to crop).

**MediaPipe Landmarks** (33 points):
- 0-10: Face (nose, eyes, ears)
- 11-14: Upper body (shoulders, elbows)
- 15-16: Wrists
- 23-28: Hips, knees, ankles
- [See MediaPipe documentation for complete reference](https://mediapipe.dev/solutions/pose)

## Architecture

FencingView follows a **layered pipeline** design:

```
Video File
    ↓
[Layer 1: Vision] ← YOLO Detection + MediaPipe Pose
    ↓
[Layer 2: Scouting] ← Movement Tracking + Action Classification
    ↓
[Layer 3: Match] ← Frame Orchestration & Generator
    ↓
Output: frame_data dict per frame
```

### Layer 1: Vision (`FencingVision`)
- Detects people using YOLO v8
- Extracts pose landmarks using MediaPipe
- Transforms crop-relative coordinates to frame-absolute
- Always returns exactly 2 players (sorted left-to-right) or none

### Layer 2: Scouting
- **`MovementTracker`**: Tracks horizontal center position (6-frame history)
  - Classifies direction: advancing, retreating, or stationary
- **`ActionClassifier`**: Estimates pose from bbox height ratio
  - Classifies: en garde (ready) or lunge
  - ⚠️ v0.0.1: Simplistic height-based heuristic (see Roadmap)

### Layer 3: Match (`EpeeMatch`)
- Coordinates the pipeline
- Maintains baseline heights for lunge detection
- Yields frame data via generator (memory efficient)
- Optional preview window with overlay HUD

## Configuration

```python
# Custom YOLO model path
match = EpeeMatch(
    video_path="path/to/video.mp4",
    config={
        "yolo_path": "/path/to/yolov8m.pt"  # Default: yolov8n.pt
    }
)

# Analysis parameters
for frame_data in match.analyze(show_preview=False):  # Disable preview
    # Process silently
```

## Known Limitations (v0.0.1)

- ⚠️ **Pose classification** uses only bbox height (incomplete - see Roadmap)
- ⚠️ **Exactly 2 players** required in frame
- ⚠️ **Movement tracking** on X-axis only (horizontal)
- ⚠️ **No re-identification** across frames (players may swap identity)
- ⚠️ **No multi-match** batch processing

These will be addressed in future releases.

## Usage Examples

### Process entire video and extract statistics

```python
from fencingview import EpeeMatch

match = EpeeMatch("epee_match.mp4")

frame_count = 0
lunge_frames_a = 0
lunge_frames_b = 0

for data in match.analyze(show_preview=False):
    frame_count += 1
    
    if "A" in data["players"] and data["players"]["A"]["action"] == "lunge":
        lunge_frames_a += 1
    
    if "B" in data["players"] and data["players"]["B"]["action"] == "lunge":
        lunge_frames_b += 1

print(f"Total frames: {frame_count}")
print(f"Player A lunges: {lunge_frames_a}")
print(f"Player B lunges: {lunge_frames_b}")
```

### Export keypoints to CSV

```python
import csv
from fencingview import EpeeMatch

match = EpeeMatch("epee_match.mp4")

with open("keypoints.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["frame_id", "player", "landmark_idx", "x", "y"])
    
    for data in match.analyze(show_preview=False):
        for player_id, player_data in data["players"].items():
            for idx, (x, y) in enumerate(player_data["keypoints"]):
                writer.writerow([
                    data["frame_id"],
                    player_id,
                    idx,
                    x,
                    y
                ])
```

## Dependencies

- `opencv-python` ≥ 4.8 - Video I/O and visualization
- `ultralytics` ≥ 8.0 - YOLO v8 model loading
- `mediapipe` ≥ 0.10 - Pose estimation
- `numpy` ≥ 1.21 - Numerical computations

## Contributing

Contributions are welcome! Areas for improvement:

- [ ] Better pose classification using angle-based heuristics
- [ ] Multi-person re-identification
- [ ] Batch video processing
- [ ] Attack/defense action classification
- [ ] Unit tests and benchmarks
- [ ] Documentation improvements

See [GitHub Issues](https://github.com/evan-br/fencingview/issues) for tasks.

## License

MIT License - See [LICENSE](LICENSE) file

## Citation

If you use FencingView in academic research, please cite:

```bibtex
@software{fencingview2025,
  title={FencingView: Computer Vision for Epee Fencing Analysis},
    author={Evandro Rissatto Pereira},
    year={2025},
    url={https://github.com/evan-br/fencingview}
}
```

## Roadmap

### v0.1.0 (Next)
- [ ] Type hints (PEP 484)
- [ ] Improved pose classification (angle-based)
- [ ] Better logging (instead of print)
- [ ] Unit tests

### v0.2.0
- [ ] Batch video processing
- [ ] Configuration file support (YAML)
- [ ] Action history tracking

### v0.3.0
- [ ] Attack/defense classification
- [ ] Frame-to-frame player re-identification
- [ ] Performance benchmarks

### v1.0.0
- [ ] Production-ready stability
- [ ] Full documentation
- [ ] Jupyter notebook tutorials

## Support

For issues, questions, or suggestions:
- 📝 [GitHub Issues](https://github.com/evan-br/fencingview/issues)
- 💬 Discussions in repository

## Acknowledgments

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [MediaPipe](https://github.com/google/mediapipe)
- [OpenCV](https://opencv.org/)

---

**Disclaimer**: v0.0.1 is an alpha release. Pose classification and action detection are simplified heuristics and may not be accurate for competition-grade analysis.
