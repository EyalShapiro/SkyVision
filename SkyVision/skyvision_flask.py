from flask import *
import json
import cv2
import time

from skyvision import *
from SkyVision_Tools import *
from skyvision_operations import *

import copy

app = Flask(__name__) # app
app.secret_key = "#4416"

operator = sky_operator()
outputs = []
required_out = "None"

error_pic = cv2.imread("ERR.jpg")

def generate():
    time.sleep(3)
    while(True):
        operator.process()
        outputs = operator.values
        
        try:
            selected_out = outputs[required_out]
        except:
            selected_out = error_pic

        ret, encodedImage = cv2.imencode(".jpg", selected_out)
        if not ret:
            continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(),mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/",methods=['GET', 'POST'])
def home(): # home page
    global required_out
    if request.method == "GET":
        try:
            required_out = "None"
            with open('session.json') as json_file:
                operator.operations.clear()
                data = json.load(json_file)
                temp_operations = data["operations"]
                counter = 0
                for op in temp_operations:
                    counter+=1
                    textinputs = []
                    for temp_input in op["text_in"]:
                        textinputs.append(operation_TextInput(temp_input["name"],temp_input["text"],temp_input["style"],temp_input["textStyle"],temp_input["value"],temp_input["brake"]))

                    numinputs = []
                    for temp_input in op["number_in"]:
                        numinputs.append(operation_NumberInput(temp_input["name"],temp_input["text"],temp_input["style"],temp_input["textStyle"],temp_input["value"],temp_input["brake"]))
                    
                    radinputs = []
                    for temp_input in op["radio_in"]:
                        radinputs.append(operation_RadioInput(temp_input["name"],temp_input["text"],temp_input["options"],temp_input["style"],temp_input["textStyle"],temp_input["optionTextStyle"],temp_input["value"],temp_input["direction"],temp_input["brake"]))

                    checkinputs = []
                    for temp_input in op["check_in"]:
                        checkinputs.append(operation_CheckboxInput(temp_input["name"],temp_input["text"],temp_input["options"],temp_input["style"],temp_input["textStyle"],temp_input["optionTextStyle"],temp_input["value"],temp_input["direction"],temp_input["brake"]))

                    colorinputs = []
                    for temp_input in op["color_in"]:
                        colorinputs.append(operation_ColorInput(temp_input["name"],temp_input["text"],temp_input["style"],temp_input["textStyle"],temp_input["value"],temp_input["brake"]))

                    varOutputs = []
                    for temp_output in op["var_out"]:
                        varOutputs.append(operation_TextInput(temp_output["name"],temp_output["text"],temp_output["style"],temp_output["textStyle"],temp_output["value"],temp_output["brake"]))


                    operator.operations.append(operation(op["name"],op["type"],text_inputs=textinputs,number_inputs=numinputs,radio_inputs=radinputs,checkbox_inputs=checkinputs,color_inputs=colorinputs,variable_outputs=varOutputs))
            pass
        except:
            pass
            # save_session()

        session.permanent = True
        return render_template("mainhtml.html",ops = operator.operations,curr_out = required_out)
    elif request.method == "POST":
        try:
            if request.form["action"] == "Save":
                save_session()
                operator.update()
                save_session()
            elif request.form["action"] == "Update":
                required_out = request.form["outID"]
                print("Req Out is",required_out)
                operator.update()
            else:
                value = request.form["action"]
                add_operation(value)
                
        except:
            pass

        return render_template("mainhtml.html",ops = operator.operations,curr_out = required_out)

def add_operation(operation_name):
    operator.update()
    new_op = copy.deepcopy(sky_operations[request.form["action"]])
    new_op.add_num(operator.inCounter)
    operator.operations.append(new_op)
    


def save_session():
    print("Saving Session")
    operations_dict = []
    for op in operator.operations:
        operations_dict.append(op.conv_dict())
        
    session["operations"] = operations_dict

    r = jsonify(dict(session))
    with open("session.json", "w") as file:
        file.write(r.get_data(as_text=True))
        file.close()
        print("Saved Session")


if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0')