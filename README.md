# pi5_RC
Project for controlling a car from a non local network.

#Assumptions [in progress]
This project was designed to run on a raspberry pi 5 with Ubuntu 24.04.4 LTS (Noble Numbat). For setting up the raspberry pi, look at youtube videos that use the pi imager 

Use the Rpi recommended 5V, 5A power supply. 


TIPS: Installing Rustdesk on your development machine to remote into the pi is helpful. Lets you develop with VS code or similar which would be resource heavy on the pi. In general, its a good idea to only run software that is necessary on the edge device(in this case the pi). It will be plenty taxed with the camera, networkconnectivity, and other functions.

#Requirements [in progress]
install RPi.GPIO

sudo apt-get update && sudo apt-get install python3-rpi.gpio

install ROS2 Jazzy Jalisco

(insert ROS2 install instructions here)

#BOM [in progress]
- Raspberry pi 5, 4GB ram (recommend heatsink and fan kit too)
- Cytron MD20A motor controller
- Stock Losi micro T (modifications listed below)
- Rpi AI camera and cable kit for Pi5

#Losi Micro T modifications
1. Unplug the battery 
2. Unplug Spektrum servo from 2 in 1 ESC and reciever
3. Desolder the ESC wires from the motor
4. Attach 3D printed adapter to house the new motor controller, rpi, etc
