import RPi.GPIO as GPIO         # using Rpi.GPIO module
from time import sleep          # import function sleep for delay
import threading
import logging
from constants import const as cn
from detection import objectdetection as od
from temperature import thermalsensor as ts 
from sms import twilioagent as sms
from led import status as led
from motion import msensor as ms
# from gui import display as dp

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def cleanup():
    ts.cleanup()
#    dp.cleanup()
#    GPIO.cleanup()

def sadoki_thread(name="Sadoki Thread"): 
    # initialize the variables
    temperature = 0
    humidity = 0    

    # sleep for 5 seconds for sensors to initialize
    sleep(5)
    
    while True:
        logging.debug('calling ts.read()')
        temperature, humidity = ts.readsensor(temperature, humidity)
        logging.debug("Temperature: {}*C   Humidity: {}% ".format(temperature, humidity))
        logging.debug('returned from ts.read()')

        # indicate that were entering the processing mode
        led.greenBlinkerOn()
        
        # detect presence of kids or dogs or cats
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
        
        # indicate that we are done processing and all is good
        led.greenBlinkerOff()
        
        # sleep for 1 minute
        logging.debug('wait for the IR sensor or for 30 seconds')
        ms.waitForMotion(30)
    
    logging.debug('Exiting sadoki thread')
    
 
    
if __name__ == '__main__':
    logging.debug('Start of sadoki_thread')
    st = threading.Thread(target=sadoki_thread, name="Sadoki Thread")
    st.start()

    # launch the display window
    logging.debug('Launching the display window')
    # dp.launchDisplay()
    
    # wait for threads to join
    st.join()
    
    cleanup()

    
    
