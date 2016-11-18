#! /usr/bin/env python
# Core imports
import time
import ev3dev.ev3 as ev3

# Local Imports
import tutorial as tutorial
import utilities
import openLoopControl as olc


motR = ev3.LargeMotor('outA')
motL = ev3.LargeMotor('outD')
print(motL.position)
motL.run_timed(duty_cycle_sp=30, time_sp=2.4*1E3)
time.sleep(2 )
#motR.run_timed(duty_cycle_sp=-30, time_sp=2.5*1E3)
print(motL.position)
ev3.Sound.speak('I\'m done baby').wait()
