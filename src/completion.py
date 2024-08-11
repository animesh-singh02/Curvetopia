import numpy as np
import cv2

def complete_curves(paths_XYs):
    completed_paths = []
    for shape in paths_XYs:
        if is_incomplete(shape):
            completed_paths.append(complete_shape(shape))
        else:
            completed_paths.append(shape)
    return completed_paths

def is_incomplete(shape):
    # Check if the shape is incomplete
    # For simplicity, we can consider a shape incomplete if it has less than 3 points
    return len(shape) < 3 or not is_closed(shape)

def is_closed(shape):
    # A shape is considered closed if the first and last points are the same (or within a small threshold)
    distance = np.linalg.norm(shape[0] - shape[-1])
    return distance < 1e-2  # Threshold for closure

def complete_shape(shape):
    # Complete the shape by closing the curve
    if is_closed(shape):
        return shape  # Already closed
    
    # If the shape is incomplete, we can close it by adding a line from the last point to the first point
    closed_shape = np.vstack((shape, shape[0]))  # Append the first point to the end
    return closed_shape

# Example usage
if __name__ == "__main__":
    # Example shapes (as numpy arrays)
    shapes = [
        np.array([[0, 0], [1, 0], [1, 1]]),  # Incomplete shape (triangle)
        np.array([[0, 0], [1, 0], [1, 1], [0, 1]]),  # Complete shape (rectangle)
        np.array([[0, 0], [1, 0], [0.5, 1]])  # Incomplete shape (triangle)
    ]
    
    completed_shapes = complete_curves(shapes)
    for shape in completed_shapes:
        print("Completed shape:", shape)
