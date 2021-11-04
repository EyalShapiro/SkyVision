from colorutils import convert
import cv2
from src.skyv_operator import operation, OperationType

def getOperations():
    return [
        operation("Webcam Input",OperationType.INPUT,camInput).addInputNumber("Id",step=1).addOutput(),
        operation("Image Input",OperationType.INPUT,imageInput).addInputText("Path").addOutput(),
        operation("Convert Color",OperationType.COLORS,convertColor).addInputText("Source").addInputRadio("Type",value="BGR2HSV",options=["BGR2HSV","BGR2RGB","BGR2GRAY","HSV2RGB","HSV2BGR","GRAY2RGB","GRAY2BGR",]).addOutput()
    ]

def convertColor(inputs,operator):
    modes = {
        "BGR2HSV":cv2.COLOR_BGR2HSV,
        "BGR2RGB":cv2.COLOR_BGR2RGB,
        "BGR2GRAY":cv2.COLOR_BGR2GRAY,
        "HSV2RGB":cv2.COLOR_HSV2RGB,
        "HSV2BGR":cv2.COLOR_HSV2BGR,
        "GRAY2RGB":cv2.COLOR_GRAY2RGB,
        "GRAY2BGR":cv2.COLOR_GRAY2BGR,}
    return [cv2.cvtColor(inputs["Source"],modes[inputs["Type"]])]

def camInput(inputs,operator):
    if operator.updating:
        operator.sources[operator.opOutputs[0]] = cv2.VideoCapture(int(inputs["Id"]))
    _, frame = operator.sources[operator.opOutputs[0]].read()
    return [frame]

def imageInput(inputs,operator):
    if operator.updating:
        operator.sources[operator.opOutputs[0]] = cv2.imread(inputs["Path"])
    return [operator.sources[operator.opOutputs[0]]]
