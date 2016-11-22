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
motR = ev3.LargeMotor('outA')
btn=ev3.Button()
motL.position=0
motR.position=0
oldTime=time.time()
while(math.fabs(time.time()-oldTime)<1):
    motL.run_direct(duty_cycle_sp=50)
    motR.run_direct(duty_cycle_sp=50)
    print(motL.position)
    print(motR.position)
    if btn.any():
        break;

print(motL.position)
print(motR.position)
motL.stop()
motR.stop()
