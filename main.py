import RPi.GPIO as GPIO         # using Rpi.GPIO module
from time import sleep          # import function sleep for delay
import logging
from detection import objectdetection as od
from temperature import thermalsensor as ts 
from sms import twilioagent as sms

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

TO_NUMBER = '+19175824874'
TEMP_THRESHOLD = 19

def cleanup():
    ts.cleanup()
    
    
if __name__ == '__main__':
    
    logging.debug('Start of main')
    
    retVal = 0
    temperature = 0
    humidity = 0
    
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
        if (retVal and (temperature > TEMP_THRESHOLD)):
            logging.debug('inside the alert condition')
            msgbody = "Sadoki lifeguard alert: Occupants in car with temperature: " + str(temperature)
            logging.debug(msgbody)
            sms.sendsms(msgbody, TO_NUMBER)
            break
        
        # sleep for 1 minute
        logging.debug('sleeping for 1 min')
        sleep(60)
    
    logging.debug('Exiting main')
    
    cleanup()



    
    
