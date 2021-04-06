from flask import *
import json
import cv2
import time

from skyvision import *
from SkyVision_Tools import *
from skyvision_operations import *

import copy # the most underrated library

app = Flask(__name__) # app
app.secret_key = "#4416" # secret key used for session saving

operator = sky_operator() # main class responsible for organizing and activating operations
required_out = "None" # Current frame that will be drawn on screen

error_pic = cv2.imread("ERR.jpg") # The frame that will be used for drawing when there is an error

windowMode = False

def generate(): # generates the output frame
    # cv2.destroyAllWindows()
    time.sleep(3) # delay to allow for camera reconnection
    while(True):
        operator.process() # activate all operations
        outputs = operator.values # get all values from the operator
        
        try: # try to set the output frame to the required frame
            selected_out = outputs[required_out] # set the output to the required frame
        except: # if setting output frame fales, set it to the error pic
            selected_out = error_pic # set the output frame to the error pic
        
        if selected_out is None:
            selected_out = error_pic

        ret, encodedImage = cv2.imencode(".jpg", selected_out) # turn the output pic to a jpg

        if ret: # if encoding to jpg fails, skip this frame
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n') # output the frame in a format that the browser can read

def generateWindow(): # generates the output frame
    global windowMode
    cv2.destroyAllWindows()
    time.sleep(5) # delay to allow for camera reconnection
    while(windowMode):
        operator.process() # activate all operations
        outputs = operator.values # get all values from the operator
        
        try: # try to set the output frame to the required frame
            selected_out = outputs[required_out] # set the output to the required frame
        except: # if setting output frame fales, set it to the error pic
            selected_out = error_pic # set the output frame to the error pic
        
        if selected_out is None:
            selected_out = error_pic

        cv2.imshow('SkyVision',selected_out)
        if cv2.waitKey(1) == ord('q'):
            windowMode = False



        
@app.route("/video_feed") # the route for only the video feed
def video_feed():
    global windowMode
    if windowMode:
        generateWindow()
        return Response(generate(),mimetype = "multipart/x-mixed-replace; boundary=frame") # return the output from the generate() function
    else:
        return Response(generate(),mimetype = "multipart/x-mixed-replace; boundary=frame") # return the output from the generate() function
    

