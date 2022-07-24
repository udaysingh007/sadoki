import io
import serial
import time
import string 
import pynmea2
from constants import const as cn


def getLatNLng():
	ser=serial.Serial(cn.UART_PORT, baudrate=9600, timeout=0.5) 
	dataout = pynmea2.NMEAStreamReader() 

	lat, lng = 'Null', 'Null'

	with ser:
		while True:
			newdata = ser.readline()
			line = ""
			try:
				line = newdata.decode()
			except:
				continue
				
			# print(line)
			if line[0:6] == "$GPRMC":  
				newmsg = pynmea2.parse(line)  
				lat = str(newmsg.latitude) + " " + str(newmsg.lat_dir)
				lng = str(newmsg.longitude) + " " + str(newmsg.lon_dir)
				# gps = "Latitude: " + str(lat) + " and Longitude: " +str(lng) 
				# print(gps)
				
				return str(lat), str(lng)
			time.sleep(1)
			
		return lat, lng
