import cv2
import numpy as np

# Global variables
points = [(41, 36), (510, 36), (508, 692), (32, 678)]  # Provided points


def correct_perspective(image, pts1):
    # Get the size of the original image
    h, w = image.shape[:2]

    # Define the size of the output image (same as the input image)
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])

    # Compute the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Apply the perspective warp with the original image size
    warped = cv2.warpPerspective(image, matrix, (w, h))

    return warped


def enhance_contrast(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization to enhance contrast
    equalized = cv2.equalizeHist(gray)
    return equalized


def detect_grid(image):
    # Apply GaussianBlur to smooth the image
    blurred = cv2.GaussianBlur(image, (3, 3), 0)

    # gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    gray = image

    # Edge detection using Canny with adjustable thresholds
    # edges = cv2.Canny(
    #     blurred, 30, 120, apertureSize=3
    # )  # Adjust thresholds if necessary
    adapt_th = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 20
    )
    adapt_th = cv2.bitwise_not(adapt_th)
    adapt_th = cv2.dilate(adapt_th, np.ones((2, 2), np.uint8), iterations=1)

    kernel = np.ones((18, 2), np.uint8)
    morph1 = cv2.morphologyEx(adapt_th, cv2.MORPH_OPEN, kernel)

    # Apply morphological operations to improve line detection
    #
    #   # Increase dilation iterations
    # eroded = cv2.erode(dilated, kernel, iterations=1)
    # eroded = cv2.Canny(eroded, 30, 120, apertureSize=3)

    # Line detection using Hough Line Transform with tuned parameters
    morph2 = morph1
    lines = cv2.HoughLinesP(
        morph1, 1.0, np.pi / 180, 50, minLineLength=0, maxLineGap=10
    )

    # Draw detected lines on the image
    grid_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(grid_image, (x1, y1), (x2, y2), (255, 255, 0), 2)  # Green lines

    return adapt_th, morph1, morph2, grid_image


# Load the image
img = cv2.imread("images/pierwsza.png")

# # Perspective correction using the provided points
# pts1 = np.float32(points)
# img = correct_perspective(img, pts1)

# # Enhance contrast
img = enhance_contrast(img)

# Grid detection on the perspective-corrected and contrast-enhanced image
edges_image, morph1_image, morph2_image, grid_image = detect_grid(img)

# Display images
cv2.imshow("Original Image", img)
# cv2.imshow("Warped Image", warped)
# cv2.imshow("Contrast Enhanced Image", enhanced_image)
cv2.imshow("Edges", edges_image)
# cv2.imshow("Eroded", eroded_image)
cv2.imshow("Morph1", morph1_image)
cv2.imshow("Morph2", morph2_image)
cv2.imshow("Detected Grid", grid_image)
cv2.imwrite("detected_grid.png", grid_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
