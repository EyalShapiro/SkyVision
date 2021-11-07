from src.skyv_inputs import *
from src.skyv_tools import *
from flask import *
import cv2
import numpy as np
import math
import copy
import time
from enum import Enum
from collections.abc import Callable

import src.skyv_network as skyv_network

error_pic = cv2.imread("res/images/ERR.jpg")  # The frame that will be used for drawing when there is an error

"""sky_operations = {  # sky operation is a dictionary that defines the inputs each operation has

    # EXAMPLE ->
    # Key : operation("operation name",OperationType,
    #   text_inputs=[operation_TextInput("html Name", " html Text")],
    #   number_inputs=[operation_NumberInput("html Name", "html Text")])
    "Image Input": operation("Image input", OperationType.INPUT,
                             text_inputs=[operation_TextInput("imgPath", "Image Path")],
                             variable_outputs=[operation_TextInput("outName", "Output name")]),

    "Webcam Input": operation("Webcam input", OperationType.INPUT,
                              number_inputs=[operation_NumberInput("webcamID", "Webcam ID")],
                              variable_outputs=[operation_TextInput("outName", "Output name")]),

    "IP Input": operation("IP input [DEPRECATED]", OperationType.INPUT,
                          text_inputs=[operation_TextInput("webcamID", "Webcam ID")],
                          variable_outputs=[operation_TextInput("outName", "Output name")]),

    "Color Mask": operation("Color Mask", OperationType.COLORS,
                            text_inputs=[
                                operation_TextInput("src", "Source")],
                            color_inputs=[
                                operation_ColorInput("lower", "Lower"),
                                operation_ColorInput("higher", "Higher")],
                            variable_outputs=[
                                operation_TextInput("outName", "Output name")]
                            ),

    "Convert Color": operation("Convert color", OperationType.COLORS,
                               text_inputs=[
                                   operation_TextInput("src", "Source")],
                               radio_inputs=[
                                   operation_RadioInput("type", "Type",
                                                        options=[
                                                            "BGR2HSV",
                                                            "BGR2RGB",
                                                            "BGR2GRAY",
                                                            "HSV2RGB",
                                                            "HSV2BGR",
                                                            "GRAY2RGB",
                                                        ])],
                               variable_outputs=[operation_TextInput("outName", "Output name")]
                               ),

    "Gaussian Blur": operation("Gaussian Blur", OperationType.MORPH,
                               text_inputs=[
                                   operation_TextInput("src", "Source")],
                               number_inputs=[
                                   operation_NumberInput("kernel", "Kernel Value"),
                                   operation_NumberInput("iter", "Iterations")
                               ],
                               variable_outputs=[operation_TextInput("outName", "Output name")]
                               ),

    "MorphEx": operation("MorphEx", OperationType.MORPH,
                         text_inputs=[
                             operation_TextInput("src", "Source")],
                         number_inputs=[
                             operation_NumberInput("kernel", "Kernel"),
                             operation_NumberInput("itr", "Iterations")],
                         radio_inputs=[
                             operation_RadioInput("type", "Type",
                                                  options=[
                                                      "Erosion",
                                                      "Dilation",
                                                      "Opening",
                                                      "Closing",
                                                  ])],
                         variable_outputs=[operation_TextInput("outName", "Output name")]
                         ),

    "Bitwise And": operation("Bitwise AND", OperationType.ARITHMETIC,
                             text_inputs=[
                                 operation_TextInput("src1", "Source 1"),
                                 operation_TextInput("src2", "Source 2"),
                                 operation_TextInput("mask", "Mask"),
                             ],
                             variable_outputs=[operation_TextInput("outName", "Output name")]
                             ),

    "Find Contours": operation("Find Contours", OperationType.COLORS,
                               text_inputs=[
                                   operation_TextInput("src", "Source"),
                               ]
                               , variable_outputs=[operation_TextInput("outName", "Output name")]
                               ),

    "Draw Contours": operation("Draw Contours", OperationType.DRAW,
                               text_inputs=[
                                   operation_TextInput("src", "Source"),
                                   operation_TextInput("cnt", "Contours"),
                               ],
                               number_inputs=[
                                   operation_NumberInput("thick", "Thickness"),
                               ],
                               color_inputs=[
                                   operation_ColorInput("clr", "Color"), ]
                               ),

    "Draw Contour": operation("Draw Contour", OperationType.DRAW,
                              text_inputs=[
                                  operation_TextInput("src", "Source"),
                                  operation_TextInput("cnt", "Contours"),
                              ],
                              number_inputs=[
                                  operation_NumberInput("thick", "Thickness"),
                              ],
                              color_inputs=[
                                  operation_ColorInput("clr", "Color"), ]
                              ),

    "Draw Circle": operation("Draw Circle", OperationType.DRAW,
                             text_inputs=[
                                 operation_TextInput("src", "Source"),
                             ],
                             number_inputs=[
                                 operation_NumberInput("radius", "Radius"),
                                 operation_NumberInput("xValue", "X", "padding-right:5px", brake=False),
                                 operation_NumberInput("yValue", "Y"),
                                 operation_NumberInput("thickness", "Thickness")
                             ],
                             color_inputs=[
                                 operation_ColorInput("Color", "Color")
                             ]
                             ),

    "Draw Circle Params": operation("Draw Circle Params", OperationType.DRAW,
                                    text_inputs=[
                                        operation_TextInput("src", "Source"),
                                        operation_TextInput("radius", "Radius"),
                                        operation_TextInput("xValue", "X", "padding-right:5px", brake=False),
                                        operation_TextInput("yValue", "Y"),
                                    ],
                                    number_inputs=[
                                        operation_TextInput("thickness", "Thickness")
                                    ],
                                    color_inputs=[
                                        operation_ColorInput("Color", "Color")
                                    ]
                                    ),

    "Draw Rectangle Params": operation("Draw Rectangle Params", OperationType.DRAW,
                                       text_inputs=[
                                           operation_TextInput("src", "Source"),
                                           operation_TextInput("wth", "Width"),
                                           operation_TextInput("hght", "Height"),
                                           operation_TextInput("xValue", "X",
                                                               "padding-right:5px;color: #ebebeb;background-color:#525252;",
                                                               brake=False),
                                           operation_TextInput("yValue", "Y"),
                                       ],
                                       number_inputs=[
                                           operation_TextInput("thickness", "Thickness")
                                       ],
                                       color_inputs=[
                                           operation_ColorInput("Color", "Color")
                                       ]
                                       ),

    "Flip": operation("Flip", OperationType.MISC, text_inputs=[operation_TextInput("imgPath", "Source")], radio_inputs=[
        operation_RadioInput("flipMode", "Mode", ["Horizontal", "Vertical", "Horizontal and Vertical"])],
                      variable_outputs=[operation_TextInput("outName", "Output name")]),

    "LargestContour": operation("Largest Contour", OperationType.MISC,
                                text_inputs=[operation_TextInput("cntrs", "Contours")],
                                variable_outputs=[operation_TextInput("cntOut", "Output name")]),

    "Rotated Rectangle": operation("Rotated Rectangle", OperationType.MISC,
                                   text_inputs=[operation_TextInput("cntrs", "Contours")],
                                   variable_outputs=[operation_TextInput("cntOut", "Output name")]),

    "Blank Image": operation("Blank Image", OperationType.MISC, text_inputs=[operation_TextInput("src", "Source")],
                             variable_outputs=[operation_TextInput("cntOut", "Output name")]),

    "Fit ellipse": operation("Fit Ellipse", OperationType.MISC, text_inputs=[operation_TextInput("src", "Source")],
                             variable_outputs=[operation_TextInput("out", "Output")]),

    "Draw ellipse": operation("Draw Ellipse", OperationType.DRAW, text_inputs=[operation_TextInput("src", "Source"),
                                                                               operation_TextInput("ellipse",
                                                                                                   "Ellipse")],
                              color_inputs=[operation_ColorInput("clr", "Color")],
                              number_inputs=[operation_NumberInput("num", "Thickness")]),

    "Draw Found Circle": operation("Draw Found Circle", OperationType.DRAW,
                                   text_inputs=[operation_TextInput("src", "Source"),
                                                operation_TextInput("circle", "Circle")],
                                   color_inputs=[operation_ColorInput("clr", "Color")],
                                   number_inputs=[operation_NumberInput("num", "Thickness")]),

    "Draw Found Circles": operation("Draw Found Circles", OperationType.DRAW,
                                    text_inputs=[operation_TextInput("src", "Source"),
                                                 operation_TextInput("circle", "Circles")],
                                    color_inputs=[operation_ColorInput("clr", "Color")],
                                    number_inputs=[operation_NumberInput("num", "Thickness")]),

    "Minimum Enclosing Circle": operation("Minimum Enclosing Circle", OperationType.MISC,
                                          text_inputs=[operation_TextInput("src", "Source")],
                                          variable_outputs=[operation_TextInput("out", "Output")]),

    "Minimum Contour Area": operation("Minimum Contour Area", OperationType.MISC,
                                      text_inputs=[operation_TextInput("src", "Source")],
                                      number_inputs=[operation_NumberInput("area", "Area")],
                                      variable_outputs=[operation_TextInput("out", "Output")]),

    "Bounding Rectangle": operation("Bounding Rectangle", OperationType.MISC,
                                    text_inputs=[operation_TextInput("src", "Source")],
                                    variable_outputs=[operation_TextInput("retX", "X"),
                                                      operation_TextInput("retY", "Y"),
                                                      operation_TextInput("retW", "W"),
                                                      operation_TextInput("retH", "H")]),

    "Hough Circles": operation("Hough Circles", OperationType.MISC, text_inputs=[operation_TextInput("src", "Source")],
                               number_inputs=[operation_NumberInput("dp", "dp"), operation_NumberInput("md", "minDist"),
                                              operation_NumberInput("ht", "Higher Threshold"),
                                              operation_NumberInput("at", "Accumulator Threshold"),
                                              operation_NumberInput("minr", "Minimum Radius"),
                                              operation_NumberInput("maxr", "Maximum Radius")],
                               variable_outputs=[operation_TextInput("out", "Output")]),

    "Math Add": operation("Math Add", OperationType.ARITHMETIC, text_inputs=[operation_TextInput("val", "Value")],
                          number_inputs=[operation_NumberInput("add", "Value to add")]),

    "Canny": operation("Canny", OperationType.COLORS, text_inputs=[operation_TextInput("src", "Source")],
                       number_inputs=[operation_NumberInput("thres1", "Threshold 1"),
                                      operation_NumberInput("thres2", "Threshold 2")],
                       variable_outputs=[operation_TextInput("out", "Output")]),

    "ApproxPolyDP": operation("ApproxPolyDP", OperationType.MISC, text_inputs=[operation_TextInput("cnt", "Contours")],
                              number_inputs=[operation_NumberInput("min", "Minimum Sides"),
                                             operation_NumberInput("max", "Maximum Sides")],
                              variable_outputs=[operation_TextInput("out", "Output")]),

    "Convex Hull": operation("Convex Hull", OperationType.MISC, text_inputs=[operation_TextInput("cnt", "Contours"), ],
                             variable_outputs=[operation_TextInput("out", "Output")], ),

    "Square Contours": operation("Square Contours", OperationType.MISC,
                                 text_inputs=[operation_TextInput("cnt", "Contours"), ],
                                 number_inputs=[operation_NumberInput("thres", "Threshold")],
                                 variable_outputs=[operation_TextInput("out", "Output")], ),

    "Average Circle Radius": operation("Average Circle Radius", OperationType.MISC,
                                       text_inputs=[operation_TextInput("src", "Source")],
                                       variable_outputs=[operation_TextInput("out", "Output")]),

    "Circle Coords": operation("Circle Coords", OperationType.MISC, text_inputs=[operation_TextInput("src", "circles")],
                               number_inputs=[operation_TextInput("onemeter", "Size at 1 meter")],
                               variable_outputs=[operation_TextInput("out","Output")]),

    "Split Channel": operation("Split Channel", OperationType.ARITHMETIC,
                               text_inputs=[operation_TextInput("src", "Source")],
                               number_inputs=[operation_NumberInput("channel", "Select Channel"), ],
                               variable_outputs=[operation_TextInput("out", "Output")]),

    "Ratio": operation("Ratio", OperationType.ARITHMETIC, text_inputs=[operation_TextInput("cnts", "Contours")],
                       number_inputs=[operation_NumberInput("wth", "Width"), operation_NumberInput("height", "Height"),
                                      operation_NumberInput("thresh", "Threshold"), ],
                       variable_outputs=[operation_TextInput("out", "Output")]),

    "Almost Equal Sides": operation("Almost Equal Sides", OperationType.ARITHMETIC, text_inputs=[operation_TextInput("cnts", "Contours")],
                                    number_inputs=[operation_NumberInput("tol", "tolerance")],
                                    variable_outputs=[operation_TextInput("out", "Output")]),

    "Network Send Num Var": operation("Network Send Num Var", OperationType.MISC, text_inputs=[operation_TextInput("key", "Key"),operation_TextInput("var", "Number Variable")]),
}"""

