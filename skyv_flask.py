import json
from threading import Thread
from src.skyv_operator import *
import src.skyv_network as skyv_network
import logging
from datetime import datetime


print("\n\n")
app = Flask(__name__)  # app
app.secret_key = "#4416"  # -secret key used for session saving

log = logging.getLogger('werkzeug')
log.disabled = True
print("\n")

operator = operator()  # main class responsible for organizing and activating operations

def threadedProcess():
    time.sleep(1)
    while True:
        operator.process()

# sets the resolution of the output frames
def setResolution(resolution):
    operator.outResolution = resolution

@app.route("/video_feed")
def video_feed(): # return the output from the generate() function
    return Response(operator.generateVideo(), mimetype="multipart/x-mixed-replace; boundary=frame")  

@app.route("/", methods=['GET', 'POST'])  # route for main page, allows for GET and POST requests
def home():  # home page
    session.permanent = True  # Make sure the session will never clear itself
    global outputOptions
    # read the last session's name from file
    saveName = 'session'
    f = open("sessions/lastSession.txt", "r")
    saveName = f.read()
    f.close()

    # load name from url
    tmpName = request.args.get('save')
    if tmpName is not None:
        if len(tmpName) > 0:
            f = open("sessions/lastSession.txt", "w")
            saveName = tmpName
            f.write(saveName)
            f.close()
    
    # if entered page regularly
    if request.method == "GET":
        operator.clearOperations()
        try:
            loadFromFile(saveName)
        except:
            print(tColors.FAIL + getTime() + "Unable to locate \"session_" + str(saveName) + ".json'\"" + tColors.ENDC)  # print error if failed to open session.json

        operator.update(False)
        outputOptions = operator.frameOptions
        return render_template("mainhtml.html", ops=operator.htmlOps(),
                               opOptions=operator.loaded_operations,
                               curr_out=operator.required_out, out_select_options=outputOptions,
                               currFile=saveName)  # returns the main html with the array of operations

    elif request.method == "POST":  # if got to the website from a press of button
        print(tColors.WARNING + getTime() + "RECEIVED " + request.form["action"] + tColors.ENDC)
        submit = request.form["action"]
        if request.form["action"] == "Save":  # If the saved button is pressed
            operator.required_out = request.form["outID"]  # set required frame
            operator.update(True)  # activate all operations and update values
            outputOptions = operator.frameOptions
            save_session(saveName)  # save again ( with set values )
        elif request.form["action"] == "Update":  # if update is pressed
            operator.required_out = request.form["outID"]  # set required frame
            operator.update(True)  # activate all operations and set values
            outputOptions = operator.frameOptions
        elif "Delete" in submit:
            value = int((request.form["action"])[6:])
            operator.removeOperation(value)
        elif "MoveUP" in submit:
            value = int((request.form["action"])[6:])
            operator.moveOperation(value, -1)
        elif "MoveDOWN" in submit:
            value = int((request.form["action"])[8:])
            operator.moveOperation(value, 1)
        else:  # if unkown button was pressed, add an operation
            value = request.form["action"]  # get the pressed button's name
            add_operation(value)  # add operation with the name of the button
        return render_template("mainhtml.html", ops=operator.htmlOps(),
                                opOptions=operator.loaded_operations,
                               curr_out=operator.required_out,
                               out_select_options=outputOptions,
                               currFile=saveName
                               )  # return the html page with all the operations

def add_operation(operation_name):  # add a new operation
    operator.update(True)  # activate all operations and set input values
    operator.addOperation(operation_name)  # add the new operation to the array of operations

def save_session(saveName):  # save the operations
    print(tColors.OKBLUE + getTime() + "Saving Session" + tColors.ENDC)
    r = jsonify(operator.operations)  # turn the session to json
    with open('sessions/session_' + str(saveName) + '.json', "w") as file:  # open the save file
        file.write(r.get_data(as_text=True))  # write the session to the save file
        file.close()  # close the save file
        print(tColors.OKGREEN + getTime() + "Saved Session" + tColors.ENDC)

def initWeb(network_table = True):
    global outputOptions
    if(network_table):
        print(tColors.OKBLUE + getTime() + "Connecting to Network table..." + tColors.ENDC)
        skyv_network.init_and_wait('10.44.16.2',"Vision")

    saveName = 'session'
    f = open("sessions/lastSession.txt", "r")
    saveName = f.read()
    f.close()
    loadFromFile(saveName)

def loadFromFile(saveName):
    operator.required_out = "None"  # set the required output frame to "None"
    with open('sessions/session_' + str(saveName) + '.json') as json_file:  # open the saved file
        operator.clearOperations()  # clear all loaded operations
        operator.operations = json.load(json_file)  # load operations from the json file
    operator.update(False)

# runs the main application
def run(operations: list[operation]):
    operator.loadOperationArray(operations)
    Thread(target=threadedProcess).start()

    initWeb(network_table=False)
    app.run(debug=True, host='0.0.0.0',threaded=True)  # run the app on main
    logMessage("STARTING WEB INTERFACE")