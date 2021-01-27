from skyvision import *
from SkyVision_Tools import *
from flask import *
import cv2

sky_operations = {
    "Image Input" : operation("Image input",OperationType.INPUT,
        text_inputs=[operation_TextInput("imgPath","Image Path")],
        # number_inputs=[operation_NumberInput("imgNath","Image Nath")],
        # radio_inputs=[operation_RadioInput("imgZath","Image Zath",["One","Two","Three"])],
        # checkbox_inputs=[operation_CheckboxInput("imgKath","Image Kath",["One","Two","Three","Four"])],
        # color_inputs=[operation_ColorInput("imgDath","Image Dath")]
    ),
    # "Webcam Input" : operation("Webcam input",OperationType.INPUT,number_inputs=[operation_NumberInput("webcamID","Webcam ID")]),

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
        
    )
}

class sky_operator:
    def __init__(self):
        self.operations = []
        self.frames = []
        self.live = True

    def update(self):
        self.frames.clear()

        # to get value use request.form[operation.value_type[index].inName]
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

            if op.type == OperationType.INPUT:
                print("Input Operation Name -",op.name)
                if op.name == "Image input":
                    self.frames.append(cv2.imread(request.form[op.textInputs[0].inName]))



            if op.type == OperationType.MORPH:
                print("Morph Operation Name -",op.name)



            if op.type == OperationType.ARITHMETIC:
                print("Arithmetic Operation Name -",op.name)
                if op.name == "Bitwise AND":
                    src1 = int(request.form[op.numberInputs[0].inName])
                    src1 = self.frames[src1]

                    src2 = int(request.form[op.numberInputs[1].inName])
                    src2 = self.frames[src2]

                    mask = int(request.form[op.numberInputs[2].inName])
                    mask = self.frames[mask]

                    final = cv2.bitwise_and(src1,src2,mask=mask)
                    self.frames.append(final)



            if op.type == OperationType.COLORS:
                print("Color Operation Name -",op.name)
                if op.name == "Convert color":
                    src = int(request.form[op.numberInputs[0].inName])
                    convert_type = request.form[op.radioInputs[0].inName]

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
                    src = int(request.form[op.numberInputs[0].inName])
                    src = self.frames[src]

                    lower = hex_to_hsv(request.form[op.colorInputs[0].inName])
                    lower = np.array([lower[0],lower[1]*255,lower[2]*255])

                    higher = hex_to_hsv(request.form[op.colorInputs[1].inName])
                    higher = np.array([higher[0],higher[1]*255,higher[2]*255])

                    mask = cv2.inRange(src, lower, higher)
                    self.frames.append(mask)



            if op.type == OperationType.DRAW:
                print("Draw Operation Name -",op.name)



            if op.type == OperationType.MISC:
                print("Misc Operation Name -",op.name)
