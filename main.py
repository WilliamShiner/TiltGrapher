import os
import tkinter as tk
from tkinter import filedialog
from create_animation import *

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    # Allow selection of multiple CSV files
    inputFiles = filedialog.askopenfilenames(title="Select the CSV files",
                                              filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    # Create the output directory if it doesn't exist
    outputDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TiltGraph Output")
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    for input_file in inputFiles:
        # Extract the base name of the input file and construct the name for the output file
        baseName = os.path.splitext(os.path.basename(input_file))[0]
        outputFile = os.path.join(outputDir, "tiltgraph_" + baseName + ".gif")

        create_animation_from_csv(input_file, outputFile)
