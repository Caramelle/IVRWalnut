#! /usr/bin/env python
# Core imports
import time
import ev3dev.ev3 as ev3

# Local Imports
import tutorial as tutorial
import utilities
import openLoopControl as olc

def calibrateBlack (sensor):
	#calibrating for black
	global blackMin
	global blackMax
	print ('Place me on black')
	time.sleep(2)
	print ('Reading black')
	endTime = time.time() + 5 ;
	while time.time() <= endTime:
		motR.run_direct (duty_cycle_sp=10)
	 	motL.run_direct(duty_cycle_sp=10)
		current = sensor.value()
		if current <= blackMin:
			blackMin = current
		if current >= blackMax:
			blackMax = current
	motR.stop()
	motL.stop()
#	return black

def calibrateWhite (sensor):
	#calibrating for white
	global whiteMin
	global whiteMax
	print ('Place me on white')
	time.sleep(5)
	print('Reading white')
	endTime = time.time() + 5 ;
	while time.time() <= endTime:
		motR.run_direct (duty_cycle_sp=10)
	 	motL.run_direct(duty_cycle_sp=10)
		current = sensor.value()
		if current <= whiteMin:
			whiteMin = current
		if current >= whiteMax:
			whiteMax = current
	motR.stop()
	motL.stop()


motR = ev3.LargeMotor('outA')
motL = ev3.LargeMotor('outD')
colorSensor = ev3.ColorSensor()
btn =ev3.Button()
colorSensor.mode = 'COL-REFLECT'
colorSensor.connected

#global values for calibration
blackMin = 200;
blackMax = 0;
whiteMin = 200;
whiteMax = 0;

calibrateWhite(colorSensor)
calibrateBlack(colorSensor)

readings = ""
readings_file = open('calibration.txt', 'w')
readings = readings + str(blackMin) + '\n'
readings = readings + str(blackMax) + '\n'
readings = readings + str(whiteMin) + '\n'
readings = readings + str(whiteMax) + '\n'
readings_file.write(readings)
readings_file.close()