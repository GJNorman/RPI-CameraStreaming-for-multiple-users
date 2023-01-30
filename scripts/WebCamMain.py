from flask import Flask, render_template, Response, request, send_from_directory  
from ProgramSettingsSave import *
from SubscriberSocket import SubscriberSocketClass
from ZMQSocketClass import ZMQSocket
import zmq
import subprocess
#camera interface
pi_camera = SubscriberSocketClass(global_Settings["SOCKET_liveStream"])

#flask application
app = Flask(__name__,static_folder="../static",template_folder="../templates")

#socket for talking to main application; "relaxed" will prevent lockup in case the main application is not running when a messsage is sent to it
socket = ZMQSocket(global_Settings["SOCKET_WebInterfaceIO"],zmq.REQ,'bytes',"Client",[zmq.REQ_RELAXED,1])


"""
********************************************************
                Setup webpage
********************************************************
"""
@app.route('/')
def loadHtmlFile():
    return render_template('CameraWebpage.html') 

"""
********************************************************
        request a javascript file
********************************************************
"""
@app.route('/RequestScriptFile')
def RequestScriptFile():
    filename = 'scripts/'+ request.args.get('filename')
    return send_from_directory('../',filename)



"""
********************************************************
        camera stream
********************************************************
"""
def yieldFrame(camera):
    #poll camera until a valid frame is recieved; (in case main application is not ready)
    while True:
        frame, ret = camera.get_message()

        if ret == True:
            return frame 


@app.route('/video_feed')
def video_feed():
    resp =  Response(yieldFrame(pi_camera),mimetype='image/jpeg')
    return resp


"""
********************************************************
    Send messages to the main camera application
    message is in bytes, b'whatever'
********************************************************
"""
def contactCameraMain(message):
    """
    create a socket to talk to "Camera Main"
    send a message; for example "Enter Service Mode"
    """

    socket.send(message)
    socket.recv()                       #wait for ack


"""
********************************************************
    Change program between service and application modes
********************************************************
"""
@app.route('/serviceMode',methods = ['POST', 'GET'])
def setServiceMode():
    global global_Settings
    contactCameraMain(b"Enter Service Mode")
    returnString = convertDictionary(global_Settings["Camera_ROI_List"])
    return Response(returnString.encode(),mimetype='text/plain')

@app.route('/applicationMode',methods = ['POST', 'GET'])
def setApplicationMode():
    contactCameraMain(b"Enter Application Mode")
    return "None"

@app.route('/startProcess',methods = ['POST', 'GET'])
def startProcess():
    print('Starting Main Camera Process')
    subprocess.Popen(["python3", "/var/www/html/scripts/CameraMain.py"])
    return "None"

@app.route('/stopProcess',methods = ['POST', 'GET'])
def stopProcess():
    contactCameraMain(b"Enter Stop Mode")
    return "None"

"""
********************************************************
        Edit Regions of interest
********************************************************
"""
#chage the boundary of a ROI
#URL will look like IP:PORT/setROI?ROIName=NAME&top=pxl&left=pxl&right=pxl&bottom=pxl&Colour=red
@app.route('/setROI',methods = ['POST', 'GET'])
def setROI():
    contactCameraMain(b"Set ROI " + str(request.args).encode())
    return "None"

#permanentely save all ROIs
@app.route('/saveROIs',methods = ['POST', 'GET'])
def saveROIs():
    contactCameraMain(b"SaveROIs")
    return 'None'
