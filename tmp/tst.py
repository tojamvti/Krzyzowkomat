import cv2
import numpy as np

def correct_perspective(image):
    # Get the size of the original image
    h, w = image.shape[:2]
    
    # Define the coordinates of the points you want to use for perspective correction
    # Adjust these points based on your specific grid if necessary
    # Example points for a typical grid
    pts1 = np.float32([[45, 36], [511, 36], [508, 693], [30, 680]])
    
    # Define the size of the output image (same as the input image)
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    
    # Compute the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    
    # Apply the perspective warp with the original image size
    warped = cv2.warpPerspective(image, matrix, (w, h))
    
    return warped

def detect_grid(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to smooth the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Apply morphological operations to improve line detection
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # Line detection using Hough Line Transform
    lines = cv2.HoughLinesP(eroded, 1, np.pi / 180, 150, minLineLength=100, maxLineGap=10)

    # Draw detected lines on the image
    grid_image = np.copy(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(grid_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green lines

    return edges, grid_image

# Load the image
img = cv2.imread('images/pierwsza.png')

# Perspective correction to a bird's eye view while keeping the original size
warped = correct_perspective(img)

# Grid detection on the perspective-corrected image
edges_image, grid_image = detect_grid(warped)

# Display images
cv2.imshow("Original Image", img)
cv2.imshow("Warped Image", warped)
cv2.imshow("Edges", edges_image)
cv2.imshow("Detected Grid", grid_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
