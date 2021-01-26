import cv2
import numpy as np

def vstack_images(image1,image2):
    return np.vstack((image1, image2))

def hstack_images(image1,image2):
    return np.hstack((image1, image2))


def vstack_array(images):
    stack = images[0]
    for image in images[1:]:
        stack = vstack_images(stack,image)
    return stack

def hstack_array(images):
    stack = images[0]
    for image in images[1:]:
        stack = hstack_images(stack,image)
    return stack