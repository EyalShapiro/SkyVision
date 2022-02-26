from colorutils import convert
import cv2
from src.skyv_operator import *
import random

def getOperations():
    return [
        # INPUT
        operation("Webcam Input",OperationType.INPUT,camInput).addInputNumber("Id",step=1).addOutput(),
        operation("Image Input",OperationType.INPUT,imageInput).addInputText("Path").addOutput(),
        
        # COLOR
        operation("Convert Color",OperationType.COLORS,convertColor).addInputText("Source").addInputRadio("Type",options=list(colorModes.keys())).addOutput(),
        operation("Color Mask",OperationType.COLORS,colorMask).addInputText("Source").addInputColor("Lower").addInputColor("Higher").addOutput(),
        operation("Color Mask From String", OperationType.COLORS, colorMaskString).addInputText("Source").addInputText("Lower").addInputText("Higher").addOutput(),
        operation("Canny",OperationType.COLORS,canny).addInputText("Source").addInputNumber("Threshold 1").addInputNumber("Threshold 2").addOutput("Output"),
        

        # SHAPE
        operation("Gaussian Blur",OperationType.SHAPE,gaussianBlur).addInputText("Source").addInputNumber("Kernel",value=3,step=1).addInputNumber("Iterations",1,step=1).addOutput(),
        operation("MorphologyEx",OperationType.SHAPE,morphEX).addInputText("Source").addInputRadio("Mode",options=list(morphModes.keys())).addInputNumber("Kernel",value=3,step=1).addInputNumber("Iterations",value=1,step=1).addOutput(),
        operation("Find Contours",OperationType.SHAPE,findContours).addInputText("Source").addOutput(),
        operation("Largest Contour",OperationType.SHAPE,largestContour).addInputText("Contours").addOutput(),
        operation("Minimum Enclosing Circle",OperationType.SHAPE,minEnclosingCircle).addInputText("Contour").addOutput(),
        operation("Convex Hull",OperationType.SHAPE,cvxHull).addInputText("Contour").addOutput(),
        operation("Rotated Rectangle",OperationType.SHAPE,rotatedRectangle).addInputText("Contours").addOutput(),
        operation("Fit Ellipse",OperationType.SHAPE,fitEllipse).addInputText("Source").addOutput(),
        operation("Bounding Rectangle",OperationType.SHAPE,boundingRectangle).addInputText("Source").addOutput("X").addOutput("Y").addOutput("W").addOutput("H"),

        # ARITHMETIC
        operation("Bitwise And",OperationType.ARITHMETIC,bitwiseAnd).addInputText("Source 1").addInputText("Source 2").addInputText("Mask").addOutput(),
        operation("Circle Coords",OperationType.ARITHMETIC,circleCoords).addInputText("Circle").addInputText("Frame").addInputText("Focal Length",value=str(10)).addInputText("Dot Pitch",value=str(9.84375)).addOutput("Out Angle").addInputText("Pixel Radius at meter").addOutput("Out Distance"),
        operation("ApproxPolyDP",OperationType.ARITHMETIC,approxPolyDP).addInputText("Contours").addInputText("Sides").addInputText("Tolerance").addOutput(),
        operation("Split Channel",OperationType.ARITHMETIC,splitChannel).addInputText("Source").addInputNumber("Select Channel").addOutput("Output"),
        operation("Ratio",OperationType.ARITHMETIC,ratio).addInputText("Contours").addInputNumber("Width").addInputNumber("Height").addInputNumber("Threshold").addOutput("Output"),

        # DRAW
        operation("Draw Contours",OperationType.DRAW,drawContours).addInputText("Source").addInputText("Contours").addInputColor("Color").addInputText("Thickness"),
        operation("Draw Circle",OperationType.DRAW,drawCircle).addInputText("Source").addInputText("Position",value=0).addInputText("Radius",value=0).addInputText("Thickness").addInputColor("Color"),
        operation("Draw Rectangle",OperationType.DRAW,drawRect).addInputText("Source").addInputText("P1",value=(0,0)).addInputText("P2",value=(0,0)).addInputText("Thickness").addInputColor("Color"),
        operation("Draw Ellipse",OperationType.DRAW,drawEllipse).addInputText("Source").addInputText("Ellipse").addInputColor("Color").addInputNumber("Thickness"),

        # MISC
        operation("Flip",OperationType.MISC,flip).addInputText("Source").addInputRadio("Flip Mode",options=list({"Horizontal":1, "Vertical":0, "Horizontal and Vertical":-1})).addOutput(),
        operation("NetworkTable Send Num",OperationType.MISC,ntSendNum).addInputText("Key").addInputText("Value"),
        operation("NetworkTable Get Num",OperationType.MISC,ntGetNum).addInputText("Key").addInputText("Store Variable"),
        operation("Network Send Num Var",OperationType.MISC,ntSendNumVar).addInputText("Key").addInputText("Number Variable"),
        operation("Print",OperationType.MISC,webPrint).addInputText("Value"),
        operation("Blank Image",OperationType.MISC,blankImg).addInputText("Source").addOutput(),
        operation("Minimum Contour Area",OperationType.MISC,minContourArea).addInputText("Source").addInputNumber("Area").addOutput("Output"),
        operation("Hough Circles",OperationType.MISC,houghCircles).addInputText("Source").addInputNumber("dp").addInputNumber("minDist").addInputNumber("Higher Threshold").addInputNumber("Accumulator Threshold").addInputNumber("Minimum Radius").addInputNumber("Maximum Radius").addOutput("Output"),
        operation("Covex Hull",OperationType.MISC,covexHull).addInputText("Contours").addOutput("Output"),
        operation("Circle Coords",OperationType.MISC,circleCoords).addInputText("Circles").addInputText("Size at 1 meter").addOutput("Output"),

        # Flow Control
        operation("IF", OperationType.FlowControl, IF).addInputText("Condition"),
        operation("ENDIF", OperationType.FlowControl, ENDIF),


    ]

