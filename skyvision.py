import copy  # the most underrated library
import json
import time

from src.skyv_operations import *
import src.skyv_network as skyv_network

app = Flask(__name__)  # app
app.secret_key = "#4416"  # -secret key used for session saving

operator = new_operator()  # main class responsible for organizing and activating operations
operator.loadOperationArray(new_operations)

error_pic = cv2.imread("res/images/ERR.jpg")  # The frame that will be used for drawing when there is an error
outputOptions = "" # Options for frames the user can show
required_out = "None"  # Current frame that will be drawn on screen

def generateVideo(resolution = 0.5):  # generates the output frame
    time.sleep(3)  # delay to allow for camera reconnection
    while True:
        operator.process()  # activate all operations
        outputs = operator.values  # get all values from the operator

        try:  # try to set the output frame to the required frame
            selected_out = outputs[required_out]  # set the output to the required frame
            selected_out = cv2.resize(selected_out,(int(selected_out.shape[1] * resolution),int(selected_out.shape[0] * resolution)))
        except:  # if setting output frame fails, set it to the error pic
            selected_out = None
            selected_out = cv2.resize(error_pic,(int(error_pic.shape[1] * 0.25),int(error_pic.shape[0] * 0.25)))  # set the output frame to the error pic
            

        ret, encodedImage = cv2.imencode(".jpg", selected_out)  # turn the output pic to a jpg

        if ret:  # if encoding to jpg fails, skip this frame
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(
                encodedImage) + b'\r\n')  # output the frame in a format that the browser can read

@app.route("/video_feed")
def video_feed(): # return the output from the generate() function
    return Response(generateVideo(),mimetype="multipart/x-mixed-replace; boundary=frame")  

@app.route("/", methods=['GET', 'POST'])  # route for main page, allows for GET and POST requests
def home():  # home page
    global required_out
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
            print("Unable to located \"session_" + str(saveName) + ".json'\"")  # print error if failed to open session.json

        session.permanent = True  # Make sure the session will never clear itself
        operator.update(False)
        if len(operator.frames) > 0:
            required_out = operator.frames[0]
        outputOptions = operator.frameOptions
        return render_template("mainhtml.html", ops=operator.htmlOps(),
                               curr_out=required_out, out_select_options=outputOptions,
                               currFile=saveName)  # returns the main html with the array of operations

    elif request.method == "POST":  # if got to the website from a press of button
        submit = request.form["action"]
        print("FOUND - " + request.form["action"])
        if request.form["action"] == "Save":  # If the saved button is pressed
            required_out = request.form["outID"]  # set required frame
            operator.update(True)  # activate all operations and update values
            outputOptions = operator.frameOptions
            save_session(saveName)  # save again ( with set values )

        elif request.form["action"] == "Update":  # if update is pressed
            required_out = request.form["outID"]  # set required frame
            operator.update(True)  # activate all operations and set values
            outputOptions = operator.frameOptions

        elif request.form["action"] == "Load":  # if Load is pressed
            saveName = request.form["loadedFile"]  # set file
            return redirect(url_for('/', save=saveName))

        elif "Delete" in submit:
            value = int((request.form["action"])[6:])
            operator.removeOperation(value)

        elif "MoveUP" in submit:
            value = int((request.form["action"])[6:])
            operator.moveOperation(value,-1)

        elif "MoveDOWN" in submit:
            value = int((request.form["action"])[8:])
            operator.moveOperation(value,1)

        else:  # if unkown button was pressed, add an operation
            print(submit)
            value = request.form["action"]  # get the pressed button's name
            add_operation(value)  # add operation with the name of the button
        return render_template("mainhtml.html", ops=operator.htmlOps(),
                               curr_out=required_out,
                               out_select_options=outputOptions,
                               currFile=saveName
                               )  # return the html page with all the operations


def add_operation(operation_name):  # add a new operation
    operator.update(True)  # activate all operations and set input values
    operator.addOperation(operation_name)  # add the new operation to the array of operations

def save_session(saveName):  # save the operations
    print("Saving Session")
    operations_dict = operator.operations  # initialize operation_dict
    session["operations"] = operations_dict  # save operations to the session

    r = jsonify(dict(session))  # turn the session to json
    with open('sessions/session_' + str(saveName) + '.json', "w") as file:  # open the save file
        file.write(r.get_data(as_text=True))  # write the session to the save file
        file.close()  # close the save file
        print("Saved Session")

def initWeb(network_table = True):
    global required_out
    global outputOptions
    if(network_table):
        print("Connecting to Network table...")
        skyv_network.init_and_wait('10.44.16.2',"Vision")

    saveName = 'session'
    f = open("sessions/lastSession.txt", "r")
    saveName = f.read()
    f.close()
    loadFromFile(saveName)

def loadFromFile(saveName):
    required_out = "None"  # set the required output frame to "None"
    with open('sessions/session_' + str(saveName) + '.json') as json_file:  # open the saved file
        operator.clearOperations()  # clear all loaded operations
        data = json.load(json_file)  # get the json data
        operator.operations = data["operations"]  # load operations from the json file
    operator.update(False)

initWeb(network_table=False)
app.run(debug=True, host='0.0.0.0')  # run the app on main