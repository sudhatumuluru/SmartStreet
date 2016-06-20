import RPi.GPIO as GPIO
import subprocess
import time

pir_sensor = 4
buzzer_sensor = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_sensor, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(buzzer_sensor, GPIO.OUT)

def buzzer():
	for i in xrange(3):
		print(i)
  		GPIO.setup(buzzer_sensor, GPIO.OUT)
    	time.sleep(1)
    	GPIO.output(buzzer_sensor, GPIO.LOW)
    	time.sleep(1)
    	GPIO.output(buzzer_sensor, GPIO.HIGH)

def pir():
	previous_state = False
	current_state = False

	while True:
		time.sleep(0.1)
		previous_state = current_state
		current_state = GPIO.input(pir_sensor)
		GPIO.output(buzzer_sensor, GPIO.LOW)
		if current_state != previous_state:
			new_state = "HIGH" if current_state else "LOW" 
			print("GPIO pin %s is %s" % (pir_sensor, new_state))
			if new_state == "HIGH":
				buzzer()

try:
	pir()
	print "trying"
except KeyboardInterrupt:
	GPIO.cleanup()

