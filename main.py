import RPi.GPIO as GPIO         # using Rpi.GPIO module
from time import sleep          # import function sleep for delay
import logging
from detection import objectdetection as od
from temperature import thermalsensor as ts 
from sms import twilioagent sms

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

to_number = '+19175824874'

def cleanup():
    ts.cleanup()
    
    
if __name__ == '__main__':
    
    logging.debug('Start of main')
    
    retVal = 0
    temperature = 0
    humidity = 0
    
    while True:
        logging.debug('calling ts.read()')
        ts.readsensor(temperature, humidity)
        logging.debug('returned from ts.read()')

        logging.debug('calling detect_object()')
        retVal = od.detect_object()
        logging.debug('returned from detect_object()')
        
        # if objects found, then break from while
        if (retVal):
            msgbody = "Sadoki lifeguard alert: Occupants in car with temperature: " + temperature
            sms.sendsms(msgbody, to_number)
            break
        
        # sleep for 1 minute
        logging.debug('sleeping for 1 min')
        sleep(60)
    
    logging.debug('Exiting main')
    
    cleanup()



    
    
