from htmlcontrol import *

class OperationType():
    NONE = 0
    INPUT = 1
    MORPH = 2
    BITWISE = 3
    CONTOURS = 4
    DRAW = 5
    MISC = 6

class operation_TextInput: # text input for operation
    def __init__(self, name, text = "",style = "",text_style = "font-size:28px;margin-right:10px;",brake=True):
        self.name = "name=\"" + name + "\""
        self.text = text
        self.style = style
        self.txtStyle = text_style
        self.br = brake

    def __str__(self):
        return html_input(self.text,"text",self.name,self.style,self.txtStyle,brake=self.br)

class operation_NumberInput: # text input for operation
    def __init__(self, name, text = "",style = "",text_style = "font-size:28px;margin-right:10px;",brake=True):
        self.name = "name=\"" + name + "\""
        self.text = text
        self.style = style
        self.txtStyle = text_style
        self.br = brake

    def __str__(self):
        return html_input(self.text,"number",self.name,self.style,self.txtStyle,brake=self.br)

class operation_RadioInput: # text input for operation
    def __init__(self, name,text = "", options = [],radio_style = "margin-left:12px;",header_style = "font-size:28px;",option_text_style="font-size:18px;",vertical=False,brake=True):
        self.name = "name=\"" + name + "\""
        self.text = text
        self.options = options
        self.style = radio_style 
        self.txtStyle = header_style
        self.optnTxtStyle = option_text_style
        self.direction = vertical
        self.brake = brake

    def __str__(self):
        retstr = html_header(self.text+": ",size=3,brake=self.direction,style=self.txtStyle)
        for option in self.options:
            retstr = retstr + html_radio(self.name,option,style=self.style,text_style=self.txtStyle,option_style=self.optnTxtStyle,brake=self.direction)
        retstr = retstr + ("<br/>" if self.brake else "")
        return retstr

class operation_CheckboxInput: # text input for operation
    def __init__(self, name,text = "", options = [],radio_style = "margin-left:12px;",header_style = "font-size:28px;",option_text_style="font-size:18px;",vertical=False,brake=True):
        self.name = "name=\"" + name + "\""
        self.text = text
        self.options = options
        self.style = radio_style 
        self.txtStyle = header_style
        self.optnTxtStyle = option_text_style
        self.direction = vertical
        self.brake = brake

    def __str__(self):
        retstr = html_header(self.text+": ",size=3,brake=self.direction,style=self.txtStyle)
        for option in self.options:
            retstr = retstr + html_checkbox(self.name,option,style=self.style,text_style=self.txtStyle,option_style=self.optnTxtStyle,brake=self.direction)
        retstr = retstr + ("<br/>" if self.brake else "")
        return retstr

class operation_ColorInput: # text input for operation
    def __init__(self, name, text = "",style = "",text_style = "font-size:28px;margin-right:10px;",brake=True):
        self.name = "name=\"" + name + "\""
        self.text = text
        self.style = style
        self.txtStyle = text_style
        self.br = brake

    def __str__(self):
        return html_color(self.name,"#00FF00",self.text,self.style,self.txtStyle,brake=self.br)

class operation: # main class for operation
    def __init__(self, name, operation_Type,text_inputs = [],radio_inputs = [],checkbox_inputs = []):
        self.name = name
        self.type = operation_Type

        self.textInputs = text_inputs
        self.radioInputs = radio_inputs
        self.checkboxInputs = checkbox_inputs

    def __str__(self):

        retdiv = "<div style=\"margin-top:7px;margin-bottom:7px;background-color:" # init div

        # set div color based on operation type
        div_color = "black"
        div_color = "#00fff7" if self.type == OperationType.INPUT else div_color 
        div_color = "#ff9100" if self.type == OperationType.MORPH else div_color
        div_color = "#11ff00" if self.type == OperationType.BITWISE else div_color
        div_color = "#e100ff" if self.type == OperationType.CONTOURS else div_color
        div_color = "#ff0000" if self.type == OperationType.DRAW else div_color
        div_color = "#fff200" if self.type == OperationType.MISC else div_color

        retdiv += div_color # add div color
        retdiv += ";border-radius: 25px;\">" # end div init

        retdiv += "<div style=\"padding-left:25px;padding-right:25px;padding-up:25px;padding-down:25px;display:inline-block;\">" # add inner div

        # div contents here ->
        retdiv += html_header(self.name) # div Title

        for text_input in self.textInputs:
            retdiv += str(text_input)

        for radio_input in self.radioInputs:
            retdiv += str(radio_input)

        for check_input in self.checkboxInputs:
            retdiv += str(check_input)

        # <- div contents end here
        retdiv += "</div></div>" # Close divs

        return retdiv