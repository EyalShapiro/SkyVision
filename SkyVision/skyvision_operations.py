from skyvision import *
from SkyVision_Tools import *
from flask import *
import cv2

sky_operations = { # sky operation is a dictionary that defines the inputs each operation has

    #EXAMPLE ->
    #Key : operation("operation name",OperationType,
    #   text_inputs=[operation_TextInput("html Name", " html Text")],
    #   number_inputs=[operation_NumberInput("html Name", "html Text")])
    "Image Input" : operation("Image input",OperationType.INPUT,text_inputs=[operation_TextInput("imgPath","Image Path")],variable_outputs=[operation_TextInput("outName","Output name")]),
    
    "Webcam Input" : operation("Webcam input",OperationType.INPUT,number_inputs=[operation_NumberInput("webcamID","Webcam ID")],variable_outputs=[operation_TextInput("outName","Output name")]),

    "IP Input" : operation("IP input [DEPRECATED]",OperationType.INPUT,text_inputs=[operation_TextInput("webcamID","Webcam ID")],variable_outputs=[operation_TextInput("outName","Output name")]),

    "Color Mask" : operation("Color Mask",OperationType.COLORS,
        text_inputs=[
            operation_TextInput("src","Source")],
        color_inputs=[
            operation_ColorInput("lower","Lower"),
            operation_ColorInput("higher","Higher")],
        variable_outputs=[
            operation_TextInput("outName","Output name")]
    ),

    "Convert Color" : operation("Convert color",OperationType.COLORS,
        text_inputs=[
            operation_TextInput("src","Source")],
        radio_inputs=[
            operation_RadioInput("type","Type",
            options=[
                "BGR2HSV",
                "BGR2RGB",
                "BGR2GRAY",
                "HSV2RGB",
                "HSV2BGR",
                "GRAY2RGB",
            ])],
        variable_outputs=[operation_TextInput("outName","Output name")]
    ),

    "Gaussian Blur" : operation("Gaussian Blur", OperationType.MORPH,
        text_inputs=[
            operation_TextInput("src", "Source")],
        number_inputs=[
            operation_NumberInput("kernel", "Kernel Value"),
            operation_NumberInput("iter", "Iterations")
        ],
        variable_outputs=[operation_TextInput("outName","Output name")]
    ),

    "MorphEx" : operation("MorphEx", OperationType.MORPH,
        text_inputs=[
            operation_TextInput("src", "Source")],
        number_inputs=[
            operation_NumberInput("kernel","Kernel"),
            operation_NumberInput("itr", "Iterations")],
        radio_inputs=[
                operation_RadioInput("type","Type",
                options=[
                    "Erosion",
                    "Dilation",
                    "Opening",
                    "Closing",
                ])],
        variable_outputs=[operation_TextInput("outName","Output name")]
    ),
 
    "Bitwise And" : operation("Bitwise AND",OperationType.ARITHMETIC,
        text_inputs=[
            operation_TextInput("src1","Source 1"),
            operation_TextInput("src2","Source 2"),
            operation_TextInput("mask","Mask"),
            ]
        ,variable_outputs=[operation_TextInput("outName","Output name")]
    ),

    "Find Contours" : operation("Find Contours",OperationType.COLORS,
        text_inputs=[
            operation_TextInput("src","Source"),
            ]
        ,variable_outputs=[operation_TextInput("outName","Output name")]
    ),

    "Draw Contours" : operation("Draw Contours",OperationType.DRAW,
        text_inputs=[
            operation_TextInput("src","Source"),
            operation_TextInput("cnt","Contours"),
            ],
        number_inputs=[
            operation_NumberInput("thick","Thickness"),
        ],
        color_inputs=[
            operation_ColorInput("clr","Color"),]
    ),

    "Draw Contour" : operation("Draw Contour",OperationType.DRAW,
        text_inputs=[
            operation_TextInput("src","Source"),
            operation_TextInput("cnt","Contours"),
            ],
        number_inputs=[
            operation_NumberInput("thick","Thickness"),
        ],
        color_inputs=[
            operation_ColorInput("clr","Color"),]
    ),

    "Draw Circle" : operation("Draw Circle", OperationType.DRAW,
        text_inputs=[
            operation_TextInput("src", "Source"),
        ],
        number_inputs=[
            operation_NumberInput("radius","Radius"),
            operation_NumberInput("xValue","X","padding-right:5px",brake=False),
            operation_NumberInput("yValue","Y"),
            operation_NumberInput("thickness", "Thickness")
        ],
        color_inputs=[
            operation_ColorInput("Color","Color")
        ]
    ),

    "Draw Circle Params" : operation("Draw Circle Params", OperationType.DRAW,
        text_inputs=[
            operation_TextInput("src", "Source"),
            operation_TextInput("radius","Radius"),
            operation_TextInput("xValue","X","padding-right:5px",brake=False),
            operation_TextInput("yValue","Y"),
        ],
        number_inputs=[
            operation_TextInput("thickness", "Thickness")
        ],
        color_inputs=[
            operation_ColorInput("Color","Color")
        ]
    ),

    "Draw Rectangle Params" : operation("Draw Rectangle Params", OperationType.DRAW,
        text_inputs=[
            operation_TextInput("src", "Source"),
            operation_TextInput("wth","Width"),
            operation_TextInput("hght","Height"),
            operation_TextInput("xValue","X","padding-right:5px;color: #ebebeb;background-color:#525252;",brake=False),
            operation_TextInput("yValue","Y"),
        ],
        number_inputs=[
            operation_TextInput("thickness", "Thickness")
        ],
        color_inputs=[
            operation_ColorInput("Color","Color")
        ]
    ),

    "Flip" : operation("Flip",OperationType.MISC,text_inputs=[operation_TextInput("imgPath","Source")],radio_inputs=[operation_RadioInput("flipMode","Mode",["Horizontal","Vertical","Horizontal and Vertical"])],variable_outputs=[operation_TextInput("outName","Output name")]),

    "LargestContour" : operation("Largest Contour",OperationType.MISC,text_inputs=[operation_TextInput("cntrs","Contours")],variable_outputs=[operation_TextInput("cntOut","Output name")]),

    "Rotated Rectangle" : operation("Rotated Rectangle",OperationType.MISC,text_inputs=[operation_TextInput("cntrs","Contours")],variable_outputs=[operation_TextInput("cntOut","Output name")]),

    "Blank Image" : operation("Blank Image",OperationType.MISC,text_inputs=[operation_TextInput("src","Source")],variable_outputs=[operation_TextInput("cntOut","Output name")]),

    "Fit ellipse": operation("Fit Ellipse",OperationType.MISC,text_inputs=[operation_TextInput("src","Source")],variable_outputs=[operation_TextInput("out","Output")]),

    "Draw ellipse": operation("Draw Ellipse",OperationType.DRAW,text_inputs=[operation_TextInput("src","Source"),operation_TextInput("ellipse","Ellipse")],color_inputs=[operation_ColorInput("clr","Color")],number_inputs=[operation_NumberInput("num","Thickness")]),

    "Draw Found Circle": operation("Draw Found Circle",OperationType.DRAW,text_inputs=[operation_TextInput("src","Source"),operation_TextInput("circle","Circle")],color_inputs=[operation_ColorInput("clr","Color")],number_inputs=[operation_NumberInput("num","Thickness")]),

    "Draw Found Circles": operation("Draw Found Circles",OperationType.DRAW,text_inputs=[operation_TextInput("src","Source"),operation_TextInput("circle","Circles")],color_inputs=[operation_ColorInput("clr","Color")],number_inputs=[operation_NumberInput("num","Thickness")]),

    "Minimum Enclosing Circle": operation("Minimum Enclosing Circle",OperationType.MISC,text_inputs=[operation_TextInput("src","Source")],variable_outputs=[operation_TextInput("out","Output")]),

    "Minimum Contour Area": operation("Minimum Contour Area",OperationType.MISC,text_inputs=[operation_TextInput("src","Source")],number_inputs=[operation_NumberInput("area","Area")],variable_outputs=[operation_TextInput("out","Output")]),

    "Bounding Rectangle": operation("Bounding Rectangle",OperationType.MISC,text_inputs=[operation_TextInput("src","Source")],variable_outputs=[operation_TextInput("retX","X"),operation_TextInput("retY","Y"),operation_TextInput("retW","W"),operation_TextInput("retH","H")]),

    "Hough Circles": operation("Hough Circles",OperationType.MISC,text_inputs=[operation_TextInput("src","Source")],number_inputs=[operation_NumberInput("dp","dp"),operation_NumberInput("md","minDist"),operation_NumberInput("ht","Higher Threshold"),operation_NumberInput("at","Accumulator Threshold"),operation_NumberInput("minr","Minimum Radius"),operation_NumberInput("maxr","Maximum Radius")],variable_outputs=[operation_TextInput("out","Output")]),

    "Math Add" : operation("Math Add",OperationType.ARITHMETIC,text_inputs=[operation_TextInput("val","Value")],number_inputs=[operation_NumberInput("add","Value to add")]),

    "Canny" : operation("Canny",OperationType.COLORS,text_inputs=[operation_TextInput("src","Source")],number_inputs=[operation_NumberInput("thres1","Threshold 1"),operation_NumberInput("thres2","Threshold 2")],variable_outputs=[operation_TextInput("out","Output")]),

    "ApproxPolyDP" : operation("ApproxPolyDP",OperationType.MISC,text_inputs=[operation_TextInput("cnt","Contours")],number_inputs=[operation_NumberInput("min","Minimum Sides"),operation_NumberInput("max","Maximum Sides")],variable_outputs=[operation_TextInput("out","Output")]),

    "Convex Hull" : operation("Convex Hull",OperationType.MISC, text_inputs=[operation_TextInput("cnt","Contours"),],variable_outputs=[operation_TextInput("out","Output")],),

    "Square Contours" : operation("Square Contours",OperationType.MISC, text_inputs=[operation_TextInput("cnt","Contours"),],number_inputs=[operation_NumberInput("thres","Threshold")],variable_outputs=[operation_TextInput("out","Output")],),

    "Average Circle Radius": operation("Average Circle Radius",OperationType.MISC,text_inputs=[operation_TextInput("src","Source")],variable_outputs=[operation_TextInput("out","Output")]),

    "Circle Coords": operation("Circle Coords",OperationType.MISC,text_inputs=[operation_TextInput("src","circles")],number_inputs=[operation_TextInput("onemeter","Size at 1 meter")]),

    "Split Channel": operation("Split Channel",OperationType.ARITHMETIC,text_inputs=[operation_TextInput("src","Source")],number_inputs=[operation_NumberInput("channel","Select Channel"),],variable_outputs=[operation_TextInput("out","Output")]),

    "Ratio": operation("Ratio",OperationType.ARITHMETIC,text_inputs=[operation_TextInput("cnts","Contours")],number_inputs=[operation_NumberInput("wth","Width"),operation_NumberInput("height","Height"),operation_NumberInput("thresh","Threshold"),],variable_outputs=[operation_TextInput("out","Output")]),
}

