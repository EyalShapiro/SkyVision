import cv2
import numpy as np
import math

EXIT_KEY = 'q'
ERROR = 0.1
AREA_RATIO = 0.15

config = {
    "hl": 30,
    "sl": 0,
    "vl": 215,
    "hh": 100,
    "sh": 255,
    "vh": 255,
    "morph_s": 4,
    "morph_op": 3,
    "morph_it": 2,
}

EXPOSURE = -7


def set_slider_val(key, value):
    config[key] = value


def create_sliders():
    cv2.namedWindow('Color')
    cv2.createTrackbar('hl', 'Color', config["hl"], 180,
                       lambda val: set_slider_val("hl", val))
    cv2.createTrackbar('sl', 'Color', config["sl"], 255,
                       lambda val: set_slider_val("sl", val))
    cv2.createTrackbar('vl', 'Color', config["vl"], 255,
                       lambda val: set_slider_val("vl", val))
    cv2.createTrackbar('hh', 'Color', config["hh"], 255,
                       lambda val: set_slider_val("hh", val))
    cv2.createTrackbar('sh', 'Color', config["sh"], 255,
                       lambda val: set_slider_val("sh", val))
    cv2.createTrackbar('vh', 'Color', config["vh"], 255,
                       lambda val: set_slider_val("vh", val))

    cv2.namedWindow('Morph')
    cv2.createTrackbar('kernel size', 'Morph', config["morph_s"], 20,
                       lambda val: set_slider_val("morph_s", val))
    cv2.createTrackbar('operation', 'Morph', config["morph_op"], 4,
                       lambda val: set_slider_val("morph_op", val))
    cv2.createTrackbar('iterations', 'Morph', config["morph_it"], 10,
                       lambda val: set_slider_val("morph_it", val))


def image_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, np.array([config['hl'], config['sl'], config['vl']]), np.array(
        [config['hh'], config['sh'], config['vh']]))

    if min(config["morph_s"], config["morph_op"], config["morph_it"]) > 0:
        ker = cv2.getStructuringElement(
            cv2.MORPH_RECT, (config["morph_s"], config["morph_s"]))

        if config["morph_op"] == 1:
            mask = cv2.erode(mask, ker, iterations=config["morph_it"])
        elif config["morph_op"] == 2:
            mask = cv2.dilate(mask, ker, iterations=config["morph_it"])
        elif config["morph_op"] == 3:
            mask = cv2.morphologyEx(
                mask, cv2.MORPH_OPEN, ker, iterations=config["morph_it"])
        elif config["morph_op"] == 4:
            mask = cv2.morphologyEx(
                mask, cv2.MORPH_CLOSE, ker, iterations=config["morph_it"])

    return mask


def find_target(mask):
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return []

    target = contours[0]
    target_area = 0

    # Area approximation would not work for steep angles, BAD!
    # Maybe use a smarter area approx (shape area relative to bounding rect area?)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if abs(cv2.contourArea(contour) / area - AREA_RATIO) <= ERROR and area > target_area: # Find largest contour that fits area ratio
            target = contour
            target_area = area

    print(abs(cv2.contourArea(target) / area - AREA_RATIO))
    return [target]


def main():
    create_sliders()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

    while cap.isOpened() and cv2.waitKey(1) != ord(EXIT_KEY):
        _, frame = cap.read()

        mask = image_mask(frame)

        filtered = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('filter', filtered)

        target = find_target(mask)
        for contour in target:
            cv2.drawContours(frame, [contour], 0, (255, 0, 0), 10)
            x, y, w, h = cv2.boundingRect(contour)
            cx = x + int(w / 2)
            cy = y + int(h / 2)
            cv2.line(frame, (cx, 0), (cx, int(height)), (255, 255, 255), 1)
            cv2.putText(frame, str(cv2.contourArea(contour) /
                        (w*h)), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))

        cv2.imshow('frame', frame)


if __name__ == "__main__":
    main()
