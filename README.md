# RPI-CameraStreaming-for-multiple-users

This project is a modification of some tutorials i found online to allow video stream from a raspberry pi server using Apache/flask/opencv,

The modification is to include ZeroMQ to allow multiple clients to connect at once

The main application writes video frames to a publisher socket. Each client will is fed from a subscriber socket.


installation using pi OS

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

copy the file "8080-CameraInterface.conf" into "/etc/apache2/sites-available"



