import os
import sys
import cv2
import numpy as np

def get_bird_eye_view(image, output_size, points):
    height, width = output_size[1], output_size[0]
    scaled_points = [(int(p[0] * width / image.shape[1]), int(p[1] * height / image.shape[0])) for p in points]
    
    src_points = np.float32([scaled_points[0], scaled_points[1], scaled_points[3], scaled_points[2]])
    dst_points = np.float32([[0, height], [width, height], [0, 0], [width, 0]])
    
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    bird_eye_view = cv2.warpPerspective(image, matrix, output_size)
    return bird_eye_view

def get_points(image):
    points = []
    mask = None
    is_masking = False
    
    def mouse_callback(event, x, y, flags, param):
        nonlocal is_masking
        if event == cv2.EVENT_LBUTTONDOWN:
            if not is_masking:
                points.append((x, y))
                print((x, y))

    def update_mask(frame):
        mask.fill(0)
        polygon = np.array([points], np.int32)
        cv2.fillPoly(mask, polygon, (255, 255, 255))
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        external_mask = cv2.bitwise_not(mask)
        masked_frame[external_mask == 255] = [0, 0, 0]
        return masked_frame
    
    def resize_image(img, scale_percent):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    scale_percent = 50  
    resized_image = resize_image(image, scale_percent)
    cv2.namedWindow("Webcam")
    cv2.setMouseCallback("Webcam", mouse_callback)
    
    while True:
        key = cv2.waitKey(1)
        
        if key & 0xFF == ord('c'):
            points = []
            is_masking = False
            if mask is not None:
                mask.fill(0)
            print("\n")
                
        # 엔터 누르면 다각형대로 마스킹
        if key == 13 and not is_masking:
            is_masking = True
            mask = np.zeros(resized_image.shape[:2], dtype=np.uint8)
            update_mask(resized_image)
            print(f"points: {points}")
            
            # BEV 변환 수행
            bev = get_bird_eye_view(resized_image, (resized_image.shape[1], resized_image.shape[0]), points)
            cv2.imshow("Bird's Eye View", bev)
        
        if len(points) > 0 and not is_masking:
            polygon = np.array([points], np.int32)
            cv2.polylines(resized_image, polygon, True, (0, 255, 0), 2)
            for point in points:
                cv2.circle(resized_image, point, 5, (0, 255, 0), -1)

        if is_masking:
            masked_frame = update_mask(resized_image)
            cv2.imshow("Webcam", masked_frame)
        else:
            cv2.imshow("Webcam", resized_image)

        if key & 0xFF == ord('q'):
            print("\n다음 이미지")
            break
        
        # esc를 누르면 프로그램 종료
        if key == 27:
            print("\n프로그램 종료")
            sys.exit()

    cv2.destroyAllWindows()

def bev_main():
    dataset_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    image_path = os.path.join(dataset_directory, "steering_1.jpg")
    image = np.array(cv2.imread(image_path))
            
    get_points(image)

if __name__ == "__main__":
    bev_main()
