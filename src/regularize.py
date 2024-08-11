import numpy as np
import cv2
from scipy.spatial import ConvexHull

def regularize_shapes(paths_XYs):
    regularized_paths = []
    for shape in paths_XYs:
        if is_circle(shape):
            regularized_paths.append(regularize_circle(shape))
        elif is_ellipse(shape):
            regularized_paths.append(regularize_ellipse(shape))
        elif is_rectangle(shape):
            regularized_paths.append(regularize_rectangle(shape))
        elif is_rounded_rectangle(shape):
            regularized_paths.append(regularize_rounded_rectangle(shape))
        elif is_regular_polygon(shape):
            regularized_paths.append(regularize_polygon(shape))
        elif is_star_shape(shape):
            regularized_paths.append(regularize_star(shape))
        elif is_straight_line(shape):
            regularized_paths.append(regularize_line(shape))
        else:
            regularized_paths.append(shape)  # If no shape is recognized, return the original
    return regularized_paths

# Helper functions
def is_straight_line(shape):
    return len(shape) == 2

def regularize_line(shape):
    return shape

def is_circle(shape):
    center = np.mean(shape, axis=0)
    distances = np.linalg.norm(shape - center, axis=1)
    return np.std(distances) < 0.1  # Threshold for circularity

def regularize_circle(shape):
    center = np.mean(shape, axis=0)
    radius = np.mean(np.linalg.norm(shape - center, axis=1))
    return create_circle(center, radius)

def is_ellipse(shape):
    (center, axes, angle) = cv2.fitEllipse(shape)
    distances = []
    for point in shape:
        dist = np.linalg.norm(point - center)
        major_axis = max(axes)
        minor_axis = min(axes)
        expected_dist = major_axis * minor_axis / np.sqrt((major_axis * np.cos(np.radians(angle)))**2 + (minor_axis * np.sin(np.radians(angle)))**2)
        distances.append(abs(dist - expected_dist))
    return np.mean(distances) < 0.1  # Adjust the threshold as needed

def regularize_ellipse(shape):
    (center, axes, angle) = cv2.fitEllipse(shape)
    center = np.array(center, dtype=np.float32)
    axes = np.array(axes, dtype=np.float32)
    angle = np.radians(angle)
    return center, axes, angle

def is_rectangle(shape):
    return len(shape) == 4 and is_rectangle_shape(shape)

def is_rounded_rectangle(shape):
    if len(shape) < 4:
        return False
    epsilon = 0.02 * cv2.arcLength(shape, True)
    approx = cv2.approxPolyDP(shape, epsilon, True)
    if len(approx) != 4:
        return False
    distances = [np.linalg.norm(approx[i] - approx[(i + 1) % 4]) for i in range(4)]
    return np.std(distances) < 0.1 * np.mean(distances)  # Check if sides are similar

def regularize_rectangle(shape):
    x, y, w, h = cv2.boundingRect(shape)
    return np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])

def regularize_rounded_rectangle(shape):
    x, y, w, h = cv2.boundingRect(shape)
    radius = min(w, h) / 10  # Example radius for rounded corners
    return (np.array([[x + radius, y], [x + w - radius, y],
                      [x + w, y + radius], [x + w, y + h - radius],
                      [x + w - radius, y + h], [x + radius, y + h],
                      [x, y + h - radius], [x, y + radius]]), radius)

def is_regular_polygon(shape):
    if len(shape) < 3:
        return False
    distances = [np.linalg.norm(shape[i] - shape[(i + 1) % len(shape)]) for i in range(len(shape))]
    angles = []
    for i in range(len(shape)):
        v1 = shape[i] - shape[(i - 1) % len(shape)]
        v2 = shape[(i + 1) % len(shape)] - shape[i]
        angle = np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0))
        angles.append(np.degrees(angle))
    return np.std(distances) < 0.1 * np.mean(distances) and np.std(angles) < 0.1 * np.mean(angles)

def regularize_polygon(shape):
    return shape[np.argsort(shape[:, 0])]  # Sort by x-coordinate

def is_star_shape(shape):
    if len(shape) < 5:
        return False
    centroid = np.mean(shape, axis=0)
    distances = np.linalg.norm(shape - centroid, axis=1)
    angles = np.arctan2(shape[:, 1] - centroid[1], shape[:, 0] - centroid[0])
    long_distance_threshold = np.mean(distances) * 1.5
    short_distance_threshold = np.mean(distances) * 0.5
    long_count = sum(d > long_distance_threshold for d in distances)
    short_count = sum(d < short_distance_threshold for d in distances)
    return long_count >= 5 and short_count >= 5  # Adjust counts as needed

def regularize_star(shape):
    centroid = np.mean(shape, axis=0)
    distances = np.linalg.norm(shape - centroid, axis=1)
    angles = np.arctan2(shape[:, 1] - centroid[1], shape[:, 0] - centroid[0])
    sorted_indices = np.argsort(angles)
    star_points = []
    for i in range(len(shape)):
        short_distance = np.mean(distances) * 0.5
        long_distance = np.mean(distances) * 1.5
        angle = angles[sorted_indices[i]]
        star_points.append(centroid + short_distance * np.array([np.cos(angle), np.sin(angle)]))
        star_points.append(centroid + long_distance * np.array([np.cos(angle), np.sin(angle)]))
    return np.array(star_points)

def create_circle(center, radius):
    # Create a circle representation
    theta = np.linspace(0, 2 * np.pi, 100)
    x = center[0] + radius * np.cos(theta)  # x-coordinate of the circle
    y = center[1] + radius * np.sin(theta)  # y-coordinate of the circle
    return np.column_stack((x, y))

def is_rectangle_shape(points):
    # Check if four points form a rectangle
    # Placeholder for actual implementation
    return True  # This should contain logic to check rectangle properties

# Example usage
if __name__ == "__main__":
    # Example shapes (as numpy arrays)
    shapes = [
        np.array([[0, 0], [1, 1]]),  # Line
        np.array([[0, 0], [1, 0], [1, 1], [0, 1]]),  # Rectangle
        np.array([[0, 0], [1, 0], [0.5, 0.5], [0, 1]])  # Irregular shape
    ]
    
    regularized = regularize_shapes(shapes)
    for shape in regularized:
        print(shape)