import cv2
import numpy as np

from backend.processing.detection.base import SquaresDetector


class BasicSquaresDetector(SquaresDetector):
    def __init__(self):
        pass

    def detect(self, image):
        contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        pre_rectangles = []

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.10 * perimeter, True)
            if len(approx) == 4 and cv2.contourArea(approx) > 500:
                pre_rectangles.append(approx)

        median_area = np.median(
            [cv2.contourArea(rectangle) for rectangle in pre_rectangles]
        )

        rectangles = []

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.10 * perimeter, True)
            if (
                len(approx) == 4
                and cv2.contourArea(approx) > median_area * 0.5
                and cv2.contourArea(approx) < median_area * 2.0
            ):
                rectangles.append(approx)

        return rectangles
