# RPI-CameraStreaming-for-multiple-users

This project is a modification of some tutorials i found online to allow video stream from a raspberry pi server using Apache/flask/opencv,

The modification is to include ZeroMQ to allow multiple clients to connect at once

It also has support for the user to add computer vision processing using OpenCV

The main application writes video frames to a publisher socket. Each client will is fed from a subscriber socket.



<img width="649" alt="Screenshot 2023-02-16 at 6 58 25 pm" src="https://user-images.githubusercontent.com/113757511/219303363-d83feabe-1fd3-466b-9fe8-1c1de31f149d.png">

### Code Integration

The Camera handling process (CameraMain.py) will dynamically import a module specified in the settings dictionary under "ModuleType" (see programSettings.py)

<img width="726" alt="Screenshot 2023-02-16 at 7 02 07 pm" src="https://user-images.githubusercontent.com/113757511/219303944-6e298070-36fc-4c44-9d0f-acd9d8263028.png">

<img width="452" alt="image" src="https://user-images.githubusercontent.com/113757511/219304210-83e9b3ea-23f6-481c-8185-df1a936970ff.png">

if it is unable to import any module, it will instead just export unedited frames in jpeg format and these will be displayed on the webpage

This way there is no need to modify any of the provided code

The imported file must have a function call process_image(src)

<img width="182" alt="image" src="https://user-images.githubusercontent.com/113757511/219305128-fbfb34bb-a0e7-49c2-a4ca-1ab359f41972.png">

you can make any modifications you like to the source image

After returning, the main process will add a stamp consisting of the module name and a timestamp

<img width="452" alt="image" src="https://user-images.githubusercontent.com/113757511/219305488-93631fba-e1d6-4f14-8483-a0b6cc87a2e4.png">

There are some in-built functions in the file "Commonfunctions.py"

These allow for some interaction with ROIs, drawing text/shapes and some other functions

ROIs are stored in the “ProgramSettings.py” file. They are stored in a sub-dictionary of global_Settings called “Camera_ROI_List”. They are stored as percentages of the total height/width of the image (so that they will work at any resolution)

To edit the “Camera_ROI_List” dictionary you can do something like this

<img width="452" alt="image" src="https://user-images.githubusercontent.com/113757511/219306754-2601ce11-55c5-442b-907a-484564e32244.png">

The colour codes are specified in “ColourCodes.py” as 8 bit (B,G,R) values. This is the colour that will be used to draw a bounding box around the ROI (if desired)
 
<img width="302" alt="image" src="https://user-images.githubusercontent.com/113757511/219306799-a2370d87-71ba-43b9-9431-4b35fd35ace8.png">

You can create a separate matrix containing the ROI by calling “isolateROI”
 
 <img width="452" alt="image" src="https://user-images.githubusercontent.com/113757511/219306980-2c158e22-d84e-463a-9412-f62a78749e13.png">

The input parameters are the source frame and the dictionary key (i.e. “AccessPoint_1”). If the key is invalid the program will return “False”

The ROI returned is a pointer to the original source image. Meaning that if you edit it, it will also edit the source. If you don’t want this, you can make a copy first, as per the below example.

<img width="452" alt="image" src="https://user-images.githubusercontent.com/113757511/219307474-02752d8e-36c3-4939-a2bf-60940b86561a.png">

You can draw a bounding box around the ROI(s) by calling

<img width="452" alt="image" src="https://user-images.githubusercontent.com/113757511/219307528-b2a9c798-21dc-40e7-b33f-35bb1f7a5548.png">

“displayName” controls whether a label will be printed with the ROI’s name (the key)

You can add text to an image using "DrawText"

<img width="452" alt="image" src="https://user-images.githubusercontent.com/113757511/219307637-4c280b16-b97c-4f4f-8d0b-061afbe7816d.png">

The function “DrawText” will automatically scale text for different resolutions. 

It will also add a black outline to the text first for readability reasons.

### Installation using pi OS

    $ apt-get install python3-opencv

    $ apt-get install pyzmq

    $ apt-get install pip3


install apache

    $ pip3 install Flask

    $ apt-get install apache2

    $ apt-get install libapache2-mod-wsgi-py

Tell apache to listen on port 8080 (or whatever else)

    $ nano /etc/apache2/ports.conf

add "Listen 8080" underneath "Listen 80"

<img width="452" alt="image" src="https://user-images.githubusercontent.com/113757511/219314754-54fb7387-9bdf-46df-b593-2987993238e4.png">

copy the file "8080-CameraInterface.conf" into "/etc/apache2/sites-available"

Enable the site

    $ sudo a2ensite 8080-CameraInterface.conf

copy "scripts", "static" and "templates" into var/www/html

give apache ownership of the files
- sudo chown -R www-data:www-data /var/www
- sudo chmod -R 777 /home/pi/.local/lib/python3.9/


set permission to access webcam
-	sudo chown www-data:www-data /dev/video0
-	sudo adduser www-data video
-	sudo usermod -a -G video www-data

restart apache2
-	sudo service apache2 restart

### Operation

log into the webpage using the rapsberry pi's IP:8080 or host address raspberry.pi:8080 (deault host name)

click the play button to launch "CameraMain.py"

<img width="361" alt="image" src="https://user-images.githubusercontent.com/113757511/219305981-6732655d-1696-4090-b0cb-426d8ba63ee4.png">

click the stop button to kill the process

The Service screen (Wrench) currently will show the Regions of interest used by the application (defined in ProgramSettings.py)

<img width="452" alt="image" src="https://user-images.githubusercontent.com/113757511/219306232-15d370ce-223e-4997-8a1e-e03812ab4e27.png">

Future updates will allow these ot be adjusted/added/removed

Troubleshooting

you can view apache error logs by entering

    sudo tail -10 /var/log/apache2/error.log
   
where -10 means the last 10 messages
