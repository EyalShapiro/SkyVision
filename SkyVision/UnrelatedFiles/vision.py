import cv2
import numpy as np
import time
import math

DEG2RAD = math.pi/180

# H_FOV = 63.2150044
H_FOV = 68.5
EXPOSURE = -7

# RANDOM VALUES, PLEASE CHANGE!
CAMERA_ANGLE = 40.8
# Camera to bottom of vision target
HEIGHT_DELTA = 54.25
VISION_TARGET_HEIGHT = 17
# END OF RANDOM VALUES

EXIT_KEY = 'q'

ERROR = 0.15
AREA_RATIO = 0.15

HSV_LOW = np.array([61, 60, 60])
HSV_HIGH = np.array([93, 255, 255])

KERNEL_SIZE = (4, 4)
OPERATION = cv2.MORPH_OPEN
ITERATIONS = 2


def image_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, HSV_LOW, HSV_HIGH)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, KERNEL_SIZE)
    mask = cv2.morphologyEx(mask, OPERATION, kernel, iterations=ITERATIONS)
    return mask


def find_target(mask):
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    target = None
    target_rect = None
    target_area = 0

    for contour in contours:
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        area = w * h
        # Find largest contour that fits area ratio
        if abs(cv2.contourArea(contour) / area - AREA_RATIO) <= ERROR and area > target_area:
            target = contour
            target_rect = rect
            target_area = area

    return [target, target_rect]


def find_angle(cx, s_width, pixel_angle):
    return (cx - s_width / 2) * pixel_angle


def find_dist_1(y, h, s_height, pixel_angle):
    angle_to_bottom = (y + h - s_height / 2) * pixel_angle
    overall_angle = (CAMERA_ANGLE - angle_to_bottom) * DEG2RAD
    print(1, angle_to_bottom)
    return HEIGHT_DELTA / math.tan(overall_angle)


def find_dist_2(y, h, s_height, pixel_angle):
    angle_to_top = (y - s_height / 2) * pixel_angle
    overall_angle = (CAMERA_ANGLE - angle_to_top) * DEG2RAD
    # print(2, overall_angle)
    return (HEIGHT_DELTA + VISION_TARGET_HEIGHT) / math.tan(overall_angle)


def main():
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    s_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
    s_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

    pixel_angle = H_FOV / s_width

    while cap.isOpened() and cv2.waitKey(1) != ord(EXIT_KEY):
        start_time = time.time()
        _, frame = cap.read()
        mask = image_mask(frame)
        # filtered = cv2.bitwise_and(frame, frame, mask=mask)
        # cv2.imshow('filter', filtered)

        target, target_rect = find_target(mask)
        if target is not None:
            cv2.drawContours(frame, [target], 0, (255, 0, 0), 5)
            x, y, w, h = target_rect
            cx = x + int(w / 2)
            cy = y + int(h / 2)
            cv2.line(frame, (cx, cy), (int(s_width / 2), cy),
                     (255, 255, 255), 1)
            cv2.line(frame, (cx, y), (cx, 0), (255, 255, 255), 1)
            cv2.putText(frame, "%.2fdeg" % find_angle(cx, s_width, pixel_angle),
                        (cx, cy - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))

            print()
            cv2.putText(frame, "%.2fin" % find_dist_1(y, h, s_height, pixel_angle),
                        (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
            cv2.putText(frame, "%.2fin" % find_dist_2(y, h, s_height, pixel_angle),
                        (200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))

        # cv2.putText(frame, "%d" % (1 / (time.time() - start_time)),
        #             (0, int(s_height)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0))

        cv2.imshow('frame', frame)


if __name__ == "__main__":
    main()
