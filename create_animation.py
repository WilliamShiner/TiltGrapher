import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def create_animation_from_csv(file_path, output_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Extract data columns
    positionValues = data.iloc[:, 0]
    radius = data.iloc[:, 1].abs()
    theta = np.deg2rad(data.iloc[:, 2])

    # Set up the figure for the combined visualization
    fig = plt.figure(figsize=(12, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[2, 1])

    # Set up the polar plot
    ax1 = fig.add_subplot(gs[0], projection='polar')
    ax1.set_theta_zero_location('S')
    ax1.set_theta_direction(1)
    ax1.set_title("Polar Plot of Given Data (Clockwise Angle Increase)")
    line, = ax1.plot([], [], lw=2)

    # Set up the vertical bar
    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(.5, .55)
    ax2.set_ylim(0, max(positionValues) + 0.1 * max(positionValues))
    ax2.set_title("Position Visualization")

    # Hide the x-axis completely
    ax2.xaxis.set_visible(False)

    # Hide spines
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)

    # Set y-axis ticks
    ax2.set_yticks([0, 0.75, 1.5])

    rect = plt.Rectangle((0.5, 0), 0.5, 0, color='blue')
    ax2.add_patch(rect)

    # Animation function
    def animate(i):
        if i == 0:
            ax1.set_rlim(0, max(radius) + 0.1 * max(radius))
        else:
            line.set_data(theta[:i], radius[:i])
            ax1.set_rlim(0, max(radius[:i]) + 0.1 * max(radius[:i]))
        rect.set_height(positionValues[i])
        return line, rect

    # Create the animation
    ani = FuncAnimation(fig, animate, frames=len(theta), blit=False, repeat=False)
    writer = PillowWriter(fps=8)
    ani.save(output_path, writer=writer)
