from flask import *
import json
import cv2

from skyvision import *

app = Flask(__name__) # app
app.secret_key = "#4416"


def generate():
    camera = cv2.VideoCapture('http://192.168.1.4:4747/mjpegfeed')
    while(camera.isOpened()):
        ret, frame = camera.read()
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        height, width = frame.shape[:2]
        frame = cv2.resize(frame,(width*3,height*3), interpolation = cv2.INTER_CUBIC)

        if not ret:
            continue

        ret, encodedImage = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(),mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/")
def home(): # home page

    with open('session.txt') as json_file:
        data = json.load(json_file)
        session["counter"] = data["counter"]
        session["data"] = data["data"]

    session.permanent = True
    return render_template("mainhtml.html")

@app.route("/formas",methods=["POST","GET"]) # allow post and get
def formas(): # home page
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        session["counter"] = session["counter"] + 1
        counter = session["counter"]
        print("Detection -",user)
        print("Counter -",counter)
        for i in range(counter):
            session["data"] = session["data"] + "<h1>P</h1><br/>"
        return ('', 204)
    else:
        return render_template("formas.html")

@app.route('/ops',methods=['GET', 'POST'])
def ops():
    operations = [
        str(operation("Image Input",OperationType.INPUT,text_inputs=[operation_TextInput("path","image path")])),
        str(operation("Morphology EX",OperationType.MORPH,
        text_inputs=[operation_NumberInput("src","Source",brake=False),operation_NumberInput("dst","Destination",text_style="margin-left:15px;")],
        radio_inputs=[operation_RadioInput("oprtn","operation",["close","open"],option_text_style="font-size:28px;",radio_style="margin-left:20px;")],
        checkbox_inputs=[operation_CheckboxInput("oprtn","operation",["close","open"],option_text_style="font-size:28px;",radio_style="margin-left:20px;"),
        operation_ColorInput("clr"," Color: ",style="width:500px;")]
        )),
        str(operation("next",OperationType.CONTOURS,text_inputs=[operation_TextInput("id","next id")]))
        ]
        
    return render_template("operations.html",ops = operations)


@app.route('/download_session')
def download_session():
    r = jsonify(dict(session))
    f = open("session.txt", "w")
    f.write(r.get_data(as_text=True))
    f.close()
    return render_template("formas.html")

if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0')