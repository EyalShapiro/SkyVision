from skyvision import *
from SkyVision_Tools import *
from flask import *
import cv2

    # camera = cv2.VideoCapture('http://192.168.1.4:4747/mjpegfeed')

sky_operations = {
    "Image Input" : operation("Image input",OperationType.INPUT,text_inputs=[operation_TextInput("imgPath","Image Path")]),

    "Webcam Input" : operation("Webcam input",OperationType.INPUT,number_inputs=[operation_NumberInput("webcamID","Webcam ID")]),

    "IP Input" : operation("IP input",OperationType.INPUT,text_inputs=[operation_TextInput("webcamID","Webcam ID")]),

    "Color Mask" : operation("Color Mask",OperationType.COLORS,
        number_inputs=[
            operation_NumberInput("src","Source")],
        color_inputs=[
            operation_ColorInput("lower","Lower"),
            operation_ColorInput("higher","Higher"),
        ]
    ),

    "Convert Color" : operation("Convert color",OperationType.COLORS,
        number_inputs=[
            operation_NumberInput("src","Source")],
        radio_inputs=[
            operation_RadioInput("type","Type",
            options=[
                "BGR2HSV",
                "BGR2RGB",
                "BGR2GRAY",
                "HSV2RGB",
                "HSV2BGR",
                "GRAY2RGB",
            ])
        ]
    ),

    "Bitwise And" : operation("Bitwise AND",OperationType.ARITHMETIC,
        number_inputs=[
            operation_NumberInput("src1","Source One"),
            operation_NumberInput("src1","Source Two"),
            operation_NumberInput("mask","Mask"),
            ],
        
    ),

    "Find Contours" : operation("Find Contours",OperationType.COLORS,
        number_inputs=[
            operation_NumberInput("src","Source"),
            ],
        
    ),

    "Draw Contours" : operation("Draw Contours",OperationType.DRAW,
        number_inputs=[
            operation_NumberInput("src","Source"),
            operation_NumberInput("cnt","Contours"),
            operation_NumberInput("thick","Thickness"),
            ],
        color_inputs=[
            operation_ColorInput("clr","Color"),
            ]
        
    )

}

class sky_operator:
    def __init__(self):
        self.operations = []
        self.frames = []
        self.contours = []
        self.sources = []

    def process(self):
        self.frames.clear()
        self.contours.clear()

        source_counter = 0

        for op in self.operations: # INPUT OPERATIONS
            if op.type == OperationType.INPUT:
                if op.name == "Image input":
                    self.frames.append(cv2.imread(op.textInputs[0].value))
                
                if op.name == "IP input":
                    ret, frame = self.sources[source_counter].read()
                    self.frames.append(frame)
                    source_counter+=1



            if op.type == OperationType.MORPH: # MORPH OPERATIONS
                pass


            if op.type == OperationType.ARITHMETIC: # ARITHMETIC OPERATIONS
                if op.name == "Bitwise AND":
                    src1 = int(op.numberInputs[0].value)
                    src1 = self.frames[src1]

                    src2 = int(op.numberInputs[1].value)
                    src2 = self.frames[src2]

                    maskval = int(op.numberInputs[2].value)
                    mask = self.frames[maskval]

                    if maskval != -1:
                        final = cv2.bitwise_and(src1,src2,mask=mask)
                        self.frames.append(final)
                    else:
                        final = cv2.bitwise_and(src1,src2)
                        self.frames.append(final)



            if op.type == OperationType.COLORS: # COLOR OPERATIONS
                if op.name == "Convert color":
                    src = int(op.numberInputs[0].value)
                    convert_type = op.radioInputs[0].value

                    if convert_type == "BGR2HSV":
                        frame_source = self.frames[src]
                        frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_BGR2HSV)
                        self.frames.append(frame_converted)
                    if convert_type == "BGR2RGB":
                        frame_source = self.frames[src]
                        frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_BGR2RGB)
                        self.frames.append(frame_converted)
                    if convert_type == "BGR2GRAY":
                        frame_source = self.frames[src]
                        frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_BGR2GRAY)
                        self.frames.append(frame_converted)
                    if convert_type == "HSV2RGB":
                        frame_source = self.frames[src]
                        frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_HSV2RGB)
                        self.frames.append(frame_converted)
                    if convert_type == "HSV2RGB":
                        frame_source = self.frames[src]
                        frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_HSV2BGR)
                        self.frames.append(frame_converted)
                    if convert_type == "GRAY2RGB":
                        frame_source = self.frames[src]
                        frame_converted = cv2.cvtColor(frame_source,cv2.COLOR_GRAY2RGB)
                        self.frames.append(frame_converted)

                if op.name == "Color Mask":
                    src = int(op.numberInputs[0].value)
                    src = self.frames[src]

                    lower = hex_to_hsv(op.colorInputs[0].value)
                    lower = np.array([lower[0],lower[1]*255,lower[2]*255])

                    higher = hex_to_hsv(op.colorInputs[1].value)
                    higher = np.array([higher[0],higher[1]*255,higher[2]*255])

                    mask = cv2.inRange(src, lower, higher)
                    self.frames.append(mask)

                if op.name == "Find Contours":
                    src = int(op.numberInputs[0].value)
                    src = self.frames[src]

                    cntrs, _ = cv2.findContours(src,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    self.contours.append(cntrs)


            if op.type == OperationType.DRAW: # DRAW OPERATIONS
                if op.name == "Draw Contours":
                    src = int(op.numberInputs[0].value)
                    src = self.frames[src]

                    cnt = int(op.numberInputs[1].value)
                    cnt = self.contours[cnt]

                    thickness = int(op.numberInputs[2].value)
                    color = hex_to_rgb(request.form[op.colorInputs[0].inName])

                    cv2.drawContours(src,cnt,-1,color,thickness=thickness)
                    


            if op.type == OperationType.MISC: # MISC OPERATIONS
                pass

    def update(self):
        for src in self.sources:
            src.release()
        self.sources.clear()

        for op in self.operations:
            for t_in in op.textInputs:
                t_in.value = request.form[t_in.inName]
            for n_in in op.numberInputs:
                n_in.value = request.form[n_in.inName]
            for r_in in op.radioInputs:
                r_in.value = request.form[r_in.inName]
            for c_in in op.checkboxInputs:
                c_in.value = request.form.getlist(c_in.inName)
            for clr_in in op.colorInputs:
                clr_in.value = request.form[clr_in.inName]

            if op.type == OperationType.INPUT: # INPUT OPERATIONS
                if op.name == "IP input":
                    camera = cv2.VideoCapture(request.form[op.textInputs[0].inName])
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
            
        self.process()