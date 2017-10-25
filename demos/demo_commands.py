#!/usr/bin/env python

import rospy
import time
from phidget_stepper.msg import StepperConfig

pub = None
isLeft = False
def stopMotors():
    # stop motor
    stopCmd = StepperConfig()
    stopCmd.toLeft = isLeft
    stopCmd.engage = False
    stopCmd.mode = True
    stopCmd.velocityLimit = float(0)
    stopCmd.acceleration = float(5)
    pub.publish(stopCmd)
    print "\nMotor stopped"

if __name__ == '__main__':
    try:
        pub = rospy.Publisher("motor_config", StepperConfig, queue_size=10)
        rospy.init_node('motor_test', anonymous=True)
        rate = rospy.Rate(2)  # 2hz

        leftCmd = StepperConfig()
        leftCmd.toLeft = isLeft
        leftCmd.engage = True  # True = make motors move
        leftCmd.mode = True  # True for velocity control
        leftCmd.velocityLimit = float(120000)
        leftCmd.acceleration = float(14000)

        pub.publish(leftCmd)
        print "parameters set"

        rospy.on_shutdown(stopMotors)
        # spin here until user exits program
        while not rospy.is_shutdown():
            rate.sleep()

    except rospy.ROSInterruptException:
        print "ROS interrupt"
        pass
