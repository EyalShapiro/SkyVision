from src.skyv_inputs import *
from src.skyv_tools import *
from flask import *
import cv2
import numpy as np
import math
import copy
import time
import re
from enum import Enum
from collections.abc import Callable

import src.skyv_network as skyv_network

error_pic = cv2.imread("res/images/ERR.jpg")  # The frame that will be used for drawing when there is an error

class OperationType(Enum):  # operation type. mostly used for the operation's color
    NONE = 0
    INPUT = 1
    SHAPE = 2
    ARITHMETIC = 3
    COLORS = 4
    DRAW = 5
    MISC = 6
    FlowControl = 7

class operation:
    def __init__(self, name: str, type: OperationType, function: Callable):
        if "MoveUP" in name or "MoveDOWN" in name or "Delete" in name:
            raise Exception("You may not use 'MoveUP/ MoveDOWN/ Delete' in an operation's name.")

        self.name = name
        self.type = type
        self.function = function

        self.inputs = []

    def addInputText(self, name: str, value: str = ""):
        self.inputs.append({"TextInput" : [name,str(value)]})
        return self
    def addInputNumber(self, name: str, value: str = 0, step: float = 0.0001):
        self.inputs.append({"NumberInput" : [name,value,step] })
        return self
    def addInputRadio(self, name: str, value: str = "None", options: list = []):
        # .addInputRadio("Type",value=list(colorModes.keys())[0],options=list(colorModes.keys()))
        if value == "None":
            value: list(options.keys())[0]
        self.inputs.append({"RadioInput" : [name,value,options]})
        return self
    def addInputColor(self, name: str, value: str = 0):
        self.inputs.append({"ColorInput" : [name,value] })
        return self
    def addOutput(self, name: str = "Output"):
        self.inputs.append({"Output" : [name,""] })
        return self
    
    def html(self, operation, operation_id: int = 0, ERR: bool = False, ErrMSG: str = "") -> str:  # return the html version of the operation
        if not ERR:
            retdiv = "<div style=\"margin-top:7px;margin-bottom:7px;background-color:#525252;border-style: solid;border-color:"  # init div
        else:
            retdiv = "<div style=\"margin-top:7px;margin-bottom:7px;background-color:#ff0000;border-style: solid;border-color:"  # init div

        # set div color based on operation type
        div_color = "black"
        div_color = "#00fff7" if self.type == OperationType.INPUT else div_color
        div_color = "#ff9100" if self.type == OperationType.SHAPE else div_color
        div_color = "#11ff00" if self.type == OperationType.ARITHMETIC else div_color
        div_color = "#e100ff" if self.type == OperationType.COLORS else div_color
        div_color = "#ff0000" if self.type == OperationType.DRAW else div_color
        div_color = "#fff200" if self.type == OperationType.MISC else div_color
        div_color = "#0000ff" if self.type == OperationType.FlowControl else div_color

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
                if key == 'ColorInput':
                    retdiv += str(operation_ColorInput(name+str(operation_id)+str(id),text=name,value=value))

                # if key == 'CheckInput':
                #     retdiv += str(check_input)

                

                # if key == 'Output':
                #     retdiv += str(var_output)

        # <- div contents end here
        retdiv += "<br/><label style=\"color: #ff9999\">" + ErrMSG + "</label>"
        retdiv += "</div></div>"  # Close divs
        return retdiv

