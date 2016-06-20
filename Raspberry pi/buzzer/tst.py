#!/usr/bin/python
import RPi.GPIO as GPIO
import time

buzzPin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzPin, GPIO.OUT)

try:
		while True:
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(buzzPin, GPIO.OUT)
			GPIO.output(buzzPin, GPIO.LOW)
			print("okay")
			time.sleep(.5)
			print("ugh")
			GPIO.output(buzzPin, GPIO.HIGH)
			time.sleep(.5)

except KeyboardInterrupt:
        GPIO.cleanup()
	

