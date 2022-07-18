import RPi.GPIO as GPIO         # using Rpi.GPIO module
from time import sleep          # import function sleep for delay
import cv2
import threading
import logging
from constants import const as cn
from detection import objectdetection as od
from temperature import thermalsensor as ts 
from sms import twilioagent as sms
from led import status as led
from motion import msensor as ms
from sound import speechtotext as speechtx

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def cleanup():
    ts.cleanup()
    speechtx.cleanup()
#    dp.cleanup()
#    GPIO.cleanup()

def speech_to_text_thread(e, name="STT Thread"): 
    speechtx.processSpeech(e)

def sadoki_thread(e, name="Sadoki Thread"): 
    # initialize the variables
    temperature = 0
    humidity = 0    

    # sleep for 5 seconds for sensors to initialize
    sleep(5)
    
    while not cn.EXIT_THREADS:
        logging.debug('calling ts.read()')
        temperature, humidity = ts.readsensor(temperature, humidity)
        logging.debug("Temperature: {}*C   Humidity: {}% ".format(temperature, humidity))
        logging.debug('returned from ts.read()')

        # indicate that were entering the processing mode
        led.greenBlinkerOn()
        
        # detect presence of kids or dogs or cats
        logging.debug('calling detect_object()')
        retVal, frame = od.detect_object()
        logging.debug('returned from detect_object()')
                
        # if objects found, then break from while
        if (temperature > cn.TEMP_THRESHOLD):
            if (retVal.get(cn.PERSON) or retVal.get(cn.DOG) or retVal.get(cn.CAT)):
                logging.debug('inside the alert condition')

                # turn on the green LED
                led.alarmOn()
                
                logging.debug("wait on event, or sleep for 30 second before sending out SMS")
                e.wait(30)
                
                # get GPS coordinates
                latitude = 0
                longitude = 0
                
                # send out SMS
                msgbody = "Sadoki lifeguard alert: Occupants in car with temperature: " \
                    + str(temperature)                \
                    + "| Latitude: " + str (latitude) \
                    + "| Longitude: " + str (longitude)
                logging.debug(msgbody)
                if not cn.QUIET_MODE:
                    sms.sendsms(msgbody, cn.TO_NUMBER)
                
                    # send out MMS as well
                    if cn.SEND_MMS:
                        # add temperature and GPS coordinates on to the image
                        od.addTempAndGPS(frame, temperature, latitude, longitude)

                        # write the image snapshot to a local file
                        cv2.imwrite(cn.LOCAL_SNAPSHOT_FILENAME, frame)
                        
                        # convert the local file into a publicly accessible URL for Twilio
                        # POST to Google Drive or a specicalized web service for Sadoki
                        imageurl = "EMPTY FOR NOW"
                        sms.sendmms(msgbody, imageurl, cn.TO_NUMBER)
                break
        
        # indicate that we are done processing and all is good
        led.greenBlinkerOff()
        
        # sleep for 1 minute
        logging.debug('wait for the IR sensor or for 30 seconds')
        ms.waitForMotion(30)
    
    logging.debug('Exiting sadoki thread')
    
 
    
if __name__ == '__main__':
    e = threading.Event()

    logging.debug('Start of sadoki_thread')
    st = threading.Thread(target=sadoki_thread, name="Sadoki Thread", args=(e,))
    st.start()

    logging.debug('Start of speech-to-text thread')
    stt = threading.Thread(target=speech_to_text_thread, name="STT Thread", args=(e,))
    stt.start()

    # launch the display window
    logging.debug('Launching the display window')
    # dp.launchDisplay()
    
    # Threads will exit when the cn.EXIT_THREADS flag is set to True
    # wait for threads to join
    st.join()
    stt.join()
    
    cleanup()

    
    
