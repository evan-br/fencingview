"""
Geometric utility functions for pose analysis.

These functions support landmark-based calculations for pose classification:
- Distance between points (e.g., joint separation)
- Angles at vertices (e.g., elbow bend, knee bend)

Used by ActionClassifier for robust pose estimation.
"""

import math
import numpy as np


def calculate_distance(p1, p2):
    """
    Calculate Euclidean distance between two points.
    
    Args:
        p1 (tuple or list): Point 1 as (x, y)
        p2 (tuple or list): Point 2 as (x, y)
        
    Returns:
        float: Euclidean distance
        
    Example:
        >>> d = calculate_distance((0, 0), (3, 4))
        >>> d
        5.0
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def calculate_angle(a, b, c):
    """
    Calculate angle at vertex b formed by three points.
    
    Computes the angle ∠ABC where b is the vertex using the dot product method.
    
    Args:
        a (tuple or list): Point A as (x, y)
        b (tuple or list): Vertex point as (x, y)
        c (tuple or list): Point C as (x, y)
        
    Returns:
        float: Angle in degrees, range [0, 180]
        
    Raises:
        ValueError: If any point is the same as vertex (zero-length vector)
        
    Example:
        >>> # Right angle
        >>> angle = calculate_angle((0, 1), (0, 0), (1, 0))
        >>> int(angle)
        90
        
        >>> # 45-degree angle
        >>> angle = calculate_angle((0, 1), (0, 0), (1, 1))
        >>> int(angle)
        45
        
    Note:
        Used for pose analysis:
        - Elbow bend (angle between shoulder-elbow-wrist)
        - Knee bend (angle between hip-knee-ankle)
        - Arm extension detection
        
        Indices from MediaPipe Pose (33 points):
        - Shoulders: 11 (left), 12 (right)
        - Elbows: 13 (left), 14 (right)
        - Wrists: 15 (left), 16 (right)
        - Hips: 23 (left), 24 (right)
        - Knees: 25 (left), 26 (right)
        - Ankles: 27 (left), 28 (right)
    """
    ba = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)
    
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    
    if norm_ba == 0 or norm_bc == 0:
        raise ValueError("Point 'a' or 'c' is the same as vertex 'b'")
    
    # Compute cosine of angle using dot product
    cosine = np.dot(ba, bc) / (norm_ba * norm_bc + 1e-8)
    
    # Clamp to [-1, 1] to handle numerical errors
    cosine = np.clip(cosine, -1.0, 1.0)
    
    # Convert radians to degrees
    angle_radians = np.arccos(cosine)
    angle_degrees = np.degrees(angle_radians)
    
    return float(angle_degrees)
