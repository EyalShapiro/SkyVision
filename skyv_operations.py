from colorutils import convert
import cv2
from src.skyv_operator import *
import random

def getOperations() -> list[operation]:
    return [
        # INPUT
        operation("Webcam Input",OperationType.INPUT,camInput).addInputNumber("Id",step=1).addOutput(),
        operation("Image Input",OperationType.INPUT,imageInput).addInputText("Path").addOutput(),
        # COLOR
        operation("Convert Color",OperationType.COLORS,convertColor).addInputText("Source").addInputRadio("Type",options=list(colorModes.keys())).addOutput(),
        operation("Color Mask",OperationType.COLORS,colorMask).addInputText("Source").addInputColor("Lower").addInputColor("Higher").addOutput(),
        # SHAPE
        operation("Gaussian Blur",OperationType.SHAPE,gaussianBlur).addInputText("Source").addInputNumber("Kernel",value=3,step=1).addInputNumber("Iterations",1,step=1).addOutput(),
        operation("MorphologyEx",OperationType.SHAPE,morphEX).addInputText("Source").addInputRadio("Mode",options=list(morphModes.keys())).addInputNumber("Kernel",value=3,step=1).addInputNumber("Iterations",value=1,step=1).addOutput(),
        operation("Find Contours",OperationType.SHAPE,findContours).addInputText("Source").addOutput(),
        operation("Largest Contour",OperationType.SHAPE,largestContour).addInputText("Contours").addOutput(),
        operation("Minimum Enclosing Circle",OperationType.SHAPE,minEnclosingCircle).addInputText("Contour").addOutput(),
        # ARITHMETIC
        operation("Bitwise And",OperationType.ARITHMETIC,bitwiseAnd).addInputText("Source 1").addInputText("Source 2").addInputText("Mask").addOutput(),
        # DRAW
        operation("Draw Contours",OperationType.DRAW,drawContours).addInputText("Source").addInputText("Contours").addInputColor("Color").addInputText("Thickness"),
        operation("Draw Circle",OperationType.DRAW,drawCircle).addInputText("Source").addInputText("X",value=0).addInputText("Y",value=0).addInputText("Radius",value=0).addInputText("Thickness").addInputColor("Color"),
        operation("Draw Rectangle",OperationType.DRAW,drawRect).addInputText("Source").addInputText("P1",value=(0,0)).addInputText("P2",value=(0,0)).addInputText("Thickness").addInputColor("Color"),
        # MISC
        operation("Flip",OperationType.MISC,flip).addInputText("Source").addInputRadio("Flip Mode",options=list({"Horizontal":1, "Vertical":0, "Horizontal and Vertical":-1})).addOutput(),
    ]

# INPUT
def camInput(inputs, operator):
    if operator.updating:
        operator.sources[operator.opOutputs[0]] = cv2.VideoCapture(int(inputs["Id"]))
    _, frame = operator.sources[operator.opOutputs[0]].read()
    if(frame is None): # input operations require specific error handling because of OpenCV behaviour
            raise Exception("Error reading frame from \"" + str(operator.opOutputs[0]) +"\".")
    return [frame]

def imageInput(inputs, operator):
    if operator.updating:
        operator.sources[operator.opOutputs[0]] = cv2.imread(inputs["Path"])
    if(operator.sources[operator.opOutputs[0]] is None):  # input operations require specific error handling because of OpenCV behaviour
        raise Exception("File \"" + inputs["Path"] + "\" Does not exist.")
    return [copy.deepcopy(operator.sources[operator.opOutputs[0]])]

# COLOR
colorModes = {
        "BGR2HSV":cv2.COLOR_BGR2HSV,
        "BGR2HLS":cv2.COLOR_BGR2HLS,
        "BGR2RGB":cv2.COLOR_BGR2RGB,
        "BGR2GRAY":cv2.COLOR_BGR2GRAY,
        "HSV2RGB":cv2.COLOR_HSV2RGB,
        "HSV2BGR":cv2.COLOR_HSV2BGR,
        "GRAY2RGB":cv2.COLOR_GRAY2RGB,
        "GRAY2BGR":cv2.COLOR_GRAY2BGR,}

def convertColor(inputs, _):
    if inputs["Source"] is not None:
        return [cv2.cvtColor(inputs["Source"],colorModes[inputs["Type"]])]
    return []

