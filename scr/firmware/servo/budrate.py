import os
import sys
from scservo_sdk import *   # Uses SCServo SDK library
import time
try:
    sys.path.insert(1, 'D:/ROBA_Software/roba_bus_servo_python') #path init for find library

    # Default setting
    SCS_IDR      = 4        # do'n need to init id 
    BAUDRATE     = 115200   # SCServo default baudrate : 1000000
    DEVICENAME   = "COM15"   # Check which port is being used on your controller
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

    #ping
    for scsid in range(0, 30):
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(portHandler, scsid)
        if scs_comm_result == COMM_SUCCESS:
            SCS_IDR = scsid

    time.sleep(.5)
    # trun one lock bit 
    scs_comm_result, scs_error = packetHandler.write4ByteTxRx(portHandler,SCS_IDR,55,0 )
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    elif scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))
    if scs_comm_result == COMM_SUCCESS:
       print("trun one lock bit ")

    time.sleep(.5)
    # change the ID number 
    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(portHandler,SCS_IDR,6,0 )
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    elif scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))
    if scs_comm_result == COMM_SUCCESS:
       print('change the ID number')
    time.sleep(0.1)

    # trun one lock bit 
    scs_comm_result, scs_error = packetHandler.write4ByteTxRx(portHandler,SCS_IDR,55,1)
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    elif scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))
    if scs_comm_result == COMM_SUCCESS:
        print('trun one lock bit')
except:
    print("some error")
# close port
portHandler.closePort()