import RPi.GPIO as GPIO         # using Rpi.GPIO module
from temperature import thermalsensor as ts 

def cleanup():
    ts.cleanup()
    GPIO.cleanup()

# invoke cleanup
cleanup()
