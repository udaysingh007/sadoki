import RPi.GPIO as GPIO         # using Rpi.GPIO module
from time import sleep          # import function sleep for delay
import logging
from detection import objectdetection as od
from temperature import thermalsensor as ts 
from constants import const as cn
from sms import twilioagent as sms
from led import status as led

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def cleanup():
    ts.cleanup()
#    GPIO.cleanup()
    
if __name__ == '__main__':
    
    logging.debug('Start of main')
    
    temperature = 0
    humidity = 0
    
    # turn on the green LED
    led.alarmOff()
    
    # sleep for 5 seconds for sensors to initialize
    sleep(5)
    
    while True:
        logging.debug('calling ts.read()')
        temperature, humidity = ts.readsensor(temperature, humidity)
        logging.debug("Temperature: {}*C   Humidity: {}% ".format(temperature, humidity))
        logging.debug('returned from ts.read()')

        logging.debug('calling detect_object()')
        retVal = od.detect_object()
        logging.debug('returned from detect_object()')
        
        # if objects found, then break from while
        if (temperature > cn.TEMP_THRESHOLD):
            if (retVal.get(cn.PERSON) or retVal.get(cn.DOG) or retVal.get(cn.CAT)):
                logging.debug('inside the alert condition')

                # turn on the green LED
                led.alarmOn()
                
                logging.debug("sleep for 30 second before sending out SMS")
                sleep(30)
                
                # send out SMS
                msgbody = "Sadoki lifeguard alert: Occupants in car with temperature: " + str(temperature)
                logging.debug(msgbody)
                # sms.sendsms(msgbody, cn.TO_NUMBER)
                break
        
        # sleep for 1 minute
        logging.debug('sleeping for 1 min')
        sleep(60)
    
    logging.debug('Exiting main')
    
    cleanup()



    
    
