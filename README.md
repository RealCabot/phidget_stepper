# Phidget Motor Wrapper

## How to use

```
roslaunch phidget_stepper launch_motor.launch
```
This will fire up two motor instances suscribing to topic `/motor_config`, the message type can be seen by `rosmsg show StepperConfig`

## How to run motor demo

```
roslaunch phidget_stepper demo_motor.launch
```

## Note
- Make sure you add `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib` to `~/.bashrc` file before running `roslaunch`

## Future work

- Seperate phidget library and ROS wrapper
- ~~Make a test script to show how to use the node~~
