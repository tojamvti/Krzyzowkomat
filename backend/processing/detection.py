import re
from sqlite3 import adapt

import cv2
import numpy as np
from matplotlib import pyplot as plt


def enhance_contrast(img):
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img


def detect_rectangles(img):
    contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    quadrilaterals_area = []

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.10 * perimeter, True)
        area = cv2.contourArea(approx)
        if len(approx) == 4 and area > 1000:
            quadrilaterals_area.append(area)

    median_area = np.median(quadrilaterals_area)

    rectangles = []

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.10 * perimeter, True)
        rectangle = cv2.minAreaRect(approx)
        area = rectangle[1][0] * rectangle[1][1]
        quadrilaterals_area = cv2.contourArea(approx)
        if (
            len(approx) == 4
            and area > median_area * 0.3
            and area < median_area * 3.0
            and quadrilaterals_area > median_area * 0.3
            and quadrilaterals_area < median_area * 2.0
        ):
            rectangles.append(rectangle)

    return rectangles


def plot_rectangles(img, rectangles, out="rectangles.jpg"):
    groups_img = np.zeros_like(img)
    for rectangle in rectangles:
        rand_color = (
            np.random.randint(100, 255),
            np.random.randint(100, 255),
            np.random.randint(100, 255),
        )

        box = cv2.boxPoints(rectangle)
        box = np.int32(box)
        cv2.drawContours(
            groups_img,
            [box],
            -1,
            rand_color,
            -1,
        )
    cv2.imwrite(out, groups_img)


def plot_circles(img, rectangles, filename="circles.jpg"):
    grid_img = np.copy(img)
    for rectangle in rectangles:
        cv2.circle(
            grid_img, (int(rectangle[0][0]), int(rectangle[0][1])), 5, (0, 0, 255), -1
        )

    cv2.imwrite(filename, grid_img)


def get_canny(img):
    canny = cv2.Canny(img, 300, 130)
    canny = cv2.GaussianBlur(canny, (3, 3), 0)
    # kernel = np.ones((3, 3), np.uint8)
    # canny = cv2.dilate(canny, kernel, iterations=1)
    # canny = cv2.GaussianBlur(canny, (3, 3), 0)
    # kernel = np.ones((3, 3), np.uint8)
    # canny = cv2.erode(canny, kernel, iterations=1)
    return canny


def get_adaptive_threshold(img):
    adapt_th = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, 4
    )
    adapt_th = cv2.bitwise_not(adapt_th)
    # kernel = np.ones((2, 2), np.uint8)
    # adapt_th = cv2.erode(adapt_th, kernel, iterations=1)
    return adapt_th


def merge_rectangles(rectangles):
    merged_rectangles = []

    for i, rectangle in enumerate(rectangles):
        new_rectange = True
        for j, merged_rectangle in enumerate(merged_rectangles):

            # TODO change to overlap criterion and select the one with the highest area or merge them
            dist = np.linalg.norm(
                (np.array(rectangle[0]) - np.array(merged_rectangle[0]))
            )

            if dist < 15:
                old_area = merged_rectangle[1][0] * merged_rectangle[1][1]
                new_area = rectangle[1][0] * rectangle[1][1]
                if new_area > old_area:
                    merged_rectangles[j] = rectangle
                new_rectange = False
                break
        if new_rectange:
            merged_rectangles.append(rectangle)

    return merged_rectangles


def remove_small_rectangles(rectangles):
    median_area = np.median(
        [rectangle[1][0] * rectangle[1][1] for rectangle in rectangles]
    )
    new_rectangles = []
    for rectangle in rectangles:
        area = rectangle[1][0] * rectangle[1][1]
        if area > median_area * 0.65:
            new_rectangles.append(rectangle)

    return new_rectangles


def find_grid(img, rectangles):
    # TODO: Implement this function
    grid_img = np.zeros_like(img)
    for rectangle in rectangles:
        rectangle = list(rectangle)
        rectangle[2] = 0.0
        box = cv2.boxPoints(rectangle)
        box = np.int32(box)
        cv2.drawContours(grid_img, [box], -1, (0, 0, 255), 2)

    cv2.imwrite("grid.jpg", grid_img)


def remove_rotation(rectangles):
    for i in range(len(rectangles)):
        rectangle = rectangles[i]
        rectangle = list(rectangle)
        rectangle[2] = 0.0
        rectangles[i] = rectangle

    return rectangles


def correct_perspective(image, pts1):
    # TODO: Use in the code
    h, w = image.shape[:2]

    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    warped = cv2.warpPerspective(image, matrix, (w, h))

    return warped


def process_image(img: np.array):
    # img = enhance_contrast(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)

    adapt_th = get_adaptive_threshold(gray)
    canny = get_canny(img)

    rectangles_adapt_th = detect_rectangles(adapt_th)
    rectangles_canny = detect_rectangles(canny)

    rectangles = []
    rectangles.extend(rectangles_adapt_th)
    rectangles.extend(rectangles_canny)

    rectangles = merge_rectangles(rectangles)

    rectangles = remove_small_rectangles(rectangles)

    # rectangles = remove_rotation(rectangles)

    return rectangles
