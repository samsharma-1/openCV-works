import math

def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points (x, y)."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def calculate_angle(p1, p2, p3):
    """
    Calculate the angle between three points. p2 is the vertex.
    Returns angle in degrees.
    """
    angle = math.degrees(math.atan2(p3[1] - p2[1], p3[0] - p2[0]) - 
                         math.atan2(p1[1] - p2[1], p1[0] - p2[0]))
    if angle < 0:
        angle += 360
    return angle
