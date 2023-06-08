#https://github.com/devlucascfarias

import PySimpleGUI as sg
from math import sqrt
from skimage import io
from skimage.feature import blob_log
from skimage.color import rgb2gray

import matplotlib.pyplot as plt
from PIL import Image

# Window layout
layout = [
    [sg.Text('Select an image')],
    [sg.Input(key='filename'), sg.FileBrowse()],
    [sg.Button('To analyze!'), sg.Button('Cancel')]
]

# Create the window
window = sg.Window('Galaxy Detection', layout)

# Read the window events
while True:
    event, values = window.Read()
    if event == 'Cancel' or event == sg.WIN_CLOSED:
        break
    if event == 'To analyze!':
        # Load the selected image
        image = io.imread(values['filename'])
        gray_image = rgb2gray(image)

        # Adjust parameters for distant galaxy detection
        blob_logarithm = blob_log(gray_image, max_sigma=50, num_sigma=30, threshold=.05)

        # Calculate radii in the 3rd column
        blob_logarithm[:, 2] = blob_logarithm[:, 2] * sqrt(2)

        blob_list = [blob_logarithm]
        colors = ['yellow']
        titles = ['Laplacian of Gaussian']
        sequence = zip(blob_list, colors, titles)

        fig, axes = plt.subplots(1, 1, figsize=(10, 10))
        ax = axes

        for idx, (blobs, color, title) in enumerate(sequence):
            ax.set_title(title)
            ax.imshow(image)
            for blob in blobs:
                y, x, r = blob
                c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
                ax.add_patch(c)
            ax.set_axis_off()

        plt.tight_layout()
        fig.canvas.draw()

        # Convert the plot to a PIL image
        image_from_plot = Image.frombytes('RGB', fig.canvas.get_width_height(),
                                          fig.canvas.tostring_rgb())

        # Save the image
        image_from_plot.save('log/result.png')

        num_galaxies = len(blob_logarithm)
        print("Galaxies found:", num_galaxies)

        sg.popup(f"Number of galaxies detected: {num_galaxies}", title='Detection Result')

# Close the window
window.Close()
