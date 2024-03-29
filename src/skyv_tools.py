import numpy as np
from colorutils import Color
from datetime import datetime
import warnings
import functools
import colorsys
from PIL import ImageColor
import cv2

def rgb_to_hls(rgb):
    r, g, b = rgb
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (round(h*360), round(l/255*100),round(s*-100))
    
def hex_to_hsv(hex):  # turn hex to hsv
    try:
        c = Color(hex=hex)
        return (round(c.hsv[0]/2),round(c.hsv[1]*255),round(c.hsv[2]*255))
    except:
        return (0,0,0)

def hex_to_hls(hex):  # turn hex to hls
    c = Color(hex=hex)
    return rgb_to_hls(c.rgb)

def hex_to_rgb(hex):  # turn hex to rgb
    c = Color(hex=hex)
    return c.rgb

def hex_to_bgr(hex):  # turn hex to bgr
    c = Color(hex=hex)
    rgb = c.rgb
    bgr = (rgb[2], rgb[1], rgb[0])
    return bgr

def vstack_images(image1, image2):  # put image on top on another image
    return np.vstack((image1, image2))

def hstack_images(image1, image2):  # put image right of another image
    return np.hstack((image1, image2))

def vstack_array(images):  # put all images in array on top of each other
    stack = images[0]
    for image in images[1:]:
        stack = vstack_images(stack, image)
    return stack

def hstack_array(images):  # put all images to the right of each other
    stack = images[0]
    for image in images[1:]:
        stack = hstack_images(stack, image)
    return stack

class tColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getTime():
    return "[" + str(datetime.now().strftime("%H:%M:%S")) + "] "

def logMessage(msg):
    print(tColors.OKCYAN + getTime() + str(msg) + tColors.ENDC)

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func