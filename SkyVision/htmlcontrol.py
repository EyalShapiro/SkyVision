#code which turns operations to html
def html_header(text,style = "",size = 1,brake = True): # make a html <h>
    return "<h" + str(size) + " style=\"" + style + "display:inline-block;\">" + text + "</h" + str(size) + ">" + ("<br/>" if brake else "")

def html_paragraph(text,style = "",brake = True): # make a html <p>
    return "<p style=\"" + style + "display:inline-block;\">" + text + "</p>" + ("<br/>" if brake else "")

def html_input(text,input_type,name,style = "",text_style="",value="",brake = True): # make a html <input>
    return "<h3 style=\"" + text_style + "display:inline-block;\">" + text + ": </h3><input type=\"" + input_type + "\" " + name + " style=\"" + style + "display:inline-block;\"" + "value=\""+ value + "\"" + "step=\"0.0001\"></input>" + ("<br/>" if brake else "")

def html_radio(name,value,style = "",text_style="",option_style="",brake = True): # make a html <input type="radio">
    return "<input type=\"radio\"" + name + " style=\"" + style + "display:inline-block;\" value=\"" + value + "\"><label style=\"" + option_style + "\">" + value + "</label> </input>" + ("<br/>" if brake else "")

def html_selectedradio(name,value,style = "",text_style="",option_style="",brake = True): # make a html <input type="radio">
    return "<input type=\"radio\"" + name + " style=\"" + style + "display:inline-block;\" value=\"" + value + "\" checked><label style=\"" + option_style + "\">" + value + "</label> </input>" + ("<br/>" if brake else "")

def html_checkbox(name,value,style = "",text_style="",option_style="",brake = True): # make a html <input type="checkbox">
    return "<input type=\"checkbox\"" + name + " style=\"" + style + "display:inline-block;\" value=\"" + value + "\"><label style=\"" + option_style + "\">" + value + "</label> </input>" + ("<br/>" if brake else "")

def html_selectedcheckbox(name,value,style = "",text_style="",option_style="",brake = True): # make a html <input type="checkbox">
    return "<input type=\"checkbox\"" + name + " style=\"" + style + "display:inline-block;\" value=\"" + value + "\" checked><label style=\"" + option_style + "\">" + value + "</label> </input>" + ("<br/>" if brake else "")

def html_color(name,color,value,style = "",text_style="",brake = True): # make a html <input type="color">
    return "<label style=\"" + text_style + "\">" + value + "</label> <input type=\"color\"" + name + " style=\"" + style + "display:inline-block;\" value=\"" + color + "\"></input>" + ("<br/>" if brake else "")