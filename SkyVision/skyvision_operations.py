from skyvision import *
from SkyVision_Tools import *
from flask import *
import cv2

sky_operations = {
    #{key: Image input ; value: object(operation)}
    
    "Image Input" : operation("Image input",OperationType.INPUT,text_inputs=[operation_TextInput("imgPath","Image Path")],variable_outputs=[operation_TextInput("outName","Output name")]),
    
    "Webcam Input" : operation("Webcam input",OperationType.INPUT,number_inputs=[operation_NumberInput("webcamID","Webcam ID")],variable_outputs=[operation_TextInput("outName","Output name")]),

    "IP Input" : operation("IP input",OperationType.INPUT,text_inputs=[operation_TextInput("webcamID","Webcam ID")],variable_outputs=[operation_TextInput("outName","Output name")]),

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
    )

}

class sky_operator:
    def __init__(self):
        self.operations = [] #array of blocks (operations)
        self.sources = [] #array of cameras 
        self.inCounter = 0 #differ between inputs
        self.values = {} #dictionary of all values

    def process(self):
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


                if op.type == OperationType.DRAW: # DRAW OPERATIONS
                    if op.name == "Draw Contours":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        cnt = op.textInputs[1].value
                        cnt = self.values[cnt]

                        thickness = int(op.numberInputs[0].value)
                        color = hex_to_rgb(op.colorInputs[0].value)
                        cv2.drawContours(src,cnt,-1,color,thickness=thickness)

                    if op.name == "Draw Circle":
                        src = op.textInputs[0].value
                        src = self.values[src]

                        radius = int(op.numberInputs[0].value)

                        x = int(op.numberInputs[1].value)
                        y = int(op.numberInputs[2].value)

                        thickness = int(op.numberInputs[3].value)


                        color = hex_to_hsv(op.colorInputs[0].value)

                        cv2.circle(src,(x,y), radius, color, thickness)

                    if op.name == "Text":
                        src = op.textInputs[0].value
                        src = self.values[src]
                    


                if op.type == OperationType.MISC: # MISC OPERATIONS
                    pass
            except:
                pass

    def MoveUP(self,num):
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

    def MoveDOWN(self,num):
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

    def Delete(self,num):
        for op in self.operations:
            if int(op.op_move_counter) == int(num):
                self.operations.remove(op)
                print("Removed")
                self.inCounter -= 1
                break

        
        self.update()

    def update(self):
        self.inCounter = len(self.values.values())

        print("UPDATING")

        self.sources.clear()

        for op in self.operations:
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