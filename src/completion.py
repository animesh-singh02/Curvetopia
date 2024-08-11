import numpy as np

def find_endpoints(XY):
    # Detect endpoints in the curve
    diffs = np.diff(XY, axis=0)
    distances = np.linalg.norm(diffs, axis=1)
    mean_distance = np.mean(distances)
    std_distance = np.std(distances)
    endpoints = []
    for i in range(len(distances)):
        if distances[i] > mean_distance + 2 * std_distance:
            endpoints.append(i)
    return endpoints

def interpolate_curve(start, end, num_points=100):
    t = np.linspace(0, 1, num_points)
    interpolated_points = (1 - t)[:, None] * start + t[:, None] * end
    return interpolated_points

def complete_curves(paths_XYs):
    completed_paths = []
    for XYs in paths_XYs:
        completed_XYs = []
        for XY in XYs:
            endpoints = find_endpoints(XY)
            if len(endpoints) == 2:
                start_idx, end_idx = endpoints
                start_point = XY[start_idx]
                end_point = XY[end_idx]
                interpolated_curve = interpolate_curve(start_point, end_point)
                completed_XY = np.vstack([XY[:start_idx+1], interpolated_curve, XY[end_idx:]])
                completed_XYs.append(completed_XY)
            else:
                completed_XYs.append(XY)
        completed_paths.append(completed_XYs)
    return completed_paths
