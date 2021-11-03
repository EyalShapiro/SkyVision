from src.html_inputs import *
from flask import *
from random import randint


class OperationType:  # operation type . mostly for the operation's color
    NONE = 0
    INPUT = 1
    MORPH = 2
    ARITHMETIC = 3
    COLORS = 4
    DRAW = 5
    MISC = 6

class operation_TextInput:  # text input for operation
    def __init__(self, name, text="", style="color: #ebebeb;background-color:#525252;",
                 text_style="font-size:28px;margin-right:10px;color:#ebebeb;", value="", brake=True):
        self.name = "name=\"" + name + "\""
        self.inName = name

        self.text = text
        self.style = style
        self.txtStyle = text_style
        self.br = brake
        self.value = value

    def conv_dict(self):
        ret_dict = {
            "name": self.inName,

            "text": self.text,
            "style": self.style,
            "textStyle": self.txtStyle,
            "brake": self.br,
            "value": request.form[self.inName]
        }
        return ret_dict

    def __str__(self):
        return html_input(self.text, "text", self.name, self.style, self.txtStyle, value=self.value,
                          brake=self.br)  # return the html version of the input

class operation_NumberInput:  # number input for operation ( like text but can only get numbers )
    def __init__(self, name, text="", style="color: #ebebeb;background-color:#525252;",
                 text_style="font-size:28px;margin-right:10px;color:#ebebeb;", value="", brake=True):
        self.name = "name=\"" + name + "\""
        self.inName = name

        self.text = text
        self.style = style
        self.txtStyle = text_style
        self.br = brake
        self.value = value

    def conv_dict(self):
        ret_dict = {
            "name": self.inName,

            "text": self.text,
            "style": self.style,
            "textStyle": self.txtStyle,
            "brake": self.br,
            "value": request.form[self.inName]
        }
        return ret_dict

    def __str__(self):
        return html_input(self.text, "number", self.name, self.style, self.txtStyle, self.value,
                          brake=self.br)  # return the html version of the input

class operation_RadioInput:  # radio input for operation ( select one of options )
    def __init__(self, name, text="", options=[], radio_style="margin-left:12px;",
                 header_style="font-size:28px;color:#ebebeb;", option_text_style="font-size:18px;color:#ebebeb;",
                 value="", vertical=False, brake=True):
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
            "name": self.inName,

            "text": self.text,
            "options": self.options,
            "style": self.style,
            "textStyle": self.txtStyle,
            "optionTextStyle": self.optnTxtStyle,
            "direction": self.direction,
            "brake": self.brake,
            "value": request.form[self.inName]
        }
        return ret_dict

    def __str__(self):
        retstr = html_header(self.text + ": ", size=3, brake=self.direction,
                             style=self.txtStyle)  # return the html version of the input
        for option in self.options:
            if option != self.value:
                retstr = retstr + html_radio(self.name, option, style=self.style, text_style=self.txtStyle,
                                             option_style=self.optnTxtStyle, brake=self.direction)
            else:
                retstr = retstr + html_selectedradio(self.name, option, style=self.style, text_style=self.txtStyle,
                                                     option_style=self.optnTxtStyle, brake=self.direction)
        retstr = retstr + ("<br/>" if self.brake else "")
        return retstr

class operation_CheckboxInput:  # checkbox input for operation ( select multiple from options )
    def __init__(self, name, text="", options=[], radio_style="margin-left:12px;",
                 header_style="font-size:28px;color:#ebebeb;", option_text_style="font-size:18px;color:#ebebeb;",
                 value="", vertical=False, brake=True):
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
            "name": self.inName,

            "text": self.text,
            "options": self.options,
            "style": self.style,
            "textStyle": self.txtStyle,
            "optionTextStyle": self.optnTxtStyle,
            "direction": self.direction,
            "brake": self.brake,
            "value": request.form.getlist(self.inName)
        }
        return ret_dict

    def __str__(self):  # return the html version of the input
        retstr = html_header(self.text + ": ", size=3, brake=self.direction, style=self.txtStyle)
        for option in self.options:
            selected = False
            for val in self.value:
                if option == val:
                    retstr = retstr + html_selectedcheckbox(self.name, option, style=self.style,
                                                            text_style=self.txtStyle, option_style=self.optnTxtStyle,
                                                            brake=self.direction)
                    selected = True
                    break
            if not selected:
                retstr = retstr + html_checkbox(self.name, option, style=self.style, text_style=self.txtStyle,
                                                option_style=self.optnTxtStyle, brake=self.direction)
        retstr = retstr + ("<br/>" if self.brake else "")
        return retstr

class operation_ColorInput:  # color input for operation
    def __init__(self, name, text="", style="", text_style="font-size:28px;margin-right:10px;color:#ebebeb;",
                 value="#00FF00", brake=True):
        self.name = "name=\"" + name + "\""
        self.inName = name

        self.text = text
        self.style = style
        self.txtStyle = text_style
        self.br = brake
        self.value = value

    def conv_dict(self):
        ret_dict = {
            "name": self.inName,

            "text": self.text,
            "style": self.style,
            "textStyle": self.txtStyle,
            "brake": self.br,
            "value": request.form[self.inName]
        }
        return ret_dict

    def __str__(self):  # return the html version of the input
        return html_color(self.name, self.value, self.text, self.style, self.txtStyle, brake=self.br, )
