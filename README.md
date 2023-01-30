# RPI-CameraStreaming-for-multiple-users

This project is a modification of some tutorials i found online to allow video stream from a raspberry pi server using Apache/flask/opencv,

The modification is to include ZeroMQ to allow multiple clients to connect at once

The main application writes video frames to a publisher socket. Each client will is fed from a subscriber socket.