def colorMask(inputs, _):
    if inputs["Source"] is not None:
        return [cv2.inRange(inputs["Source"],np.array(inputs["Lower"]),np.array(inputs["Higher"]))]
    return []

# SHAPE
morphModes = {
        "CLOSE":cv2.MORPH_CLOSE,
        "OPEN":cv2.MORPH_OPEN,
        "BLACKHAT":cv2.MORPH_BLACKHAT,
        "TOPHAT":cv2.MORPH_TOPHAT,
        "RECT":cv2.MORPH_RECT,
        "CROSS":cv2.MORPH_CROSS,
        "ERODE":cv2.MORPH_ERODE,
        "DILATE":cv2.MORPH_DILATE,
        "GRADIENT":cv2.MORPH_GRADIENT,
        "HITMISS":cv2.MORPH_HITMISS,
        "ELLIPSE":cv2.MORPH_ELLIPSE,}

def findContours(inputs,_):
    if inputs["Source"] is not None:
        return [cv2.findContours(inputs["Source"], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)]
    return []

def morphEX(inputs, _):
    if inputs["Source"] is not None:
        return [cv2.morphologyEx(inputs["Source"],morphModes[inputs["Mode"]],(int(inputs["Kernel"]),int(inputs["Kernel"])),iterations=int(inputs["Iterations"]))]
    return []

def gaussianBlur(inputs, _):
    if inputs["Source"] is not None:
        return [cv2.GaussianBlur(inputs["Source"],(int(inputs["Kernel"]),int(inputs["Kernel"])),inputs["Iterations"])]
    return []

def largestContour(inputs,_):
    largest = inputs["Contours"][0]
    for cnt in inputs["Contours"][0]:
        if(cnt is not None):
            if(cv2.contourArea(cnt) > 5):
                largest = cnt
    if(largest is not None):
        return [[[largest]]]
    return []

def minEnclosingCircle(inputs,_):
    cnt = inputs["Contour"][0][0]
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    return [((x,y),radius)]

# ARITHMETIC
def bitwiseAnd(inputs,_):
    if inputs["Source1"] is not None and inputs["Source2"] is not None:
        if(inputs["Mask"] is not None):
            return [cv2.bitwise_and(inputs["Source 1"],inputs["Source 2"],mask=inputs["Mask"])]
        return [cv2.bitwise_and(inputs["Source 1"],inputs["Source 2"])]
    return []

# DRAW
def drawContours(inputs,_):
    if inputs["Source"] is not None and inputs["Contours"] is not None:
        clr = Color(hsv=(inputs["Color"][0]*2,inputs["Color"][1]/255,inputs["Color"][2]/255))
        bgr = (clr.rgb[2],clr.rgb[1],clr.rgb[0])
        if(len(inputs["Contours"][0]) > 0):
            time.sleep(1)
            return [cv2.drawContours(inputs["Source"], inputs["Contours"][0], -1, bgr, thickness=int(inputs["Thickness"]))]
    return []

def drawCircle(inputs,_):
    if inputs["Source"] is not None:
        clr = Color(hsv=(inputs["Color"][0]*2,inputs["Color"][1]/255,inputs["Color"][2]/255))
        return [cv2.circle(inputs["Source"], (int(inputs["X"]),int(inputs["Y"])),inputs["Radius"], (clr.rgb[2],clr.rgb[1],clr.rgb[0]), thickness=int(inputs["Thickness"]))]
    return []

def drawRect(inputs,_):
    if inputs["Source"] is not None:
        clr = Color(hsv=(inputs["Color"][0]*2,inputs["Color"][1]/255,inputs["Color"][2]/255))
        return [cv2.rectangle(inputs["Source"], (int(inputs["P1"][0]),int(inputs["P1"][1])),(int(inputs["P2"][0]),int(inputs["P2"][1])), (clr.rgb[2],clr.rgb[1],clr.rgb[0]), thickness=int(inputs["Thickness"]))]
    return []

# MISC
def flip(inputs,_):
    if(inputs["Source"] is not None):
        mode = {"Horizontal":1, "Vertical":0, "Horizontal and Vertical":-1}[inputs["Flip Mode"]]
        frame_flipped = cv2.flip(inputs["Source"], mode)
        return [frame_flipped]
    return []