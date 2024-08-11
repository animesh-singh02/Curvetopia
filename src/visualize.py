import numpy as np
import matplotlib.pyplot as plt

def plot(paths_XYs, colours, output_path):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for i, XYs in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            XY = np.array(XY)  # Ensure XY is a NumPy array
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    plt.savefig(output_path)
    plt.close(fig)
