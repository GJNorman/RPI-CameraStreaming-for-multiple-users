import numpy as np
import cv2 as cv                        #camera operations
import zmq                              #socket communication
from ZMQSocketClass import ZMQSocket    #abstraction layer over zmq
import datetime                         #using datetime module
import threading                        #for socket messages sent by/to other programs
from SchedulerClass import Scheduler    #basic Timer 
from ProgramSettingsSave import *       #import global variables
from ColourCodes import *               #color codes for opencv
from CommonFunctions import *           #commonly used functions

"""
****************************************************************************
            selectively load file based on the 
            connected module type
****************************************************************************
"""
try:
            Application = __import__(global_Settings["ModuleType"])
except:
            Application = None
Message = ""
MessageRxFlag = False

#preallocate frame buffer
mainFrameBuffer = np.zeros((global_Settings["Camera_Vertical_Resolution"],global_Settings["Camera_Horizontal_Resolution"],3),np.uint8)

"""
****************************************************************************
            add time stamp and module name to frame

            ModuleName  TIMESTAMP   STATUS      FRAMERATE
****************************************************************************
"""
def stampImage(image,StampFps):          
    global global_Settings,ColourCodes

    ct = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    status = "ONLINE"   #TODO

    message = global_Settings["ModuleName"] + " " + ct + " " + status + " FPS:" +str(StampFps)
    DrawText(image,message,[5,5])
    return
"""
****************************************************************************
        initialise /dev/video0 with required resolution and framerate
        return a handle to the camera
****************************************************************************
"""
def initCamera(cameraID):
    global global_Settings
    try:
        cap = cv.VideoCapture(cameraID,cv.CAP_ANY) #cv.CAP_V4L2)
    except:
        cap = cv.VideoCapture(-1,cv.CAP_ANY)                  
    cap.set(cv.CAP_PROP_FRAME_WIDTH, global_Settings["Camera_Horizontal_Resolution"])
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, global_Settings["Camera_Vertical_Resolution"])
    cap.set(cv.CAP_PROP_FPS, global_Settings["Camera_FPS"])
    return cap
"""
****************************************************************************
        setup various system timers for scheduling
****************************************************************************
"""
def initTimers():
    global global_Settings
    requiredTimeBtwFrames = 1.0/global_Settings["Camera_FPS"]
    CameraTimer = Scheduler(requiredTimeBtwFrames)

    #used to calculate FPS
    OneSecondTimer = Scheduler(1.0)
    return CameraTimer,OneSecondTimer

"""
****************************************************************************
        This function is for communications with other processes 
        using REP/REQ pattern
****************************************************************************
"""
def MessageIOFunction():
    global Message,MessageRxFlag

    socket = ZMQSocket(global_Settings["SOCKET_WebInterfaceIO"],  zmq.REP,"bytes", "Server")

    while True:
        #wait for previous message to be processed
        while MessageRxFlag is True:
            pass
        Message = socket.recv()     #get next message - blocking request
        socket.send(b'Ack')         #acknowledge message
        MessageRxFlag = True        #set flag for main process
    return
"""
****************************************************************************
        This function is for processing messages recieved from other processes 
****************************************************************************
"""
def processMessage():
    global Message,MessageRxFlag,Application
    print("Raw Message: ",Message)
    exitRequest = False                         #process has not recieved a request to exit
    Message=str(Message)

    #look for a request to change running mode
    if Message.find("Mode") != -1:
        del Application
        if Message.find("Service") != -1:     
            Application = __import__("ServiceMode")
            
        elif Message.find("Application") != -1:
            Application = __import__(global_Settings["ModuleType"])
            
        elif Message.find("Stop") != -1:
            exitRequest = True
    #look for a request to save the regions of interest
    if Message.find("SaveROIs") != -1:
        saveSettings(global_Settings)

    #look for a request to adjust the current regions of interest
    if Message.find("Set ROI ") != -1:
        try:  
            #b"Set ROI ImmutableMultiDict([('ROIName', 'EXAMPLE_ROI_1'), ('top', '25'), ('bottom', '35'), ('left', '30'), ('right', '40')])"
            EndMarker = "'"
            Name    = isolateSubstring(Message,"ROIName', '",   EndMarker)
            top     = isolateSubstring(Message,"top', '",       EndMarker)
            bottom  = isolateSubstring(Message,"bottom', '",    EndMarker)
            left    = isolateSubstring(Message,"left', '",      EndMarker)
            right   = isolateSubstring(Message,"right', '",     EndMarker)

            global_Settings["Camera_ROI_List"][Name][2] = isolateSubstring(Message,"Colour', '",     EndMarker)
            global_Settings["Camera_ROI_List"][Name][0] = [int(left),int(top)]
            global_Settings["Camera_ROI_List"][Name][1] = [int(right),int(bottom)]
        except:
            pass

    MessageRxFlag = False        
            
    return exitRequest
"""
****************************************************************************
            Process the Next frame
            hand it over to the "Application"
            then do post-processing
                        add timestamp
                        convert to jpeg
                        transmit over socket
****************************************************************************
"""
def ProcessNextFrame(cap,WebLiveSocket,FPS_Counter,StampFps):
    global mainFrameBuffer 
    Success = cap.read(mainFrameBuffer)[0]    #normally cap.read() returns two values -> bool, frameBuffer
                                              #we're passing the frame buffer by reference, so we don't want that returned
                                              #thats why we use array notation to only return the first parameter (bool)
    if Success is True:
        #increment counter
        FPS_Counter+=1

        #pass frame to application 
        if Application is not None:
            Success = Application.process_image(mainFrameBuffer)
            if Success is True:
                #add timestamps 
                stampImage(mainFrameBuffer,StampFps)        #stampFPS holds the FPS from the previous second
                #convert to .jpg image
                if global_Settings["Camera_Export_As_Gray"] == True:
                    ret,jpeg = cv.imencode('.jpg',  cv.cvtColor(mainFrameBuffer, cv.COLOR_BGR2GRAY))
                else:
                    ret,jpeg = cv.imencode('.jpg', mainFrameBuffer)
                #transmit on publish socket
                WebLiveSocket.send(jpeg) 
    return FPS_Counter  
"""
****************************************************************************
            MAIN
****************************************************************************
"""
if __name__ == '__main__':

    #initialise the camera
    cap = initCamera(0)
    #Task schedulers
    CameraTimer, OneSecondTimer = initTimers()

    # ZeroMQ - set up publisher socket for Live monitoring
    WebLiveSocket  = ZMQSocket(global_Settings["SOCKET_liveStream"],  zmq.PUB,"bytes", "Server",[zmq.SNDHWM,global_Settings["SOCKET_FRAMES_TO_BUFFER"]])
    MeassageThread = threading.Thread(target=MessageIOFunction,daemon=True)
    MeassageThread.start()

    FPS_Counter = 0
    StampFps = 0

    
    while cap.isOpened():

        #Process Next Frame
        if (CameraTimer.CheckTimeout() == True):
            FPS_Counter = ProcessNextFrame(cap,WebLiveSocket,FPS_Counter,StampFps)
                
        #calculate the Frame rate every second
        if(OneSecondTimer.CheckTimeout() == True):
            StampFps = FPS_Counter
            FPS_Counter = 0
    
        #check if any messages have been recieved
        if MessageRxFlag is True:
            exitRequest = processMessage()
            if exitRequest is True:
                break
         
    # tidy up
    cap.release()                               #release /dev/video0