@deprecated
class oldSky_operator:  # main class responsible for running operations
    def __init__(self):
        self.operations = []  # array of blocks (operations)
        self.sources = []  # array of cameras
        self.frames = []
        self.frameOptions = "<option value=None>No Available Options</option>"
        self.inCounter = 0  # differ between inputs
        self.values = {}  # dictionary of all values
        # self.allAnglesA = []

    def process(self):  # process operations each frame
        self.values.clear()

        source_counter = 0  # which camera you get info from

        for op in self.operations:  # INPUT OPERATIONS
            try:
                if op.type == OperationType.INPUT:  # if the type is from type "input" (cyan)
                    if op.name == "Image input":  # op.name is the value in the dict
                        self.values[op.variableOutputs[0].value] = cv2.imread(op.textInputs[0].value)

                    if op.name == "IP input":
                        cap = self.sources[source_counter]
                        if cap is not None:
                            ret, frame = cap.read()
                            self.values[op.variableOutputs[0].value] = frame
                            source_counter += 1

                    if op.name == "Webcam input":
                        cap = self.sources[source_counter]
                        if cap is not None:
                            ret, frame = cap.read()
                            self.values[op.variableOutputs[0].value] = frame
                            source_counter += 1

                if op.type == OperationType.MORPH:  # MORPH OPERATIONS

                    if op.name == "Gaussian Blur":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        KernelValue = int(op.numberInputs[0].value)
                        Kernel = (KernelValue, KernelValue)

                        iterations = int(op.numberInputs[1].value)
                        frame_blurred = cv2.GaussianBlur(src, Kernel,
                                                         iterations)  # last param would be the times it blurs
                        self.values[op.variableOutputs[0].value] = frame_blurred

                    if op.name == "MorphEx":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        KernelValue = int(op.numberInputs[0].value)
                        Kernel = np.ones((KernelValue, KernelValue), np.uint8)

                        Iterations = int(op.numberInputs[1].value)

                        convert_type = op.radioInputs[0].value

                        if convert_type == "Erosion":
                            output_frame = cv2.erode(src, Kernel, iterations=Iterations)

                        if convert_type == "Dilation":
                            output_frame = cv2.dilate(src, Kernel, iterations=Iterations)

                        if convert_type == "Opening":  # erosion then dilation (removes noise)
                            output_frame = cv2.morphologyEx(src, cv2.MORPH_OPEN, Kernel, iterations=Iterations)

                        if convert_type == "Closing":  # dilation then erosion (removes "holes" in pic)
                            output_frame = cv2.morphologyEx(src, cv2.MORPH_CLOSE, Kernel, iterations=Iterations)

                        self.values[op.variableOutputs[0].value] = output_frame

                if op.type == OperationType.ARITHMETIC:  # ARITHMETIC OPERATIONS
                    if op.name == "Bitwise AND":
                        src1 = op.textInputs[0].value
                        src1 = self.values[src1]

                        src2 = op.textInputs[1].value
                        src2 = self.values[src2]

                        maskval = op.textInputs[2].value

                        if maskval != str(-1):
                            mask = self.values[maskval]
                            final = cv2.bitwise_and(src1, src2, mask=mask)
                            self.values[op.variableOutputs[0].value] = final
                        else:
                            final = cv2.bitwise_and(src1, src2)
                            self.values[op.variableOutputs[0].value] = final

                    if op.name == "Math Add":
                        val = op.textInputs[0].value
                        value = int(self.values[val])
                        add = int(op.numberInputs[0].value)
                        res = (value + add)
                        self.values[val] = res

                    if op.name == "Split Channel":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        sel = int(op.numberInputs[0].value)
                        self.values[op.variableOutputs[0].value] = cv2.split(src)[sel]

                    if op.name == "Ratio":
                        cnt = op.textInputs[0].value
                        contours = self.values[cnt]

                        width = int(op.numberInputs[0].value)
                        height = int(op.numberInputs[1].value)
                        threshold = float(op.numberInputs[2].value)
                        validCnt = []

                        for cnt in contours:
                            x, y, w, h = cv2.boundingRect(cnt)

                            if abs(w / h - width / height) <= threshold:
                                validCnt.append(cnt)

                        self.values[op.variableOutputs[0].value] = validCnt

                    if op.name == "Almost Equal Sides":
                        
                        contours = self.values[op.textInputs[0].value]

                        tol = float(op.numberInputs[0].value)

                        correct = []

                        for cnt in contours:
                            distances = [math.dist(list(cnt[i][0]), list(cnt[i+1][0])) for i in range(len(cnt)-1)]
                            avg = sum(distances)/len(distances)
                            found = False

                            for d in distances:
                                if abs((d - avg)/avg) > tol:
                                    found = True
                                    break
                            
                            if not found:
                                correct.append(cnt)
                        
                        self.values[op.variableOutputs[0].value] = correct

                if op.type == OperationType.COLORS:  # COLOR OPERATIONS
                    if op.name == "Convert color":
                        src = op.textInputs[0].value
                        convert_type = op.radioInputs[0].value  # the conversion that was chosen

                        if convert_type == "BGR2HSV":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source, cv2.COLOR_BGR2HSV)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "BGR2RGB":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source, cv2.COLOR_BGR2RGB)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "BGR2GRAY":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source, cv2.COLOR_BGR2GRAY)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "HSV2RGB":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source, cv2.COLOR_HSV2RGB)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "HSV2RGB":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source, cv2.COLOR_HSV2BGR)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "GRAY2RGB":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source, cv2.COLOR_GRAY2RGB)
                            self.values[op.variableOutputs[0].value] = frame_converted

                    if op.name == "Color Mask":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        lower = hex_to_hsv(op.colorInputs[0].value)
                        lower = np.array([lower[0], lower[1] * 255, lower[2] * 255])

                        higher = hex_to_hsv(op.colorInputs[1].value)
                        higher = np.array([higher[0], higher[1] * 255, higher[2] * 255])

                        mask = cv2.inRange(src, lower, higher)
                        self.values[op.variableOutputs[0].value] = mask

                    if op.name == "Find Contours":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        cntrs, _ = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        self.values[op.variableOutputs[0].value] = cntrs

                    if op.name == "Canny":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        canny = cv2.Canny(src, int(op.numberInputs[0].value), int(op.numberInputs[1].value))
                        self.values[op.variableOutputs[0].value] = canny

                if op.type == OperationType.DRAW:  # DRAW OPERATIONS
                    if op.name == "Draw Contours":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        cnt = op.textInputs[1].value
                        cnt = self.values[cnt]
                        thickness = int(op.numberInputs[0].value)
                        color = hex_to_bgr(op.colorInputs[0].value)
                        cv2.drawContours(src, cnt, -1, color, thickness=thickness)

                    if op.name == "Draw Contour":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        cnt = op.textInputs[1].value
                        cnt = self.values[cnt]

                        thickness = int(op.numberInputs[0].value)
                        color = hex_to_bgr(op.colorInputs[0].value)
                        cv2.drawContours(src, [cnt], -1, color, thickness=thickness)

                    if op.name == "Draw Circle":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        radius = int(op.numberInputs[0].value)

                        x = int(op.numberInputs[1].value)
                        y = int(op.numberInputs[2].value)

                        thickness = int(op.numberInputs[3].value)

                        color = hex_to_bgr(op.colorInputs[0].value)

                        cv2.circle(src, (x, y), radius, color, thickness)

                    if op.name == "Draw Circle Params":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        radius = int(self.values[op.textInputs[1].value])
                        x = int(self.values[op.textInputs[2].value])
                        y = int(self.values[op.textInputs[3].value])

                        thickness = int(op.numberInputs[0].value)

                        color = hex_to_bgr(op.colorInputs[0].value)

                        cv2.circle(src, (x, y), radius, color, thickness)

                    if op.name == "Draw Rectangle Params":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        width = self.values[op.textInputs[1].value]
                        height = self.values[op.textInputs[2].value]
                        x = self.values[op.textInputs[3].value]
                        y = self.values[op.textInputs[4].value]
                        thickness = int(op.numberInputs[0].value)
                        color = hex_to_bgr(op.colorInputs[0].value)
                        cv2.rectangle(src, (x, y), (x + width, y + height), color, thickness)

                    if op.name == "Draw Found Circle":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        circle = op.textInputs[1].value
                        circle = self.values[circle]

                        thickness = int(op.numberInputs[0].value)

                        color = hex_to_bgr(op.colorInputs[0].value)

                        cv2.circle(src, circle[0], circle[1], color, thickness)

                    if op.name == "Draw Found Circles":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        circles = op.textInputs[1].value
                        circles = self.values[circles]
                        thickness = int(op.numberInputs[0].value)

                        color = hex_to_bgr(op.colorInputs[0].value)
                        for i in range(len(circles[0, :])):
                            # draw the outer circle
                            currCirc = circles[0, :][i]
                            cv2.circle(src, (currCirc[0], currCirc[1]), currCirc[2], color, thickness)

                    if op.name == "Draw Ellipse":
                        frame = op.textInputs[0].value
                        frame = self.values[frame]
                        ellipse = op.textInputs[1].value
                        ellipse = self.values[ellipse]
                        color = hex_to_bgr(op.colorInputs[0].value)
                        thickness = int(op.numberInputs[0].value)

                        cv2.ellipse(frame, ellipse, color, thickness)

                    if op.name == "Text":
                        src = op.textInputs[0].value
                        src = self.values[src]

                if op.type == OperationType.MISC:  # MISC OPERATIONS
                    if op.name == "Network Send Num Var":

                        self.values[op.textInputs[1].value] = int(self.values[op.textInputs[1].value])

                        print("Expected Val:",self.values[op.textInputs[1].value])
                        # print("Setting",op.textInputs[0].value,"to",self.values[op.textInputs[1].value])
                        skyv_network.set_number(op.textInputs[0].value,int(self.values[op.textInputs[1].value]))
                        print("Received Val:",skyv_network.get_number(op.textInputs[0].value,-1))

                    if op.name == "Flip":

                        src = op.textInputs[0].value
                        src = self.values[src]
                        flip_type = op.radioInputs[0].value  # the conversion that was chosen

                        if flip_type == "Horizontal":
                            frame_flipped = cv2.flip(src, 1)
                            self.values[op.variableOutputs[0].value] = frame_flipped
                        if flip_type == "Vertical":
                            frame_flipped = cv2.flip(src, 0)
                            self.values[op.variableOutputs[0].value] = frame_flipped
                        if flip_type == "Horizontal and Vertical":
                            frame_flipped = cv2.flip(src, -1)
                            self.values[op.variableOutputs[0].value] = frame_flipped

                    if op.name == "Largest Contour":
                        src = op.textInputs[0].value
                        contours = self.values[src]

                        largestCnt = 0
                        largestValue = -1

                        for cnt in contours:
                            currArea = cv2.contourArea(cnt)
                            if currArea > largestValue:
                                largestValue = currArea
                                largestCnt = cnt

                        self.values[op.variableOutputs[0].value] = cnt

                    if op.name == "Fit Ellipse":
                        src = op.textInputs[0].value
                        contour = self.values[src]
                        ellipse = cv2.fitEllipse(contour)

                        self.values[op.variableOutputs[0].value] = ellipse

                    if op.name == "Minimum Enclosing Circle":
                        src = op.textInputs[0].value
                        cnt = self.values[src]

                        (x, y), radius = cv2.minEnclosingCircle(cnt)

                        self.values[op.variableOutputs[0].value] = ((int(x), int(y)), int(radius))

                    if op.name == "Minimum Contour Area":
                        src = op.textInputs[0].value
                        contours = self.values[src]

                        area = int(op.numberInputs[0].value)

                        outcnts = []
                        for cnt in contours:
                            currarea = cv2.contourArea(cnt)
                            if currarea > area:
                                outcnts.append(cnt)

                        self.values[op.variableOutputs[0].value] = outcnts

                    if op.name == "Bounding Rectangle":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        x, y, w, h = cv2.boundingRect(src)

                        self.values[op.variableOutputs[0].value] = x
                        self.values[op.variableOutputs[1].value] = y
                        self.values[op.variableOutputs[2].value] = w
                        self.values[op.variableOutputs[3].value] = h

                    if op.name == "Rotated Rectangle":
                        cnt = op.textInputs[0].value
                        cnt = self.values[cnt]

                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)

                        self.values[op.variableOutputs[0].value] = [box]

                    if op.name == "Blank Image":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        height, width, channels = src.shape

                        blank_image = np.zeros((height, width, channels), np.uint8)

                        self.values[op.variableOutputs[0].value] = blank_image

                    if op.name == "Hough Circles":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        circles = cv2.HoughCircles(src, cv2.HOUGH_GRADIENT, int(op.numberInputs[0].value),
                                                   int(op.numberInputs[1].value),
                                                   param1=int(op.numberInputs[2].value),
                                                   param2=int(op.numberInputs[3].value),
                                                   minRadius=int(op.numberInputs[4].value),
                                                   maxRadius=int(op.numberInputs[5].value))
                        circles = np.uint16(np.around(circles))
                        self.values[op.variableOutputs[0].value] = circles

                    if op.name == "ApproxPolyDP":
                        cnt = op.textInputs[0].value
                        contours = self.values[cnt]

                        minsides = int(op.numberInputs[0].value)
                        maxsides = int(op.numberInputs[1].value)

                        contour_list = []
                        for contour in contours:
                            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
                            if minsides <= len(approx) <= maxsides:
                                contour_list.append(contour)

                        self.values[op.variableOutputs[0].value] = contour_list

                    if op.name == "Convex Hull":
                        cnt = op.textInputs[0].value
                        contours = self.values[cnt]

                        hull_list = []
                        for i in range(len(contours)):
                            hull = cv2.convexHull(contours[i])
                            hull_list.append(hull)

                        self.values[op.variableOutputs[0].value] = hull_list

                    if op.name == "Square Contours":
                        cnt = op.textInputs[0].value
                        contours = self.values[cnt]
                        thres = float(op.numberInputs[0].value)
                        cnt_list = []
                        for i in range(len(contours)):
                            _, _, w, h = cv2.boundingRect(contours[i])

                            if h * thres <= w <= h * ((1 - thres) + 1):
                                cnt_list.append(contours[i])
                        self.values[op.variableOutputs[0].value] = cnt_list

                    if op.name == "Average Circle Radius":
                        circs = op.textInputs[0].value
                        circles = self.values[circs]

                        circle_list = []

                        ccounter = 0
                        csum = 0

                        for circle in circles:
                            ccounter += 1
                            csum += circle[2]

                        avg = csum / ccounter

                        for circle in circles:
                            if circle[2] >= avg:
                                circle_list.append(circle)
                        self.values[op.variableOutputs[0].value] = circle_list

                    if op.name == "Circle Coords":
                        circs = op.textInputs[0].value
                        circles = self.values[circs]
                        onemeter = float(op.numberInputs[0].value)
                        if len(circles[0]) > 0:
                            for circ in circles[0]:
                                # distance = onemeter / circ[2]
                                # print("Dist - " + str(distance) + "[", onemeter, circ[2], "]")
                                # print(circ)
                                Resolution = (1280, 720)
                                F_Length = 10
                                Dot_Pitch = 9.84375
                                hFOV = 60

                                S_Width = Dot_Pitch * Resolution[1]  # in um
                                S_Width = S_Width / 1000  # in mm
                                F_Pix = (Resolution[0] / 2 / S_Width) * F_Length

                                K = np.array([[F_Pix, 0, Resolution[0] / 2], [0, F_Pix, Resolution[1] / 2],
                                            [0, 0, 1]])  # pinhole camera matrix

                                def FrameToWorldRay(Fx, Fy):
                                    Ki = np.linalg.inv(K)
                                    r = Ki.dot([Fx, Fy, 1])
                                    return r  # a "ray" in the sense that all the 3D points R = s * r, obtained by multiplying it for an arbitrary number s, will lie on the same line going through the camera center and pixel (x, y).

                                def RaysToAngle(R1,
                                                R2):  # calculate the angle between two rays using advanced math none of us understand. It is theoretically possible to find the 3D coords of a point and use simple trigonometry, but this looks nicer.
                                    cos_angle = R1.dot(R2) / (np.linalg.norm(R1) * np.linalg.norm(R2))
                                    angle_radians = np.arccos(cos_angle)
                                    return angle_radians

                                final_angle = np.degrees(RaysToAngle(FrameToWorldRay(circ[0], Resolution[1] / 2),
                                                                    FrameToWorldRay(Resolution[0] / 2, Resolution[1] / 2)))

                                dir = 1 if(circ[0] > Resolution[0] / 2) else -1
                                final_angle = dir * (final_angle)

                                self.values[op.variableOutputs[0].value] = final_angle
                        else:
                            self.values[op.variableOutputs[0].value] = -1
                            
            except Exception as e:
                # print(e) # prints exception
                pass

    def MoveUP(self, num):  # move operation up
        self.update()
        counter = 0
        curr_operation = 0

        try:
            for op in self.operations:
                if int(op.op_move_counter) == int(num):
                    curr_operation = op
                    self.operations.remove(op)
                    self.operations.insert(counter - 1, curr_operation)
                    break

                counter += 1
        except:
            pass

    def MoveDOWN(self, num):  # move operation down
        self.update()
        counter = 0
        curr_operation = 0

        try:
            for op in self.operations:
                if int(op.op_move_counter) == int(num):
                    curr_operation = op
                    self.operations.remove(op)
                    self.operations.insert(counter + 1, curr_operation)
                    break

                counter += 1
        except:
            pass

    def Delete(self, num):  # delete operation
        self.update()
        for op in self.operations:
            if int(op.op_move_counter) == int(num):
                self.operations.remove(op)
                self.inCounter -= 1
                break

        self.update()

    def update(self):  # process operations when update is pressed

        self.inCounter = len(self.values.values())
        print("UPDATING")

        self.sources.clear()
        self.frames.clear()

        for op in self.operations:  # update the counter used for addnum
            try:
                for t_in in op.textInputs:
                    t_in.value = request.form[t_in.inName]
                    self.inCounter += 1
                for n_in in op.numberInputs:
                    n_in.value = request.form[n_in.inName]
                    self.inCounter += 1
                for r_in in op.radioInputs:
                    r_in.value = request.form[r_in.inName]
                    self.inCounter += 1
                for c_in in op.checkboxInputs:
                    c_in.value = request.form.getlist(c_in.inName)
                    self.inCounter += 1
                for clr_in in op.colorInputs:
                    clr_in.value = request.form[clr_in.inName]
                    self.inCounter += 1
                for var_out in op.variableOutputs:
                    var_out.value = request.form[var_out.inName]
                    self.inCounter += 1
            except:
                pass

            try:
                if op.type == OperationType.INPUT:  # INPUT OPERATIONS
                    if op.name == "IP input":
                        camera = cv2.VideoCapture(op.textInputs[0].value)
                        if camera is not None:
                            self.sources.append(camera)

                    if op.name == "Webcam input":
                        id = int(op.numberInputs[0].value)
                        camera = cv2.VideoCapture(id)
                        self.sources.append(camera)

                if op.type == OperationType.MORPH:  # MORPH OPERATIONS
                    pass

                if op.type == OperationType.ARITHMETIC:  # ARITHMETIC OPERATIONS
                    pass

                if op.type == OperationType.COLORS:  # COLOR OPERATIONS
                    pass

                if op.type == OperationType.DRAW:  # DRAW OPERATIONS
                    pass

                if op.type == OperationType.MISC:  # MISC OPERATIONS
                    pass
            except:
                pass
        self.process()
        self.updateOutputOptions()

    def updateOutputOptions(self):
        self.frameOptions = ""
        for key in self.values:
            if isinstance(self.values[key], np.ndarray):
                if len(np.shape(self.values[key])) >= 2 <= 3:
                    self.frames.append(key)
                    self.frameOptions += "<option value=\"" + key + "\" style=\"background-color:#525252;\">" + key + "</option>"
                else:
                    # Add to correct values frame
                    pass
            elif isinstance(self.values[key], list):
                # Add to correct values frame
                pass

        # return self.frameOptions
        if self.frameOptions != "":
            return self.frameOptions
        return "<option value=None>No Available Options</option>"
