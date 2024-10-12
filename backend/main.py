import os
import re

import cv2
from processing.detection import find_grid, plot_circles, plot_rectangles, process_image

# RGB
for i, file in enumerate(os.listdir("./processing/.data/images")):
    img = cv2.imread(f"./processing/.data/images/{file}")
    rectangles = process_image(img)
    plot_rectangles(img, rectangles, f"./processing/.data/processed/{i}.jpg")
    plot_circles(img, rectangles, f"./processing/.data/processed/{i}_circles.jpg")

# img = cv2.imread("./processing/.data/images/IMG20240907191848.jpg")
# rectangles = process_image(img)
# plot_rectangles(img, rectangles, f"./processed.jpg")
# find_grid(img, rectangles)
