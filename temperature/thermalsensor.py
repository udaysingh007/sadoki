import time
import board
import logging
import adafruit_dht
import psutil

dhtPIN = board.D23

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(dhtPIN)

def readsensor(temp, humidity):
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        logging.debug("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        return
    except RuntimeError as error:
        logging.debug(error.args[0])
        return
    except Exception as error:
        sensor.exit()
        raise error

def cleanup():
	sensor.exit()
    
