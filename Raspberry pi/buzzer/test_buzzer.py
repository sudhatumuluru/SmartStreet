#!/usr/bin/python
import RPi.GPIO as GPIO
import time

buzzPin = 25

GPIO.setmode(GPIO.BCM)

try:
  GPIO.setup(buzzPin, GPIO.OUT)
  while True:
    time.sleep(.5)
    GPIO.output(buzzPin, GPIO.LOW)
    time.sleep(.5)
    GPIO.output(buzzPin, GPIO.HIGH)

except:
  GPIO.cleanup()
