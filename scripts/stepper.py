#!/usr/bin/env python
import rospy
from phidget_stepper.msg import StepperConfig

import time 
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

# RIGHT_ID = 420519
# LEFT_ID = 420520

ch = 0

def StepperAttached(e):
    try:
        attached = e
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("\n")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        exit(1)   
    
def StepperDetached(e):
    detached = e
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        exit(1)   

def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))

def PositionChangeHandler(e, position):
    print("Position: %f" % position)

def configMotor(conf):
    global ch
    if conf.toLeft == rospy.get_param("~isLeft"):
        ch.setEngaged(conf.engage)
        ch.setTargetPosition(conf.position)
        ch.setControlMode(conf.mode)
        ch.setAcceleration(conf.acceleration)
        ch.setVelocityLimit(conf.velocityLimit)

def closeMotor():
    global ch
    try:
        ch.close()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        exit(1) 
    print("Closed Stepper device")

if __name__ == '__main__':
    try:
        # Initialize stepper motors
        try:
            ch = Stepper()
        except RuntimeError as e:
            print("Runtime Exception %s" % e.details)
            exit(1)
        try:
            ch.setOnAttachHandler(StepperAttached)
            ch.setOnDetachHandler(StepperDetached)
            ch.setOnErrorHandler(ErrorEvent)

            ch.setOnPositionChangeHandler(PositionChangeHandler)

            print("Waiting for the Phidget Stepper Object to be attached...")
            SERIAL_ID = rospy.get_param('~serialId')
            ch.setDeviceSerialNumber(SERIAL_ID)
            ch.openWaitForAttachment(5000)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            exit(1)

        # Initialize suscriber node
        rospy.init_node('stepper_motor', anonymous=True)
        rospy.Subscriber("motor_config", StepperConfig, configMotor)

        rospy.on_shutdown(closeMotor)

    except rospy.ROSInterruptException:
        pass