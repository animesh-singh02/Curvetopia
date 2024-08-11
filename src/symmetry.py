import numpy as np

def detect_symmetry(paths_XYs):
    symmetrical_shapes = []
    for shape in paths_XYs:
        if has_symmetry(shape):
            symmetrical_shapes.append(shape)
    return symmetrical_shapes

def has_symmetry(shape):
    # Check for vertical, horizontal, and rotational symmetry
    return (has_vertical_symmetry(shape) or
            has_horizontal_symmetry(shape) or
            has_rotational_symmetry(shape))

def has_vertical_symmetry(shape):
    # Check for vertical symmetry
    centroid = np.mean(shape, axis=0)
    mirrored_shape = np.copy(shape)
    mirrored_shape[:, 0] = 2 * centroid[0] - mirrored_shape[:, 0]  # Mirror across vertical line
    return np.allclose(np.sort(shape, axis=0), np.sort(mirrored_shape, axis=0))

def has_horizontal_symmetry(shape):
    # Check for horizontal symmetry
    centroid = np.mean(shape, axis=0)
    mirrored_shape = np.copy(shape)
    mirrored_shape[:, 1] = 2 * centroid[1] - mirrored_shape[:, 1]  # Mirror across horizontal line
    return np.allclose(np.sort(shape, axis=0), np.sort(mirrored_shape, axis=0))

def has_rotational_symmetry(shape):
    # Check for rotational symmetry (180 degrees)
    centroid = np.mean(shape, axis=0)
    rotated_shape = np.copy(shape)
    rotated_shape = np.array([rotate_point(point, centroid, 180) for point in shape])
    return np.allclose(np.sort(shape, axis=0), np.sort(rotated_shape, axis=0))

def rotate_point(point, center, angle):
    # Rotate a point around a center by a given angle in degrees
    angle_rad = np.radians(angle)
    cos_angle = np.cos(angle_rad)
    sin_angle = np.sin(angle_rad)
    
    # Translate point back to origin
    point -= center
    
    # Rotate point
    x_new = point[0] * cos_angle - point[1] * sin_angle
    y_new = point[0] * sin_angle + point[1] * cos_angle
    
    # Translate point back
    return np.array([x_new, y_new]) + center

# Example usage
if __name__ == "__main__":
    # Example shapes (as numpy arrays)
    shapes = [
        np.array([[0, 0], [1, 0], [1, 1], [0, 1]]),  # Square (symmetrical)
        np.array([[0, 0], [2, 0], [1, 1]]),  # Triangle (not symmetrical)
        np.array([[0, 0], [1, 0], [0, 1], [1, 1]]),  # Rectangle (symmetrical)
        np.array([[0, 0], [1, 1], [2, 0], [1, -1]])  # Non-symmetrical shape
    ]

    symmetrical_shapes = detect_symmetry(shapes)
    for shape in symmetrical_shapes:
        print("Symmetrical shape:", shape)