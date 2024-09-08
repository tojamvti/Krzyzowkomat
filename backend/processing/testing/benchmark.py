import os

import cv2

from backend.processing.detection.pipeline import ImagePipeline
from backend.processing.testing.utils import get_data_files


def run():
    path = "./processing/.data/images"
    if not os.path.exists(path):
        raise FileNotFoundError("Data not found")

    files = [f for f in os.listdir(path) if f.endswith(".jpg")]

    pipeline = ImagePipeline()

    for file in files:
        image = cv2.imread(file)
        pipeline.process(image)


if __name__ == "__main__":
    run()
