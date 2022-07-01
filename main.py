import RPi.GPIO as GPIO         # using Rpi.GPIO module
from time import sleep          # import function sleep for delay
import logging
from detection import objectdetection as od

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
    
if __name__ == '__main__':
    
    logging.debug('Start of main')
    
    retVal = 0
    
    while True:
        logging.debug('calling detect_object()')
        retVal = od.detect_object()
        logging.debug('returned from detect_object()')
        
        # if objects found, then break from while
        if (retVal):
            break
        
        # sleep for 1 minute
        logging.debug('sleeping for 1 min')
        sleep(60)
    
    logging.debug('Exiting main')
    
    #sleep(15);



    
    
