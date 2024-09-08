import cv2
import numpy as np

from backend.processing.detection.base import Preprocessor


class CannyPreprocessor(Preprocessor):
    def __init__(self):
        pass

    def preprocess(self, image):
        canny = cv2.Canny(image, 230, 250)
        kernel = np.ones((3, 3), np.uint8)
        canny = cv2.dilate(canny, kernel, iterations=1)
        kernel = np.ones((2, 2), np.uint8)
        canny = cv2.erode(canny, kernel, iterations=1)
        return canny


class AdaptiveThresholdPreprocessor(Preprocessor):
    def __init__(self):
        pass

    def preprocess(self, image):
        pass


class LaplacianPreprocessor(Preprocessor):
    def __init__(self):
        pass

    def preprocess(self, image):
        pass


class SobelPreprocessor(Preprocessor):
    def __init__(self):
        pass

    def preprocess(self, image):
        pass
