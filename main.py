import os
import tkinter as tk
from tkinter import filedialog
from create_animation import *

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
