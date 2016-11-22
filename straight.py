#! /usr/bin/env python
# Core imports
import time
import math
import ev3dev.ev3 as ev3

# Local Imports
import tutorial as tutorial
import utilities
import openLoopControl as olc

R = ev3.LargeMotor('outA')
L = ev3.LargeMotor('outD')
btn = ev3.button()

R.reset()
L.reset()
while not btn.any():
	R.run_direct(duty_cycle_sp = 25)
	L.run_direct(duty_cycle_sp = 25)
R.stop()
L.stop()