# End

class OperationType(Enum):  # operation type. mostly used for the operation's color
    NONE = 0
    INPUT = 1
    MORPH = 2
    ARITHMETIC = 3
    COLORS = 4
    DRAW = 5
    MISC = 6

@deprecated
class oldOperation:  # main class for operation
    def __init__(self, name, operation_Type, text_inputs=[], number_inputs=[], radio_inputs=[], checkbox_inputs=[],
                 color_inputs=[], variable_outputs=[]):
        self.name = name
        self.type = operation_Type

        self.textInputs = text_inputs
        self.numberInputs = number_inputs
        self.radioInputs = radio_inputs
        self.checkboxInputs = checkbox_inputs
        self.colorInputs = color_inputs
        self.variableOutputs = variable_outputs

        self.op_move_counter = 0

    def add_num(self, num):  # add num adds a unique number to each input
        counter = randint(num, 9999999)
        for op_input in self.textInputs:
            counter += 1

            value = num + counter
            op_input.name = "name=\"" + op_input.inName + str(value) + "\""
            op_input.inName = op_input.inName + str(value)

        for op_input in self.numberInputs:
            counter += 1

            value = num + counter
            op_input.name = "name=\"" + op_input.inName + str(value) + "\""
            op_input.inName = op_input.inName + str(value)

        for op_input in self.radioInputs:
            counter += 1

            value = num + counter
            op_input.name = "name=\"" + op_input.inName + str(value) + "\""
            op_input.inName = op_input.inName + str(value)

        for op_input in self.checkboxInputs:
            counter += 1

            value = num + counter
            op_input.name = "name=\"" + op_input.inName + str(value) + "\""
            op_input.inName = op_input.inName + str(value)

        for op_input in self.colorInputs:
            counter += 1

            value = num + counter
            op_input.name = "name=\"" + op_input.inName + str(value) + "\""
            op_input.inName = op_input.inName + str(value)

        for op_input in self.variableOutputs:
            counter += 1

            value = num + counter
            op_input.name = "name=\"" + op_input.inName + str(value) + "\""
            op_input.inName = op_input.inName + str(value)

        self.op_move_counter = str(num)

    def conv_dict(self):  # turns the operation and it's inputs to a dictionary, required for json files

        text_in_dict = []
        for op_input in self.textInputs:
            text_in_dict.append(op_input.conv_dict())

        number_in_dict = []
        for op_input in self.numberInputs:
            number_in_dict.append(op_input.conv_dict())

        radio_in_dict = []
        for op_input in self.radioInputs:
            radio_in_dict.append(op_input.conv_dict())

        checkbox_in_dict = []
        for op_input in self.checkboxInputs:
            checkbox_in_dict.append(op_input.conv_dict())

        color_in_dict = []
        for op_input in self.colorInputs:
            color_in_dict.append(op_input.conv_dict())

        var_out_dict = []
        for op_output in self.variableOutputs:
            var_out_dict.append(op_output.conv_dict())

        ret_dict = {
            "name": self.name,
            "type": self.type,
            "text_in": text_in_dict,
            "number_in": number_in_dict,
            "radio_in": radio_in_dict,
            "check_in": checkbox_in_dict,
            "color_in": color_in_dict,
            "var_out": var_out_dict
        }

        return ret_dict

    def __str__(self):  # return the html version of the operation

        retdiv = "<div style=\"margin-top:7px;margin-bottom:7px;background-color:#525252;border-style: solid;border-color:"  # init div

        # set div color based on operation type
        div_color = "black"
        div_color = "#00fff7" if self.type == OperationType.INPUT else div_color
        div_color = "#ff9100" if self.type == OperationType.MORPH else div_color
        div_color = "#11ff00" if self.type == OperationType.ARITHMETIC else div_color
        div_color = "#e100ff" if self.type == OperationType.COLORS else div_color
        div_color = "#ff0000" if self.type == OperationType.DRAW else div_color
        div_color = "#fff200" if self.type == OperationType.MISC else div_color

        retdiv += div_color  # add div color
        retdiv += ";border-radius: 25px;\">"  # end div init

        retdiv += "<div style=\"padding-left:25px;padding-right:25px;padding-up:25px;padding-down:25px;display:inline-block;\">"  # add inner div

        # div contents here ->
        retdiv += html_header(self.name, brake=False, style="color:#ebebeb;")  # div Title
        # margin-right: 15px;margin-left: 65px;\"
        retdiv += "<div style=\"text-align: right;display: inline-block;\">"
        retdiv += "<button type=\"submit\" formmethod=\"post\" name=\"action\" value=\"Delete" + str(
            self.op_move_counter) + "\" style=\"margin-left:15px;color: #ebebeb;background-color:#525252\">Delete</button>"
        retdiv += "<button type=\"submit\" formmethod=\"post\" name=\"action\" value=\"MoveUP" + str(
            self.op_move_counter) + "\" style=\"margin-left:15px;color: #ebebeb;background-color:#525252\">Move UP</button>"
        retdiv += "<button type=\"submit\" formmethod=\"post\" name=\"action\" value=\"MovDON" + str(
            self.op_move_counter) + "\" style=\"margin-left:15px;color: #ebebeb;background-color:#525252\">Move DOWN</button><br/>"
        retdiv += "</div><br>"

        # add the html versions of all the inputs of the operation
        for text_input in self.textInputs:
            retdiv += str(text_input)

        for number_input in self.numberInputs:
            retdiv += str(number_input)

        for radio_input in self.radioInputs:
            retdiv += str(radio_input)

        for check_input in self.checkboxInputs:
            retdiv += str(check_input)

        for color_input in self.colorInputs:
            retdiv += str(color_input)

        for var_output in self.variableOutputs:
            retdiv += str(var_output)

        # <- div contents end here
        retdiv += "</div></div>"  # Close divs

        return retdiv

