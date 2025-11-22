# FencingView Demo - How to Run

This directory contains example scripts demonstrating how to use FencingView for analyzing epee fencing videos.

## Quick Start

### 1. **Basic Usage** (with preview window)

```bash
# From project root directory
python examples/demo_analysis.py
```

This will analyze the default video file `epee1.mp4` (if it exists) and display a live preview with player detection overlay.

**What you'll see:**
- Live video with bounding boxes around detected players
- Real-time pose and movement classification
- Frame-by-frame analysis in console

**Controls:**
- Press `q` to quit the preview window early

---

### 2. **Analyze a Custom Video**

```bash
python examples/demo_analysis.py path/to/your/match.mp4
```

Supported formats: MP4, AVI, MOV, MKV, etc. (any format OpenCV supports)

---

### 3. **Fast Analysis (No Preview)**

```bash
python examples/demo_analysis.py --no-preview path/to/video.mp4
```

Faster processing without GUI preview. Useful for:
- Running on servers or headless systems
- Batch processing multiple videos
- Analyzing very long videos

---

## Output Explanation

The demo prints progress and sample output:

```
🎬 Loading video: epee1.mp4
🔬 Starting analysis...
  ✓ Frame 30 processed
  
  Frame 31 Sample:
    Player A: en garde | advancing
    Player B: lunge | retreating

  ✓ Frame 60 processed

==================================================
✅ Analysis Complete!
   Total frames processed: 1205
   Frames with 2 players: 1180
   Detection rate: 97.9%
==================================================
```

**Meanings:**
- **`en garde`** = Ready position (standing upright)
- **`lunge`** = Attack position (body bent forward)
- **`advancing`** = Moving toward opponent
- **`retreating`** = Moving away from opponent
- **`stopped`** = No movement detected
- **Detection rate** = Percentage of frames where both players were detected

---

## Advanced Usage

### Write Custom Analysis Script

You can extend `demo_analysis.py` or create your own script:

```python
from fencingview import EpeeMatch

# Load video
match = EpeeMatch("path/to/video.mp4")

# Process frame by frame
for frame_data in match.analyze(show_preview=False):
    frame_id = frame_data["frame_id"]
    players = frame_data["players"]
    
    if "A" in players and "B" in players:
        player_a = players["A"]
        player_b = players["B"]
        
        # Access data:
        bbox_a = player_a["bbox"]              # (x1, y1, x2, y2)
        action_a = player_a["action"]          # "en garde" or "lunge"
        movement_a = player_a["movement"]      # "advancing", "retreating", "stopped"
        keypoints_a = player_a["keypoints"]    # 33 MediaPipe landmarks
        
        # Do something with the data
        print(f"Frame {frame_id}: A={action_a} {movement_a}")
```

### Export Data to CSV

```python
import csv
from fencingview import EpeeMatch

match = EpeeMatch("video.mp4")

with open("analysis.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["frame", "player", "action", "movement"])
    
    for frame_data in match.analyze(show_preview=False):
        for player_id, data in frame_data["players"].items():
            writer.writerow([
                frame_data["frame_id"],
                player_id,
                data["action"],
                data["movement"]
            ])

print("✅ Saved to analysis.csv")
```

### Extract Lunges Only

```python
from fencingview import EpeeMatch

match = EpeeMatch("video.mp4")
lunges = []

for frame_data in match.analyze(show_preview=False):
    for player_id, data in frame_data["players"].items():
        if data["action"] == "lunge":
            lunges.append({
                "frame": frame_data["frame_id"],
                "player": player_id,
                "bbox": data["bbox"]
            })

print(f"Found {len(lunges)} lunge frames")
for lunge in lunges[:5]:  # Show first 5
    print(lunge)
```

---

## Troubleshooting

### Error: "Video file not found"
```bash
# Make sure the video exists and path is correct
python examples/demo_analysis.py ./videos/match.mp4

# Or use absolute path
python examples/demo_analysis.py /home/user/fencing/match.mp4
```

### Error: "Cannot import fencingview"
```bash
# Make sure you're in project root directory
cd /path/to/fencingview
python examples/demo_analysis.py

# Or install package locally
pip install -e .
python examples/demo_analysis.py
```

### Slow Performance
- Use `--no-preview` flag (removes GUI overhead)
- Try a shorter video for testing
- Ensure no other GPU-intensive apps are running
- YOLO model downloads on first use (~100MB)

### No Players Detected
- Check video quality (very low resolution may fail)
- Ensure both fencers are visible in frame
- Try with a different video
- Check console for YOLO/MediaPipe errors

---

## Next Steps

- Read main [README.md](../README.md) for full API documentation
- Check [Architecture docs](../docs/) for technical details
- Explore source code in `src/fencingview/`

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/evan-br/fencingview/issues
- Check documentation: `docs/` folder
