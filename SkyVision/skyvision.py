from htmlcontrol import *
from flask import *

class OperationType():
    NONE = 0
    INPUT = 1
    MORPH = 2
    ARITHMETIC = 3
    COLORS = 4
    DRAW = 5
    MISC = 6

class operation_TextInput: # text input for operation
    def __init__(self, name, text = "",style = "",text_style = "font-size:28px;margin-right:10px;",value="",brake=True):
        self.name = "name=\"" + name + "\""
        self.inName = name

        self.text = text
        self.style = style
        self.txtStyle = text_style
        self.br = brake
        self.value = value

    def conv_dict(self):
        ret_dict = {
            "name" : self.inName,

            "text" : self.text,
            "style" : self.style,
            "textStyle" : self.txtStyle,
            "brake" : self.br,
            "value" : request.form[self.inName]
        }
        return ret_dict

    def __str__(self):
        return html_input(self.text,"text",self.name,self.style,self.txtStyle,value=self.value,brake=self.br)

class operation_NumberInput: # text input for operation
    def __init__(self, name, text = "",style = "",text_style = "font-size:28px;margin-right:10px;",value="",brake=True):
        self.name = "name=\"" + name + "\""
        self.inName = name

        self.text = text
        self.style = style
        self.txtStyle = text_style
        self.br = brake
        self.value = value

    def conv_dict(self):
        ret_dict = {
            "name" : self.inName,

            "text" : self.text,
            "style" : self.style,
            "textStyle" : self.txtStyle,
            "brake" : self.br,
            "value" : request.form[self.inName]
        }
        return ret_dict

    def __str__(self):
        return html_input(self.text,"number",self.name,self.style,self.txtStyle,self.value,brake=self.br)

class operation_RadioInput: # text input for operation
    def __init__(self, name,text = "", options = [],radio_style = "margin-left:12px;",header_style = "font-size:28px;",option_text_style="font-size:18px;",value="",vertical=False,brake=True):
        self.name = "name=\"" + name + "\""
        self.inName = name

        self.text = text
        self.options = options
        self.style = radio_style 
        self.txtStyle = header_style
        self.optnTxtStyle = option_text_style
        self.direction = vertical
        self.brake = brake
        self.value = value

    def conv_dict(self):
        ret_dict = {
            "name" : self.inName,

            "text" : self.text,
            "options" : self.options,
            "style" : self.style,
            "textStyle" : self.txtStyle,
            "optionTextStyle" : self.optnTxtStyle,
            "direction" : self.direction,
            "brake" : self.brake,
            "value" : request.form[self.inName]
        }
        return ret_dict

    def __str__(self):
        retstr = html_header(self.text+": ",size=3,brake=self.direction,style=self.txtStyle)
        for option in self.options:
            if option != self.value:
                retstr = retstr + html_radio(self.name,option,style=self.style,text_style=self.txtStyle,option_style=self.optnTxtStyle,brake=self.direction)
            else:
                retstr = retstr + html_selectedradio(self.name,option,style=self.style,text_style=self.txtStyle,option_style=self.optnTxtStyle,brake=self.direction)
        retstr = retstr + ("<br/>" if self.brake else "")
        return retstr

class operation_CheckboxInput: # text input for operation
    def __init__(self, name,text = "", options = [],radio_style = "margin-left:12px;",header_style = "font-size:28px;",option_text_style="font-size:18px;",value = "",vertical=False,brake=True):
        self.name = "name=\"" + name + "\""
        self.inName = name

        self.text = text
        self.options = options
        self.style = radio_style 
        self.txtStyle = header_style
        self.optnTxtStyle = option_text_style
        self.direction = vertical
        self.brake = brake
        self.value = value

    def conv_dict(self):
        ret_dict = {
            "name" : self.inName,

            "text" : self.text,
            "options" : self.options,
            "style" : self.style,
            "textStyle" : self.txtStyle,
            "optionTextStyle" : self.optnTxtStyle,
            "direction" : self.direction,
            "brake" : self.brake,
            "value" : request.form.getlist(self.inName)
        }
        return ret_dict

    def __str__(self):
        retstr = html_header(self.text+": ",size=3,brake=self.direction,style=self.txtStyle)
        for option in self.options:
            selected = False
            for val in self.value:
                if option == val:
                    retstr = retstr + html_selectedcheckbox(self.name,option,style=self.style,text_style=self.txtStyle,option_style=self.optnTxtStyle,brake=self.direction)
                    selected = True
                    break
            if not selected:
                retstr = retstr + html_checkbox(self.name,option,style=self.style,text_style=self.txtStyle,option_style=self.optnTxtStyle,brake=self.direction)
        retstr = retstr + ("<br/>" if self.brake else "")
        return retstr

class operation_ColorInput: # text input for operation
    def __init__(self, name, text = "",style = "",text_style = "font-size:28px;margin-right:10px;",value="#00FF00",brake=True):
        self.name = "name=\"" + name + "\""
        self.inName = name

        self.text = text
        self.style = style
        self.txtStyle = text_style
        self.br = brake
        self.value = value

    def conv_dict(self):
        ret_dict = {
            "name" : self.inName,

            "text" : self.text,
            "style" : self.style,
            "textStyle" : self.txtStyle,
            "brake" : self.br,
            "value" : request.form[self.inName]
        }
        return ret_dict

    def __str__(self):
        return html_color(self.name,self.value,self.text,self.style,self.txtStyle,brake=self.br,)

class operation: # main class for operation
    def __init__(self, name, operation_Type,text_inputs = [],number_inputs = [],radio_inputs = [],checkbox_inputs = [],color_inputs = []):
        self.name = name
        self.type = operation_Type

        self.textInputs = text_inputs
        self.numberInputs = number_inputs
        self.radioInputs = radio_inputs
        self.checkboxInputs = checkbox_inputs
        self.colorInputs = color_inputs

        #op_input.name = "name=\"" + op_input.inName + str(value) + "\""
    def add_num(self,num):
        counter = 0
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
        

    def conv_dict(self):

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

        ret_dict = {
            "name" : self.name,
            "type" : self.type,
            "text_in" : text_in_dict,
            "number_in" : number_in_dict,
            "radio_in" : radio_in_dict,
            "check_in" : checkbox_in_dict,
            "color_in" : color_in_dict,
        }


        return ret_dict

    def __str__(self):

        retdiv = "<div style=\"margin-top:7px;margin-bottom:7px;background-color:" # init div

        # set div color based on operation type
        div_color = "black"
        div_color = "#00fff7" if self.type == OperationType.INPUT else div_color 
        div_color = "#ff9100" if self.type == OperationType.MORPH else div_color
        div_color = "#11ff00" if self.type == OperationType.ARITHMETIC else div_color
        div_color = "#e100ff" if self.type == OperationType.COLORS else div_color
        div_color = "#ff0000" if self.type == OperationType.DRAW else div_color
        div_color = "#fff200" if self.type == OperationType.MISC else div_color

        retdiv += div_color # add div color
        retdiv += ";border-radius: 25px;\">" # end div init

        retdiv += "<div style=\"padding-left:25px;padding-right:25px;padding-up:25px;padding-down:25px;display:inline-block;\">" # add inner div

        # div contents here ->
        retdiv += html_header(self.name) # div Title

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

        # <- div contents end here
        retdiv += "</div></div>" # Close divs

        return retdiv