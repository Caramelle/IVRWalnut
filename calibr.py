#! /usr/bin/env python
# Core imports
import time
import ev3dev.ev3 as ev3
import math
# Local Imports
import tutorial as tutorial
import utilities
import openLoopControl as olc


motL = ev3.LargeMotor('outD')
btn=ev3.Button()
g=ev3.GyroSensor()
g.mode='GYRO-ANG'
oldVal=g.value()
print("OLD VALUE: ",oldVal)
while(math.fabs(oldVal-g.value())<89):
    motL.run_direct(duty_cycle_sp=20)
    print(g.value())
    if btn.any():
        break;


motL.stop()