class sky_operator: # main class responsible for running operations
    def __init__(self):
        self.operations = [] #array of blocks (operations)
        self.sources = [] #array of cameras 
        self.inCounter = 0 #differ between inputs
        self.values = {} #dictionary of all values

    def process(self): # process operations each frame
        self.values.clear()

        source_counter = 0 #which camera you get info from

        for op in self.operations: # INPUT OPERATIONS
            try:
                if op.type == OperationType.INPUT: #if the type is from type "input" (cyan)
                    if op.name == "Image input": #op.name is the value in the dict
                        self.values[op.variableOutputs[0].value] = cv2.imread(op.textInputs[0].value) 
                   
                    if op.name == "IP input":
                        cap = self.sources[source_counter]
                        if cap is not None:
                            ret, frame = cap.read()
                            self.values[op.variableOutputs[0].value] = frame
                            source_counter+=1

                    if op.name == "Webcam input":
                        cap = self.sources[source_counter]
                        if cap is not None:
                            ret, frame = cap.read()
                            self.values[op.variableOutputs[0].value] = frame
                            source_counter+=1

                if op.type == OperationType.MORPH: # MORPH OPERATIONS
                    
                    if op.name == "Gaussian Blur":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        KernelValue = int(op.numberInputs[0].value)
                        Kernel = (KernelValue,KernelValue)
                        
                        iterations = int(op.numberInputs[1].value)
                        frame_blurred = cv2.GaussianBlur(src, Kernel,iterations) #last param would be the times it blurs
                        self.values[op.variableOutputs[0].value] = frame_blurred

                    if op.name == "MorphEx":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        KernelValue = int(op.numberInputs[0].value)
                        Kernel = np.ones((KernelValue,KernelValue), np.uint8)

                        Iterations = int(op.numberInputs[1].value)
                    
                        convert_type = op.radioInputs[0].value

                        if convert_type == "Erosion":
                            output_frame = cv2.erode(src, Kernel, iterations=Iterations)


                        if convert_type == "Dilation":
                            output_frame = cv2.dilate(src, Kernel, iterations=Iterations)


                        if convert_type == "Opening": #erosion then dilation (removes noise)
                            output_frame = cv2.morphologyEx(src, cv2.MORPH_OPEN,Kernel, iterations=Iterations)
                        
                        if convert_type == "Closing": #dilation then erosion (removes "holes" in pic)
                            output_frame = cv2.morphologyEx(src,cv2.MORPH_CLOSE ,Kernel, iterations=Iterations  )
                        
                        self.values[op.variableOutputs[0].value] = output_frame

                if op.type == OperationType.ARITHMETIC: # ARITHMETIC OPERATIONS
                    if op.name == "Bitwise AND":
                        src1 = op.textInputs[0].value
                        src1 = self.values[src1]

                        src2 = op.textInputs[1].value
                        src2 = self.values[src2]

                        maskval = op.textInputs[2].value

                        if maskval != str(-1):
                            mask = self.values[maskval]
                            final = cv2.bitwise_and(src1,src2,mask=mask)
                            self.values[op.variableOutputs[0].value] = final
                        else:
                            final = cv2.bitwise_and(src1,src2)
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
                        validCnt=[]

                        for cnt in contours:
                            x,y,w,h = cv2.boundingRect(cnt)

                            if abs(w/h - width/height) <= threshold:
                                validCnt.append(cnt)
                                print(abs(w/h - width/height))

                        self.values[op.variableOutputs[0].value] = validCnt

                if op.type == OperationType.COLORS: # COLOR OPERATIONS
                    if op.name == "Convert color":
                        src = op.textInputs[0].value
                        convert_type = op.radioInputs[0].value #the conversion that was chosen  

                        if convert_type == "BGR2HSV":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_BGR2HSV)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "BGR2RGB":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_BGR2RGB)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "BGR2GRAY":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_BGR2GRAY)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "HSV2RGB":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_HSV2RGB)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "HSV2RGB":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_HSV2BGR)
                            self.values[op.variableOutputs[0].value] = frame_converted
                        if convert_type == "GRAY2RGB":
                            frame_source = self.values[src]
                            frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_GRAY2RGB)
                            self.values[op.variableOutputs[0].value] = frame_converted

                    if op.name == "Color Mask":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        lower = hex_to_hsv(op.colorInputs[0].value)
                        lower = np.array([lower[0],lower[1]*255,lower[2]*255])

                        higher = hex_to_hsv(op.colorInputs[1].value)
                        higher = np.array([higher[0],higher[1]*255,higher[2]*255])

                        mask = cv2.inRange(src, lower, higher)
                        self.values[op.variableOutputs[0].value] = mask

                    if op.name == "Find Contours":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        cntrs, _ = cv2.findContours(src,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        self.values[op.variableOutputs[0].value] = cntrs

                        if(op.variableOutputs[0].value == "cannycnts"):
                            print("FOUND",len(cntrs))

                    if op.name == "Canny":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        canny = cv2.Canny(src,int(op.numberInputs[0].value),int(op.numberInputs[1].value))
                        self.values[op.variableOutputs[0].value] = canny

                if op.type == OperationType.DRAW: # DRAW OPERATIONS
                    if op.name == "Draw Contours":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        cnt = op.textInputs[1].value
                        cnt = self.values[cnt]
                        thickness = int(op.numberInputs[0].value)
                        color = hex_to_bgr(op.colorInputs[0].value)
                        cv2.drawContours(src,cnt,-1,color,thickness=thickness)

                    if op.name == "Draw Contour":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        cnt = op.textInputs[1].value
                        cnt = self.values[cnt]

                        thickness = int(op.numberInputs[0].value)
                        color = hex_to_bgr(op.colorInputs[0].value)
                        cv2.drawContours(src,[cnt],-1,color,thickness=thickness)

                    if op.name == "Draw Circle":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        radius = int(op.numberInputs[0].value)

                        x = int(op.numberInputs[1].value)
                        y = int(op.numberInputs[2].value)

                        thickness = int(op.numberInputs[3].value)


                        color = hex_to_bgr(op.colorInputs[0].value)

                        cv2.circle(src,(x,y), radius, color, thickness)

                    if op.name == "Draw Circle Params":
                        

                        src = op.textInputs[0].value
                        src = self.values[src]
                        radius = int(self.values[op.textInputs[1].value])
                        x = int(self.values[op.textInputs[2].value])
                        y = int(self.values[op.textInputs[3].value])
                        
                        thickness = int(op.numberInputs[0].value)

                        color = hex_to_bgr(op.colorInputs[0].value)

                        cv2.circle(src,(x,y), radius, color, thickness)

                    if op.name == "Draw Rectangle Params":

                        src = op.textInputs[0].value
                        src = self.values[src]
                        width = self.values[op.textInputs[1].value]
                        height = self.values[op.textInputs[2].value]
                        x = self.values[op.textInputs[3].value]
                        y = self.values[op.textInputs[4].value]
                        thickness = int(op.numberInputs[0].value)
                        color = hex_to_bgr(op.colorInputs[0].value)
                        cv2.rectangle(src,(x,y), (x+width,y+height), color, thickness)
                        print("rect-",x,y,width,height)

                    if op.name == "Draw Found Circle":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        
                        circle = op.textInputs[1].value
                        circle = self.values[circle]
                        
                        thickness = int(op.numberInputs[0].value)
                        
                        color = hex_to_bgr(op.colorInputs[0].value)
                        
                        cv2.circle(src,circle[0], circle[1], color, thickness)
                        
                    if op.name == "Draw Found Circles":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        circles = op.textInputs[1].value
                        circles = self.values[circles]
                        thickness = int(op.numberInputs[0].value)
                        
                        color = hex_to_bgr(op.colorInputs[0].value)
                        for i in range(len(circles[0,:])):
                                # draw the outer circle
                                currCirc = circles[0,:][i]
                                cv2.circle(src,(currCirc[0],currCirc[1]),currCirc[2],color,thickness)

                    if op.name =="Draw Ellipse":
                        frame = op.textInputs[0].value
                        frame = self.values[frame]
                        ellipse = op.textInputs[1].value
                        ellipse = self.values[ellipse]
                        color = hex_to_bgr(op.colorInputs[0].value)
                        thickness = int(op.numberInputs[0].value)

                        cv2.ellipse(frame,ellipse,color,thickness)

                    if op.name == "Text":
                        src = op.textInputs[0].value
                        src = self.values[src]
                    
                if op.type == OperationType.MISC: # MISC OPERATIONS
                    if op.name == "Flip":
                        
                        src = op.textInputs[0].value
                        src = self.values[src]
                        flip_type = op.radioInputs[0].value #the conversion that was chosen  

                        if flip_type == "Horizontal":
                            frame_flipped = cv2.flip(src,1)
                            self.values[op.variableOutputs[0].value] = frame_flipped
                        if flip_type == "Vertical":
                            frame_flipped = cv2.flip(src,0)
                            self.values[op.variableOutputs[0].value] = frame_flipped
                        if flip_type == "Horizontal and Vertical":
                            frame_flipped = cv2.flip(src,-1)
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
                        src= op.textInputs[0].value
                        contour = self.values[src]
                        ellipse = cv2.fitEllipse(contour)
                        
                        self.values[op.variableOutputs[0].value] = ellipse                    

                    if op.name == "Minimum Enclosing Circle":
                        src= op.textInputs[0].value
                        cnt = self.values[src]

                        (x,y),radius = cv2.minEnclosingCircle(cnt)

                        self.values[op.variableOutputs[0].value] = ((int(x),int(y)),int(radius))                    

                    if op.name == "Minimum Contour Area":
                        src= op.textInputs[0].value
                        contours = self.values[src]

                        area = int(op.numberInputs[0].value)

                        outcnts = []
                        for cnt in contours:
                            currarea = cv2.contourArea(cnt)
                            if(currarea > area):
                                outcnts.append(cnt)

                        self.values[op.variableOutputs[0].value] = outcnts

                    if op.name == "Bounding Rectangle":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        x,y,w,h = cv2.boundingRect(src)

                        self.values[op.variableOutputs[0].value] = x
                        self.values[op.variableOutputs[1].value] = y
                        self.values[op.variableOutputs[2].value] = w
                        self.values[op.variableOutputs[3].value] = h

                        print("BOUND")

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

                        blank_image = np.zeros((height,width,channels), np.uint8)

                        self.values[op.variableOutputs[0].value] = blank_image

                    if op.name == "Hough Circles":
                        src = op.textInputs[0].value
                        src = self.values[src]
                        circles = cv2.HoughCircles(src,cv2.HOUGH_GRADIENT,int(op.numberInputs[0].value),int(op.numberInputs[1].value),
                            param1=int(op.numberInputs[2].value),param2=int(op.numberInputs[3].value),minRadius=int(op.numberInputs[4].value),maxRadius=int(op.numberInputs[5].value))
                        circles = np.uint16(np.around(circles))
                        self.values[op.variableOutputs[0].value] = circles

                    if op.name == "ApproxPolyDP":
                        cnt = op.textInputs[0].value
                        contours = self.values[cnt]

                        minsides = int(op.numberInputs[0].value)
                        maxsides = int(op.numberInputs[1].value)

                        contour_list = []
                        for contour in contours:
                            approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
                            if ((len(approx) >= minsides and len(approx) <= maxsides)):
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
                            _,_,w,h = cv2.boundingRect(contours[i])

                            if(w >= h * thres and w <= h * ((1 - thres) + 1)):
                                cnt_list.append(contours[i])
                        self.values[op.variableOutputs[0].value] = cnt_list

                    if op.name == "Average Circle Radius":
                        circs = op.textInputs[0].value
                        circles = self.values[circs]
                        
                        circle_list = []

                        ccounter = 0
                        csum = 0

                        for circle in circles:
                            ccounter+=1
                            csum += circle[2]

                        avg = csum / ccounter

                        for circle in circles:
                            if(circle[2] >= avg):
                                circle_list.append(circle)
                        self.values[op.variableOutputs[0].value] = circle_list
            
                    if op.name == "Circle Coords":
                        circs = op.textInputs[0].value
                        circles = self.values[circs]
                        onemeter = float(op.numberInputs[0].value)
                        for circ in circles[0]:
                            distance = onemeter / circ[2]
                            
                            print("Dist - " + str(distance) + "[",onemeter,circ[2],"]")

                        
                        
            except:
                pass

    def MoveUP(self,num): # move operation up
        self.update()
        counter = 0
        curr_operation = 0

        try:
            for op in self.operations:
                if int(op.op_move_counter) == int(num):
                    curr_operation = op
                    self.operations.remove(op)
                    self.operations.insert(counter-1,curr_operation)
                    break

                counter += 1
        except:
            pass

    def MoveDOWN(self,num): # move operation down
        self.update()
        counter = 0
        curr_operation = 0

        try:
            for op in self.operations:
                if int(op.op_move_counter) == int(num):
                    curr_operation = op
                    self.operations.remove(op)
                    self.operations.insert(counter+1,curr_operation)
                    break

                counter += 1
        except:
            pass

    def Delete(self,num): # delete operation
        self.update()
        for op in self.operations:
            if int(op.op_move_counter) == int(num):
                self.operations.remove(op)
                print("Removed")
                self.inCounter -= 1
                break

        
        self.update()

    def update(self): # process operations when update is pressed

        self.inCounter = len(self.values.values())

        print("UPDATING")

        self.sources.clear()

        for op in self.operations: # update the counter used for addnum
            for t_in in op.textInputs:
                t_in.value = request.form[t_in.inName]
                self.inCounter+=1
            for n_in in op.numberInputs:
                n_in.value = request.form[n_in.inName]
                self.inCounter+=1
            for r_in in op.radioInputs:
                r_in.value = request.form[r_in.inName]
                self.inCounter+=1
            for c_in in op.checkboxInputs:
                c_in.value = request.form.getlist(c_in.inName)
                self.inCounter+=1
            for clr_in in op.colorInputs:
                clr_in.value = request.form[clr_in.inName]
                self.inCounter+=1
            for var_out in op.variableOutputs:
                var_out.value = request.form[var_out.inName]
                self.inCounter+=1
            
            try:
                if op.type == OperationType.INPUT: # INPUT OPERATIONS
                    if op.name == "IP input":
                        camera = cv2.VideoCapture(op.textInputs[0].value)
                        if camera is not None:
                            self.sources.append(camera)
                            print("READ IP")
                        else:
                            print("READ ERR")

                    if op.name == "Webcam input":
                        id = int(op.numberInputs[0].value)
                        camera = cv2.VideoCapture(id)
                        self.sources.append(camera)
                        
                        



                if op.type == OperationType.MORPH: # MORPH OPERATIONS
                    pass


                if op.type == OperationType.ARITHMETIC: # ARITHMETIC OPERATIONS
                    pass


                if op.type == OperationType.COLORS: # COLOR OPERATIONS
                    pass

                if op.type == OperationType.DRAW: # DRAW OPERATIONS
                    pass


                if op.type == OperationType.MISC: # MISC OPERATIONS
                    pass
            except:
                pass
            
        self.process()
#End