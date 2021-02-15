import cv2
import numpy as np
from colorutils import Color

def hex_to_hsv(hex): # turn hex to hsv
    c = Color(hex=hex)
    return c.hsv

def hex_to_rgb(hex): # turn hex to hsv
    c = Color(hex=hex)
    return c.rgb

def vstack_images(image1,image2): # put image on top on another image
    return np.vstack((image1, image2))

def hstack_images(image1,image2): # put image right of another image
    return np.hstack((image1, image2))


def vstack_array(images): # put all images in array on top of each other
    stack = images[0]
    for image in images[1:]:
        stack = vstack_images(stack,image)
    return stack

def hstack_array(images): # put all images to the right of each other
    stack = images[0]
    for image in images[1:]:
        stack = hstack_images(stack,image)
    return stack