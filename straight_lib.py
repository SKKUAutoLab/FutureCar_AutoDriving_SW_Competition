import os
import sys
import cv2
import numpy as np
           
def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def hough_transform(image, polygon):
    resized_image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    # Hough 변환을 사용하여 직선을 검출
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    
    # 검출된 직선을 이미지에 그림
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(resized_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
          
    return resized_image

def hough_main():
    dataset_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    image_files = ["steering_4.jpg"]
    polygon = [(12, 718), (718, 705), (582, 389), (103, 414)]

    for image_file in image_files:
        image_path = os.path.join(dataset_directory, image_file)
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Error: Could not open or find the image {image_file}.")
            continue

        result_image = hough_transform(image, polygon)

        cv2.imshow("Detected Lines - " + image_file, result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    hough_main()