class operation:
    def __init__(self, name: str, type: OperationType, function: Callable):
        if "MoveUP" in name or "MoveDOWN" in name or "Delete" in name:
            raise Exception("You may not use 'MoveUP/ MoveDOWN/ Delete' in an operation's name.")

        self.name = name
        self.type = type
        self.function = function

        self.inputs = []

    def addInputText(self, name: str, value: str = ""):
        self.inputs.append({"TextInput" : [name,value]})
        return self
    def addInputNumber(self, name: str, value: str = 0, step: float = 0.0001):
        self.inputs.append({"NumberInput" : [name,value,step] })
        return self
    def addInputRadio(self, name: str, value: str = "", options: list = []):
        self.inputs.append({"RadioInput" : [name,value,options]})
        return self
    def addOutput(self, name: str = "Output"):
        self.inputs.append({"Output" : [name,""] })
        return self
    
    def html(self, operation, operation_id: int = 0) -> str:  # return the html version of the operation
        retdiv = "<div style=\"margin-top:7px;margin-bottom:7px;background-color:#525252;border-style: solid;border-color:"  # init div

        # set div color based on operation type
        div_color = "black"
        div_color = "#00fff7" if self.type == OperationType.INPUT else div_color
        div_color = "#ff9100" if self.type == OperationType.MORPH else div_color
        div_color = "#11ff00" if self.type == OperationType.ARITHMETIC else div_color
        div_color = "#e100ff" if self.type == OperationType.COLORS else div_color
        div_color = "#ff0000" if self.type == OperationType.DRAW else div_color
        div_color = "#fff200" if self.type == OperationType.MISC else div_color

        retdiv += div_color  # add div color
        retdiv += ";border-radius: 25px;\">"  # end div init

        retdiv += "<div style=\"padding-left:25px;padding-right:25px;padding-up:25px;padding-down:25px;display:inline-block;\">"  # add inner div

        # div contents here ->
        retdiv += html_header(self.name, brake=False, style="color:#ebebeb;")  # div Title
        retdiv += "<div style=\"text-align: right;display: inline-block;\">"

        for button in ['Delete','MoveUP', 'MoveDOWN']: # create buttons to move and delete operation
            retdiv += "<button type=\"submit\" formmethod=\"post\" name=\"action\" value=\"" + button + str(operation_id) + "\" style=\"margin-left:15px;color: #ebebeb;background-color:#525252\">" + button + "</button>"
        retdiv += "</div><br>"

        for input in operation["inputs"]:
            for key in input:
                input = input[key]
                id = 0
                name = input[0]
                value = input[1]

                if key == 'Output':
                    retdiv += str(operation_TextInput(name+str(operation_id)+str(id),text=name,value=value))
                if key == 'TextInput':
                    retdiv += str(operation_TextInput(name+str(operation_id)+str(id),text=name,value=value))
                if key == 'NumberInput':
                    retdiv += str(operation_NumberInput(name+str(operation_id)+str(id),text=name,value=value,step = input[2]))
                if key == 'RadioInput':
                    retdiv += str(operation_RadioInput(name+str(operation_id)+str(id),text=name,value=value,options=input[2]))

                # if key == 'CheckInput':
                #     retdiv += str(check_input)

                # if key == 'ColorInput':
                #     retdiv += str(color_input)

                # if key == 'Output':
                #     retdiv += str(var_output)

        # <- div contents end here
        retdiv += "</div></div>"  # Close divs
        return retdiv

