import numpy as np
from regularize import regularize_shapes
from symmetry import detect_symmetry
from completion import complete_curves
from visualization import polylines2svg

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def main():
    input_path = 'C:/Users/KIIT/OneDrive/Desktop/Curvetopia/data/frag1.csv'
    output_path = 'C:/Users/KIIT/OneDrive/Desktop/Curvetopia/output/detected_shapes.svg'  # Path to save the output SVG file

    # Read the shapes from the CSV file
    try:
        paths_XYs = read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        return

    # Regularize the shapes
    regularized_shapes = regularize_shapes(paths_XYs)

    # Detect symmetrical shapes
    symmetrical_shapes = detect_symmetry(regularized_shapes)

    # Complete the curves of the shapes
    completed_shapes = complete_curves(symmetrical_shapes)

    # Visualize the completed shapes and save as SVG
    polylines2svg(completed_shapes, output_path)

if __name__ == "__main__":
    main()