import numpy as np
from scipy.spatial import distance

def is_straight_line(XY, tolerance=0.01):
    line_vector = XY[-1] - XY[0]
    line_length = np.linalg.norm(line_vector)
    if line_length == 0:
        return False
    unit_line_vector = line_vector / line_length
    for point in XY[1:-1]:
        vector = point - XY[0]
        projection_length = np.dot(vector, unit_line_vector)
        projection = projection_length * unit_line_vector
        distance_to_line = np.linalg.norm(vector - projection)
        if distance_to_line > tolerance:
            return False
    return True

def is_circle(XY, tolerance=0.01):
    center = np.mean(XY, axis=0)
    distances = np.linalg.norm(XY - center, axis=1)
    return np.std(distances) < tolerance

def is_rectangle(XY, tolerance=0.01):
    if len(XY) != 5 or not np.allclose(XY[0], XY[-1]):
        return False
    angles = []
    for i in range(4):
        vec1 = XY[i+1] - XY[i]
        vec2 = XY[(i+2) % 4] - XY[i+1]
        angle = np.arccos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        angles.append(angle)
    return np.allclose(angles, [np.pi/2, np.pi/2, np.pi/2, np.pi/2], atol=tolerance)

def regularize_curves(paths_XYs):
    regularized_paths = []
    for XYs in paths_XYs:
        regularized_XYs = []
        for XY in XYs:
            if is_straight_line(XY):
                regularized_XYs.append([XY[0], XY[-1]])
            elif is_circle(XY):
                center = np.mean(XY, axis=0)
                radius = np.mean(np.linalg.norm(XY - center, axis=1))
                angle = np.linspace(0, 2 * np.pi, len(XY))
                regularized_XY = np.array([center + radius * np.array([np.cos(a), np.sin(a)]) for a in angle])
                regularized_XYs.append(regularized_XY)
            elif is_rectangle(XY):
                # Find the bounding box
                min_x, min_y = np.min(XY, axis=0)
                max_x, max_y = np.max(XY, axis=0)
                regularized_XY = np.array([
                    [min_x, min_y],
                    [min_x, max_y],
                    [max_x, max_y],
                    [max_x, min_y],
                    [min_x, min_y]
                ])
                regularized_XYs.append(regularized_XY)
            else:
                # If not a regular shape, keep the original
                regularized_XYs.append(XY)
        regularized_paths.append(regularized_XYs)
    return regularized_paths