# INPUT
cam = cv2.VideoCapture(0)
def camInput(inputs, operator):
    global cam
    if operator.updating:
        time.sleep(0.5)
    ret, frame = cam.read()
    if(not ret): # input operations require specific error handling because of OpenCV behaviour
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

def colorMaskString(inputs, _):
    if inputs["Source"] is not None:
        return [cv2.inRange(inputs["Source"],np.array(inputs["Lower"]),np.array(inputs["Higher"]))]
    return []

# TODO: implement
def canny(inputs,_):
    pass

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
        cnts, _ = cv2.findContours(inputs["Source"], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return [cnts]
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
    if(inputs["Contours"] is not None):
        return [max(inputs["Contours"], key = cv2.contourArea)]
    return []

def minEnclosingCircle(inputs,_):
    if inputs["Contour"] is not None:
        cnt = inputs["Contour"]
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        return [((x,y),radius)]
    return []

def cvxHull(inputs,_):
    if inputs["Contour"] is not None:
        cnt = inputs["Contour"]
        return [cv2.convexHull(cnt)]
    return []

# TODO: implement
def rotatedRectangle(inputs,_):
    pass

# TODO: implement
def fitEllipse(inputs,_):
    pass

# TODO: implement
def boundingRectangle(inputs,_):
    pass

# ARITHMETIC
def bitwiseAnd(inputs,_):
    if inputs["Source 1"] is not None and inputs["Source 2"] is not None:
        if(inputs["Mask"] is not None):
            return [cv2.bitwise_and(inputs["Source 1"],inputs["Source 2"],mask=inputs["Mask"])]
        return [cv2.bitwise_and(inputs["Source 1"],inputs["Source 2"])]
    return []

def circleCoords(inputs,_):
    circle = inputs["Circle"]
    onemeter = inputs["Pixel Radius at meter"]
    if circle is not None:
        distance = onemeter / circle[1]
        Resolution = (inputs["Frame"].shape[1],inputs["Frame"].shape[0])
        F_Length = inputs["Focal Length"]
        Dot_Pitch = inputs["Dot Pitch"]

        S_Width = Dot_Pitch * Resolution[1]  # in um
        S_Width = S_Width / 1000  # in mm
        F_Pix = (Resolution[0] / 2 / S_Width) * F_Length
        Kval = np.array([[F_Pix, 0, Resolution[0] / 2], [0, F_Pix, Resolution[1] / 2],[0, 0, 1]])  # pinhole camera matrix
        final_angle = np.degrees(RaysToAngle(FrameToWorldRay(circle[0][0], Resolution[1] / 2,Kval),FrameToWorldRay(Resolution[0] / 2, Resolution[1] / 2,Kval)))
        dir = 1 if(circle[0][0] > Resolution[0] / 2) else -1
        final_angle = dir * (final_angle) + 90
        return[final_angle,distance]

def approxPolyDP(inputs,_):
    contours = inputs["Contours"]
    sides = inputs["Sides"]
    tolerance = inputs["Tolerance"]
    contour_list = []
    for contour in contours[0]:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        if sides - tolerance <= len(approx) <= sides + tolerance:
            contour_list.append(contour)
    return [[contour_list,contours[1]]]

# TODO: implement
def splitChannel(inputs,_):
    pass

# TODO: implement
def ratio(inputs,_):
    pass

# DRAW
def drawContours(inputs,_):
    if inputs["Source"] is not None and inputs["Contours"] is not None:
        clr = Color(hsv=(inputs["Color"][0]*2,inputs["Color"][1]/255,inputs["Color"][2]/255))
        bgr = (clr.rgb[2],clr.rgb[1],clr.rgb[0])
        if(len(inputs["Contours"]) > 0):
            return [cv2.drawContours(inputs["Source"], inputs["Contours"], -1, bgr, thickness=int(inputs["Thickness"]))]
    return []

def drawCircle(inputs,_):
    if inputs["Source"] is not None:
        clr = Color(hsv=(inputs["Color"][0]*2,inputs["Color"][1]/255,inputs["Color"][2]/255))
        return [cv2.circle(inputs["Source"], (int(inputs["Position"][0]),int(inputs["Position"][1])),int(inputs["Radius"]), (clr.rgb[2],clr.rgb[1],clr.rgb[0]), thickness=int(inputs["Thickness"]))]
    return []

def drawRect(inputs,_):
    if inputs["Source"] is not None:
        clr = Color(hsv=(inputs["Color"][0]*2,inputs["Color"][1]/255,inputs["Color"][2]/255))
        return [cv2.rectangle(inputs["Source"], (int(inputs["P1"][0]),int(inputs["P1"][1])),(int(inputs["P2"][0]),int(inputs["P2"][1])), (clr.rgb[2],clr.rgb[1],clr.rgb[0]), thickness=int(inputs["Thickness"]))]
    return []

# TODO: implement
def drawEllipse(inputs,_):
    pass

# MISC
def flip(inputs,_):
    if(inputs["Source"] is not None):
        mode = {"Horizontal":1, "Vertical":0, "Horizontal and Vertical":-1}[inputs["Flip Mode"]]
        frame_flipped = cv2.flip(inputs["Source"], mode)
        return [frame_flipped]
    return []

def ntSendNum(inputs,_):
    if(inputs["Key"] is not None):
        skyv_network.set_number(inputs["Key"],float(inputs["Value"]))

# TODO: immplement
def ntSendNumVar(inputs,_):
    pass

def ntGetNum(inputs,_):
    if(inputs["Key"] is not None):
        return [skyv_network.get_number(inputs["Key"], -1)]

def webPrint(inputs,_):
    if(inputs["Value"] is not None):
        logMessage("USER PRINT - " + str(inputs["Value"]))

# TODO: implement
def blankImg(inputs,_):
    if(inputs["Source"] is not None):
        return [np.zeros(inputs["Source"].shape, np.uint8)]
    return []

# TODO: implement
def minContourArea(inputs,_):
    pass

# TODO: implement
def houghCircles(inputs,_):
    pass

# TODO: implement
def covexHull(inputs,_):
    pass

# TODO: implement
def circleCoords(inputs,_):
    pass

# Flow Control
def IF(inputs,_):
    return [inputs["Condition"]]

def ENDIF(inputs,_):
    pass

 
# HELP
def FrameToWorldRay(Fx, Fy,K):
    Ki = np.linalg.inv(K)
    r = Ki.dot([Fx, Fy, 1])
    return r  # a "ray" in the sense that all the 3D points R = s * r, obtained by multiplying it for an arbitrary number s, will lie on the same line going through the camera center and pixel (x, y).

def RaysToAngle(R1,
                R2):  # calculate the angle between two rays using advanced math none of us understand. It is theoretically possible to find the 3D coords of a point and use simple trigonometry, but this looks nicer.
    cos_angle = R1.dot(R2) / (np.linalg.norm(R1) * np.linalg.norm(R2))
    angle_radians = np.arccos(cos_angle)
    return angle_radians

    