class operator:
    def __init__(self,) -> None:
        self.loaded_operations = {}  # array of blocks (operations)
        self.operations = []  # array of blocks (operations)

        self.sources = {}  # array of cameras
        self.frames = []
        self.frameOptions = "<option value=None>No Available Options</option>"

        self.opValues = {}
        self.opOutputs = []
        self.values = {}  # dictionary of all values
        self.updating = False
        self.required_out = "None"

        self.outResolution = 0.5

    def process(self):
        for op in self.operations:
            self.opValues.clear()
            self.opOutputs.clear()
            for input in op["inputs"]:
                for key in input:
                    name = input[key][0]
                    value = input[key][1]
                    if "Input" in key:
                        value = float(value) if str(value).isnumeric() else value
                        if(type(value) == str):
                            if(len(value) > 2):
                                if(value[0] == '&' and value[-1] == '&'):
                                    value = self.values[value[1:-1]]

                        self.opValues[name] = value
                    elif "Output" in key:
                        self.opOutputs.append(value)
            try:
                operation_outputs = self.getOperationSource(op).function(self.opValues,self)
            except Exception as error:
                print(tColors.FAIL + getTime() + "OPERATION ERROR\n===============\n" + str(error) + tColors.ENDC)
            if operation_outputs is not None:
                self.values.update(dict(zip(self.opOutputs,operation_outputs)))

    def update(self, fromUpdate: bool = True):
        self.updating = True
        self.sources.clear()
        self.values.clear()
        tmp_operations = copy.deepcopy(self.operations)  # duplicate the operations array
        for op_id in range(len(tmp_operations)):
            op = tmp_operations[op_id]
            for input_id in range(len(op["inputs"])):
                input = op["inputs"][input_id]
                for key in input:
                    id = 0
                    name = input[key][0]
                    value = input[key][1]
                    if fromUpdate:
                        value = request.form[name+str(op_id)+str(id)]
                        tmp_operations[op_id]["inputs"][input_id][key][1] = value
            
        self.operations = copy.deepcopy(tmp_operations) # update operations to duplicate
        del tmp_operations
        self.process()
        self.getOutputOptions()
        self.updating = False
        
    def loadOperation(self, op: operation):
        self.loaded_operations[op.name] = op
        return
    
    def loadOperationArray(self, ops: list[operation]):
        for op in ops:
            self.loadOperation(op)
        # self.update(True)

    def addOperation(self, op_name: str):
        if op_name in self.loaded_operations:
            self.operations.append({'name'  : str(format((len(self.operations) + 1),'05d')) + op_name,
                                    "inputs" : self.loaded_operations[op_name].inputs,
                                    "type" : 1})
        else:
            print(tColors.FAIL+getTime()+"Unable to add operation \"" + op_name + "\""+tColors.ENDC )

    def removeOperation(self, op_id: int):
        self.operations.pop(op_id)

    def moveOperation(self, op_id: int, direction: int):
        self.update()
        self.operations.insert(max(0,op_id+direction), self.operations.pop(op_id))

    def clearOperations(self):
        self.operations.clear()

    def getOperationSource(self, op: operation) -> operation:
        return self.loaded_operations[op["name"][5:]]

    def getOutputOptions(self):
        self.frameOptions = ""
        for key in self.values:
            if isinstance(self.values[key], np.ndarray):
                if len(np.shape(self.values[key])) >= 2 <= 3:
                    self.frames.append(key)
                    self.frameOptions += "<option value=\"" + key + "\" style=\"background-color:#525252;\">" + key + "</option>"
        if self.frameOptions != "":
            return self.frameOptions
        return "<option value=None>No Available Options</option>"

    def htmlOps(self):
        htmls = []
        for id in range(len(self.operations)):
            op = self.operations[id]
            htmls.append(self.getOperationSource(op).html(op,id))
        return htmls

    def generateVideo(self):  # generates the output frame
        time.sleep(1)  # delay to allow for camera reconnection
        while True:
            outputs = self.values  # get all values from the operator

            try:  # try to set the output frame to the required frame
                selected_out = outputs[self.required_out]  # set the output to the required frame
                selected_out = cv2.resize(selected_out,(int(selected_out.shape[1] * self.outResolution),int(selected_out.shape[0] * self.outResolution)))
            except:  # if setting output frame fails, set it to the error pic
                selected_out = None
                selected_out = cv2.resize(error_pic,(int(error_pic.shape[1] * 0.25),int(error_pic.shape[0] * 0.25)))  # set the output frame to the error pic
                
            ret, encodedImage = cv2.imencode(".jpg", selected_out)  # turn the output pic to a jpg
            if ret:  # if encoding to jpg fails, skip this frame
                self.outputVid = (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
                yield self.outputVid  # output the frame in a format that the browser can read