@app.route("/",methods=['GET', 'POST']) # route for main page, allows for GET and POST requests
def home(): # home page
    global required_out
    #cv2.destroyAllWindows()
    if request.method == "GET": # if entered page regularly
        try:
            required_out = "None" # set the required output frame to "None"
            with open('session.json') as json_file: # open the saved file
                operator.operations.clear() # clear all loaded operations
                data = json.load(json_file) # get the json data
                temp_operations = data["operations"] # load operations from the json file

                counter = 0
                cc = 0
                for op in temp_operations: # for operation in loaded operations
                    
                    textinputs = [] # all text inputs in the loaded operation
                    for temp_input in op["text_in"]:
                        textinputs.append(operation_TextInput(temp_input["name"],temp_input["text"],temp_input["style"],temp_input["textStyle"],temp_input["value"],temp_input["brake"])) # create a operation_TextInput from loaded data
                        counter+=1

                    numinputs = [] # all number inputs in the loaded operation
                    for temp_input in op["number_in"]:
                        numinputs.append(operation_NumberInput(temp_input["name"],temp_input["text"],temp_input["style"],temp_input["textStyle"],temp_input["value"],temp_input["brake"])) # create a operation_NumberInput from loaded data
                        counter+=1
                    
                    radinputs = [] # all radio inputs in the loaded operation
                    for temp_input in op["radio_in"]:
                        radinputs.append(operation_RadioInput(temp_input["name"],temp_input["text"],temp_input["options"],temp_input["style"],temp_input["textStyle"],temp_input["optionTextStyle"],temp_input["value"],temp_input["direction"],temp_input["brake"])) # create a operation_RadioInput from loaded data
                        counter+=1

                    checkinputs = [] # all checkbox inputs in the loaded operation
                    for temp_input in op["check_in"]:
                        checkinputs.append(operation_CheckboxInput(temp_input["name"],temp_input["text"],temp_input["options"],temp_input["style"],temp_input["textStyle"],temp_input["optionTextStyle"],temp_input["value"],temp_input["direction"],temp_input["brake"])) # create a operation_CheckboxInput from loaded data
                        counter+=1

                    colorinputs = [] # all color inputs in the loaded operation
                    for temp_input in op["color_in"]:
                        colorinputs.append(operation_ColorInput(temp_input["name"],temp_input["text"],temp_input["style"],temp_input["textStyle"],temp_input["value"],temp_input["brake"])) # create a operation_ColorInput from loaded data
                        counter+=1

                    varOutputs = [] # all variable Outputs in the loaded operation
                    for temp_output in op["var_out"]:
                        varOutputs.append(operation_TextInput(temp_output["name"],temp_output["text"],temp_output["style"],temp_output["textStyle"],temp_output["value"],temp_output["brake"])) # create a operation_TextInput from loaded data
                        counter+=1

                    op = operation(op["name"],op["type"],text_inputs=textinputs,number_inputs=numinputs,radio_inputs=radinputs,checkbox_inputs=checkinputs,color_inputs=colorinputs,variable_outputs=varOutputs)
                    op.add_num(cc) # add num is used to differentiate each input from another
                    cc += 1
                    operator.inCounter += 1
                    operator.operations.append(op) # create an operation from all created inputs
            pass
        except:
            print("Unable to located \"Session.json\"") # print error if failed to open session.json

        session.permanent = True # Make sure the session will never clear itself
        return render_template("mainhtml.html",ops = operator.operations,curr_out = required_out) # returns the main html with the array of operations

    elif request.method == "POST": # if got to the website from a press of button
        try:
            submit = request.form["action"][:6]
            print("FOUND - " + request.form["action"])
            if request.form["action"] == "Save": # If the saved button is pressed
                required_out = request.form["outID"] # set required frame
                operator.update() # activate all operations and update values
                save_session() # save again ( with set values )

            elif request.form["action"] == "Update": # if update is pressed
                required_out = request.form["outID"] # set required frame
                print("Req Out is",required_out) 
                operator.update() # activate all operations and set values

            elif submit == "Delete":
                value = int((request.form["action"])[6:])
                operator.Delete(value)

            elif submit == "MoveUP":
                value = int((request.form["action"])[6:])
                operator.MoveUP(value)

            elif submit == "MovDON":
                value = int((request.form["action"])[6:])
                operator.MoveDOWN(value)

            elif request.form["action"] == "WindowMode": # If the saved button is pressed
                # cv2.destroyAllWindows()
                global windowMode
                windowMode = not windowMode

            else: # if not update nor save was pressed, add an operation
                value = request.form["action"] # get the pressed button's name
                add_operation(value) # add operation with the name of the button
                    
                    
        except:
            pass

        return render_template("mainhtml.html",ops = operator.operations,curr_out = required_out) # return the html page with all the operations

def add_operation(operation_name): # add a new operation
    operator.update() # activate all operations and set input values
    new_op = copy.deepcopy(sky_operations[request.form["action"]]) # copy an operation from the dictionary of operations
    new_op.add_num(operator.inCounter) # add a unique number to each inputs ( used to identify each one )
    operator.operations.append(new_op) # add the new operation to the array of operations
    


def save_session(): # save the operations
    print("Saving Session")
    operations_dict = [] # initialize operation_dict
    for op in operator.operations:
        operations_dict.append(op.conv_dict()) # add the opeartion to the array after converting it to a dictionary
        
    session["operations"] = operations_dict # save operations to the session

    r = jsonify(dict(session)) # turn the session to json
    with open("session.json", "w") as file: # open the save file
        file.write(r.get_data(as_text=True)) # write the session to the save file
        file.close() # close the save file
        print("Saved Session")


app.run(debug = True,host='0.0.0.0') # run the app on main