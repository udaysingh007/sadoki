import time
import board
import logging
import adafruit_dht
import psutil
from constants import const as cn

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(cn.DHT_PIN)

def readsensor(temp, humidity):
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        logging.debug("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        return temp, humidity
    except RuntimeError as error:
        logging.debug(error.args[0])
        return temp, humidity
    except Exception as error:
        sensor.exit()
        raise error

def cleanup():
	sensor.exit()
    
