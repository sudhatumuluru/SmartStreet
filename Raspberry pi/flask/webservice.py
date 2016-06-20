from flask import Flask
from flask import jsonify
from flask import request
import os
import subprocess
import json
import time
import sqlite3 as lite
import webservice_lib as lib

app = Flask(__name__)

# BLUE:  pigs p 18 255
# RED:	 pigs p 23 255
# GREEN: pigs p 24 255

@app.route("/") 
def hello():
	concurrency = lib.check_ip_control(request.remote_addr)
	if( concurrency == "busy" ):
		return "busy"
	elif( concurrency == "proceed" ):
		return "Hello world!"

@app.route("/status") 
def return_status():
	return "up"

@app.route('/smarttree/api/v1.0/release', methods=['GET'])
def control():
	concurrency = lib.check_ip_control(request.remote_addr)
	if( concurrency == "busy" ):
		return "user is not permitted"
	elif( concurrency == "proceed" ):
		lib.release_ip_control()
		return "control is released"

@app.route('/smarttree/api/v1.0/', methods=['GET'])
def get_ip():
	get_ip_address()
	dbentry = jsonify({'time': time.strftime("%c"), 'ip': request.remote_addr})
	return dbentry, 200

@app.route('/smarttree/api/v1.0/weather', methods=['GET'])
def getWeather():
	data=subprocess.check_output(['sudo', 'python', '/home/pi/Adafruit_Python_DHT/examples/getWeather.py', '11', '17'])
	print('this is my weather data: %s' % data)
	return data

@app.route('/smarttree/api/v1.0/music', methods=['GET'])
def getMusicList():
	musicList = os.listdir("../music/")
	print(musicList)
	return json.dumps(musicList)
	
	
@app.route('/smarttree/api/v1.0/music/<string:music_title>', methods=['GET'])
def music_control(music_title):

	concurrency = lib.check_ip_control(request.remote_addr)
	if( concurrency == "busy" ):
		return "busy"
	elif( concurrency == "proceed" ):
		if( music_title == "status" ):
			return "up"
		else:	
			print('omxplayer ../music/{}'.format(music_title))
			subprocess.call(['omxplayer', '../music/{}'.format(music_title)])
			return json.dumps(music_title)



@app.route('/smarttree/api/v1.0/light/<string:color>', methods=['GET'])
def control_light(color):
	def turn_lights_off():
		subprocess.call(['pigs', 'p', '18', '0'])
		subprocess.call(['pigs', 'p', '23', '0'])
		subprocess.call(['pigs', 'p', '24', '0'])

	def turn_lights_blue():
		subprocess.call(['pigs', 'p', '18', '255'])

	def turn_lights_red():
		subprocess.call(['pigs', 'p', '23', '255'])

	def turn_lights_green():
		subprocess.call(['pigs', 'p', '24', '255'])

	concurrency = lib.check_ip_control(request.remote_addr)
	if( concurrency == "busy" ):
		return "busy"
	elif( concurrency == "proceed" ):
		if color == 'off':
			turn_lights_off()
		elif color == 'blue':
			turn_lights_off()
			turn_lights_blue()
		elif color == 'red':
			turn_lights_off()
			turn_lights_red()
		elif color == 'green':
			turn_lights_off()
			turn_lights_green()
		elif color == 'all':
			turn_lights_blue()
			turn_lights_red()
			turn_lights_green()

		db_time = time.strftime("%c")
		db_status = color
		db_ip = request.remote_addr

		query = "insert into light_status values('"+db_time+"','"+db_status+"', '"+db_ip+"');" 

		print query

		try:
			db_connection = lite.connect('sensorstatus.db')
			db_cur = db_connection.cursor()
			print("db_cur is connection")
			db_cur.execute(query)
			db_connection.commit()
		except lite.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
		
		if db_connection:
			print("db_cur is closing")
			db_cur.close()

		return json.dumps(color)


@app.route('/smarttree/api/v1.0/light/status', methods=['GET'])
def get_status():
	query = "select * from light_status order by time desc limit 1"
	try:
		db_connection = lite.connect('sensorstatus.db')
		db_cur = db_connection.cursor()
		db_cur.execute(query)
		row = db_cur.fetchall();
	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
	return json.dumps(row);


if __name__ == "__main__":

	app.run(host='0.0.0.0')