class operator:
    def __init__(self,verbose):
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
        self.currSave = ""
        self.verbose = verbose

    def process(self):
        level = 0
        true_levels = [0]


        for op in self.operations:
            self.opValues.clear()
            self.opOutputs.clear()
            for input in op["inputs"]:
                for key in input:
                    name = input[key][0]
                    value = str(input[key][1])
                    if "Input" in key:
                        if "Color" in key:
                            value = hex_to_hsv(value)
                        try:
                            if "Text" in key or "Number" in key:
                                match = re.search('&[a-zA-Z]+',value)
                                if(match is not None):
                                    string = str(value[:match.start()] + 'self.values[\'' + match.group()[1:] + '\']'  + value[match.end():])
                                    try:
                                        value = eval(string)
                                    except Exception as e:
                                        pass
                                else:
                                    value = eval(value)
                        except Exception as e:
                            value = input[key][1]
                            if(self.verbose):
                                # logMessage("Cant parse value \"" + str(value)[1:] + "\"")
                                pass

                        self.opValues[name] = value
                    elif "Output" in key:
                        self.opOutputs.append(value)
            
            if self.getOperationSource(op).name == "IF":
                level += 1
                if self.getOperationSource(op).function(self.opValues,self)[0]:
                    true_levels.append(level)
            elif self.getOperationSource(op).name == "ENDIF":
                if level in true_levels:
                    true_levels.remove(level)
                level -= 1
                

            if(level in true_levels):
                try:
                    op["ERR"]=False
                    op["ERRMSG"]=""
                    operation_outputs = self.getOperationSource(op).function(self.opValues,self)
                    if operation_outputs is not None:
                        self.values.update(dict(zip(self.opOutputs,operation_outputs)))
                except Exception as error:
                    op["ERR"]=True
                    op["ERRMSG"]=str(error)
                    if(self.verbose):
                        print("\n" + tColors.FAIL + getTime() + "OPERATION ERROR [" + op["name"][5:] + "]\n" + str(error) + tColors.ENDC)
        try:  # try to set the output frame to the required frame
            self.outputVideo = self.values[self.required_out]  # set the output to the required frame
            self.outputVideo = cv2.resize(self.outputVideo,(int(self.outputVideo.shape[1] * self.outResolution),int(self.outputVideo.shape[0] * self.outResolution)))
        except:  # if setting output frame fails, set it to the error pic
            self.outputVideo = cv2.resize(error_pic,(int(error_pic.shape[1] * 0.25),int(error_pic.shape[0] * 0.25)))  # set the output frame to the error pic

    def update(self, fromUpdate = True):
        if(self.currSave != ""):
            self.updating = True
            if fromUpdate:
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
                            try:
                                value = request.form[name+str(op_id)+str(id)]
                                tmp_operations[op_id]["inputs"][input_id][key][1] = value
                            except:
                                if(self.verbose):
                                    print(tColors.FAIL + getTime() + "UNABLE TO GET VALUE " + name+str(op_id)+str(id) + ".")
                
            self.operations = copy.deepcopy(tmp_operations) # update operations to duplicate
            del tmp_operations
            time.sleep(3)
            self.process()
            self.getOutputOptions()
            self.updating = False
        else:
            if(self.verbose):
                print(tColors.FAIL + getTime() + "UNABLE TO UPDATE, PLEASE LOAD FILE.")
        
    def loadOperation(self, op):
        self.loaded_operations[op.name] = op
        return
    
    def loadOperationArray(self, ops):
        for op in ops:
            self.loadOperation(op)
        # self.update(True)

    def addOperation(self, op_name):
        if op_name in self.loaded_operations:
            self.operations.append({'name'  : str(format((len(self.operations) + 1),'05d')) + op_name,
                                    "inputs" : self.loaded_operations[op_name].inputs,
                                    "type" : self.loaded_operations[op_name].type.value})
        else:
            if(self.verbose):
                print(tColors.FAIL+getTime()+"Unable to add operation \"" + op_name + "\""+tColors.ENDC )

    def removeOperation(self, op_id):
        self.operations.pop(op_id)

    def moveOperation(self, op_id, direction):
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
            try:
                htmls.append(self.getOperationSource(op).html(op,id,op["ERR"],op["ERRMSG"]))
            except:
                htmls.append(self.getOperationSource(op).html(op,id))
        return htmls

    def generateVideo(self):  # generates the output frame
        time.sleep(1)  # delay to allow for camera reconnection
        while True:
            ret, encodedImage = cv2.imencode(".jpg", self.outputVideo)  # turn the output pic to a jpg
            if ret:  # if encoding to jpg fails, skip this frame
                self.outputVid = (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
                yield self.outputVid  # output the frame in a format that the browser can read