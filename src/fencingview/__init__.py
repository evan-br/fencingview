"""
FencingView: Computer Vision library for analyzing epee fencing matches.

Combines YOLO person detection, MediaPipe pose estimation, and custom heuristics
for movement and action classification from video.

Example:
    >>> from fencingview import EpeeMatch
    >>> match = EpeeMatch("path/to/video.mp4")
    >>> for frame_data in match.analyze(show_preview=True):
    ...     players = frame_data["players"]
    ...     print(f"Frame {frame_data['frame_id']}: {players}")
"""

__version__ = "0.0.1"
__author__ = "Evandro Rissatto Pereira"
__email__ = "erissatto@gmail.com"
__license__ = "MIT"

from fencingview.epee.match import EpeeMatch
from fencingview.epee.vision import FencingVision
from fencingview.common.geometry import calculate_distance, calculate_angle

__all__ = [
    "EpeeMatch",
    "FencingVision",
    "calculate_distance",
    "calculate_angle",
]
