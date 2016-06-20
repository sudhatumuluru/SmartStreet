from datetime import datetime, timedelta
import sqlite3 as lite
import json
import sys

def check_ip_control(call_ip):
	print call_ip
	query = "select ip_address, datetime, released from ip_control order by datetime desc limit 1"
	try:
		db_connection = lite.connect('sensorstatus.db')
		db_cur = db_connection.cursor()
		db_cur.execute(query)
		row = db_cur.fetchone();

		db_ip = row[0]
		db_datetime = row[1]
		db_release = row[2]

		if( db_release == "released" ):
			update_ip_control(call_ip)
			concurrency = "proceed"
		else:
			# compare sysdate with dbdate
			sysdate = unicode(datetime.now())
			dateformat="%Y-%m-%d %H:%M:%S.%f"
			db_date = datetime.strptime(db_datetime, dateformat)

			if datetime.now() > db_date + timedelta(seconds=30):
				print("system is unlocked")
				time_calc = "unlocked"
			else:
				print("system is locked")
				time_calc = "locked"


			# check ip address
			if( call_ip == db_ip ):
				if( time_calc == "unlocked" ):
					update_ip_control(call_ip)
					concurrency = "proceed"
				else:
					concurrency = "proceed"
			else:
				if( time_calc == "unlocked" ):
					update_ip_control(call_ip)
					concurrency = "proceed"
				else:
					concurrency = "busy"

	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)

	print ("concurrency: "+concurrency)
	return concurrency


def calculate_time(db_datetime):
	print db_datetime

	sysdate = unicode(datetime.now())
	print sysdate

	dateformat="%Y-%m-%d %H:%M:%S.%f"
	db_date = datetime.strptime(db_datetime, dateformat)

	if datetime.now() > db_date + timedelta(minutes=1):
		print("system is unlocked")
		time_calc = "unlocked"

	else:
		print("system is locked")
		time_calc = "locked"

	return time_calc


def update_ip_control(call_ip):
	sysdate = unicode(datetime.now())
	query = "insert into ip_control values('"+call_ip+"', '"+sysdate+"', 'NULL')"
	try:
		db_connection = lite.connect('sensorstatus.db')
		db_cur = db_connection.cursor()
		db_cur.execute(query)
		db_connection.commit()
		print("update_ip_control complete")

	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)

def release_ip_control():
	query = "update ip_control set released = 'released' where datetime = (select max(datetime) from ip_control)"
	try:
		db_connection = lite.connect('sensorstatus.db')
		db_cur = db_connection.cursor()
		db_cur.execute(query)
		db_connection.commit()
		print("release_ip_control complete")

	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)

#check_ip_control("192.168.0.001")
#print match
