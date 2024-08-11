import os
from src.read_csv import read_csv
from src.visualize import plot
from src.regularize import regularize_curves
from src.symmetry import identify_symmetry
from src.completion import complete_curves
from src.svg_conversion import polylines2svg

DATA_DIR = 'data/'
COLOURS = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

def main():
    # Read and process isolated curves
    isolated_paths = read_csv(os.path.join(DATA_DIR, 'isolated.csv'))
    isolated_paths = regularize_curves(isolated_paths)
    isolated_paths = identify_symmetry(isolated_paths)
    plot(isolated_paths, COLOURS, os.path.join(DATA_DIR, 'isolated_plot.png'))
    polylines2svg(isolated_paths, os.path.join(DATA_DIR, 'isolated_output.svg'), COLOURS)
    
    # Read and process fragmented curves
    frag0_paths = read_csv(os.path.join(DATA_DIR, 'frag0.csv'))
    frag1_paths = read_csv(os.path.join(DATA_DIR, 'frag1.csv'))
    frag0_paths = regularize_curves(frag0_paths)
    frag1_paths = identify_symmetry(frag1_paths)
    plot(frag0_paths, COLOURS, os.path.join(DATA_DIR, 'frag0_plot.png'))
    plot(frag1_paths, COLOURS, os.path.join(DATA_DIR, 'frag1_plot.png'))
    polylines2svg(frag0_paths, os.path.join(DATA_DIR, 'frag0_output.svg'), COLOURS)
    polylines2svg(frag1_paths, os.path.join(DATA_DIR, 'frag1_output.svg'), COLOURS)
    
    # Read and process occlusion curves
    occlusion1_paths = read_csv(os.path.join(DATA_DIR, 'occlusion1.csv'))
    occlusion1_paths = complete_curves(occlusion1_paths)
    plot(occlusion1_paths, COLOURS, os.path.join(DATA_DIR, 'occlusion1_plot.png'))
    polylines2svg(occlusion1_paths, os.path.join(DATA_DIR, 'occlusion1_output.svg'), COLOURS)
    
    occlusion2_paths = read_csv(os.path.join(DATA_DIR, 'occlusion2.csv'))
    occlusion2_paths = complete_curves(occlusion2_paths)
    plot(occlusion2_paths, COLOURS, os.path.join(DATA_DIR, 'occlusion2_plot.png'))
    polylines2svg(occlusion2_paths, os.path.join(DATA_DIR, 'occlusion2_output.svg'), COLOURS)

if __name__ == '__main__':
    main()
