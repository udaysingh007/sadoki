from mobility import cytronmotor 
import RPi.GPIO as GPIO         # using Rpi.GPIO module
from time import sleep          # import function sleep for delay
import threading
import logging
from detection import objectdetection

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
    

def init_motor_movement(e):
    logging.debug('Motor start');
    cytronmotor.move_forward(0);
    e.wait();
    #sleep(5);
    cytronmotor.move_stop();
	    	
def init_object_detection(e,t):
    logging.debug('Sleep - object detection')
    sleep(t);
    logging.debug('Calling Event.set() - Object detection')
    objectdetection.detect_object();
    e.set();
    logging.debug('Stop - Object detection')
    
def wait_for_event(e):
    logging.debug('wait_for_event starting')
    event_is_set = e.wait()
    logging.debug('event set: %s', event_is_set)

def wait_for_event_timeout(e, t):
    while not e.isSet():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other things')

if __name__ == '__main__':
    
    
    e = threading.Event()
    
    mobilityThread = threading.Thread(name='Mobility thread', 
                      target=init_motor_movement, 
                      args=(e, ))
    mobilityThread.start()
    
    detectionThread = threading.Thread(name='Object Detection thread', 
                      target=init_object_detection, 
                      args=(e, 10))
    detectionThread.start()
    
    
    
    logging.debug('Exiting Main thread ')
    
    #sleep(15);



    
    
