import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tkinter as tk
from tkinter import filedialog
import os


def create_animation_from_csv(file_path, output_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Extract data columns
    position_values = data.iloc[:, 0]
    radius = data.iloc[:, 1].abs()
    theta = np.deg2rad(data.iloc[:, 2])

    # Set up the figure for the combined visualization
    fig = plt.figure(figsize=(12, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[2, 1])

    # Set up the polar plot
    ax1 = fig.add_subplot(gs[0], projection='polar')
    ax1.set_theta_zero_location('S')
    ax1.set_theta_direction(1)
    ax1.set_title("M3F Tilt Magnitude and Direction")
    line, = ax1.plot([], [], lw=2)

    # Pre-compute the maximum radial limit
    # max_rlim = max(radius) + 0.1 * max(radius)
    max_rlim = 1
    ax1.set_rlim(0, max_rlim)

    # Set up the vertical bar
    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0.45, 0.55)  # Narrow the x-axis range to reduce horizontal space
    ax2.xaxis.set_visible(False)  # Hide the x-axis
    ax2.set_ylim(0, 1.5)  # Set the y-axis maximum to 1.5
    ax2.set_title("Position Visualization")
    rect = plt.Rectangle((0.47, 0), 0.06, 0, color='blue')
    ax2.add_patch(rect)

    # Remove the borders
    for spine in ax2.spines.values():
        spine.set_visible(False)

    # Set custom y-axis labels
    ax2.set_yticks([0, 0.75, 1.5])
    ax2.set_yticklabels(['0', '0.75', '1.5'])

    # Animation function
    def animate(i):
        line.set_data(theta[:i], radius[:i])
        rect.set_height(position_values[i])
        return line, rect

    # Create the animation
    ani = FuncAnimation(fig, animate, frames=len(theta), blit=False, repeat=False)
    writer = PillowWriter(fps=8)
    ani.save(output_path, writer=writer)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    # Allow selection of multiple CSV files
    input_files = filedialog.askopenfilenames(title="Select the CSV files",
                                              filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    # Create the output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TiltGraph Output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for input_file in input_files:
        # Extract the base name of the input file and construct the name for the output file
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, "tiltgraph_" + base_name + ".gif")

        create_animation_from_csv(input_file, output_file)
