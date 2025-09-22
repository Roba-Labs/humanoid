import os
import sys
from scservo_sdk import *   # Uses SCServo SDK library

try:
    sys.path.insert(1, 'D:/ROBA_Software/roba_bus_servo_python') #path init for find library

    # Default setting
    SCS_IDR      = 0        # do'n need to init id 
    SCS_IDC      = 4        # Just set change  ID 
    BAUDRATE     = 115200   # SCServo default baudrate : 1000000
    DEVICENAME   = "COM8"   # Check which port is being used on your controller
                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
    protocol_end = 1        # SCServo bit end(STS/SMS=0, SCS=1)


    # serial port init 
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(protocol_end) # protocol init

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")

    #Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
