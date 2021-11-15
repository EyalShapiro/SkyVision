from colorutils import convert
import cv2
from src.skyv_operator import *

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
        # ARITHMETIC
        operation("Bitwise And",OperationType.ARITHMETIC,bitwiseAnd).addInputText("Source 1").addInputText("Source 2").addInputText("Mask").addOutput(),
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
    return [operator.sources[operator.opOutputs[0]]]

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

def convertColor(inputs, operator):
    return [cv2.cvtColor(inputs["Source"],colorModes[inputs["Type"]])]

def colorMask(inputs, operator):
    return [cv2.inRange(inputs["Source"],np.array(inputs["Lower"]),np.array(inputs["Higher"]))]

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

def morphEX(inputs, operator):
    return [cv2.morphologyEx(inputs["Source"],morphModes[inputs["Mode"]],(int(inputs["Kernel"]),int(inputs["Kernel"])),iterations=int(inputs["Iterations"]))]


def gaussianBlur(inputs, _):
    return [cv2.GaussianBlur(inputs["Source"],(int(inputs["Kernel"]),int(inputs["Kernel"])),inputs["Iterations"])]

# ARITHMETIC
def bitwiseAnd(inputs,_):
    if(inputs["Mask"] != ""):
        return [cv2.bitwise_and(inputs["Source 1"],inputs["Source 2"],mask=inputs["Mask"])]
    return [cv2.bitwise_and(inputs["Source 1"],inputs["Source 2"])]