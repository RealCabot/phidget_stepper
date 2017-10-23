#!/usr/bin/env python

import rospy
from phidget_stepper.msg import StepperConfig
def talker():
    pub = rospy.Publisher("motor_config", StepperConfig, queue_size=10)
    rospy.init_node('motor_test', anonymous=True)
    rate = rospy.Rate(1) # 2hz

    while not rospy.is_shutdown():
        leftCmd = StepperConfig()
        leftCmd.toLeft = True
        leftCmd.engage = True #True for sending  power to motor coils (make it move)
        leftCmd.mode = True #True
        leftCmd.velocityLimit =  float(20)
        leftCmd.acceleration = float(100)
        leftCmd.position = int(1500)

        print("sent it boss")
        pub.publish(leftCmd)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
