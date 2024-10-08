import RPi.GPIO as GPIO         # using Rpi.GPIO module
import gpiozero
from time import sleep          # import function sleep for delay
from constants import const as cn

redLED = gpiozero.LED(cn.GPIO_RED_LED)
greenLED = gpiozero.LED(cn.GPIO_GREEN_LED)
buzzer = gpiozero.Buzzer(cn.GPIO_BUZZER)

def alarmOn():
	# turn on RED and turn off GREEN
	redLED.blink(on_time=0.1, off_time=0.1)
	greenLED.off()
	if not cn.QUIET_MODE:
		buzzer.beep(on_time=0.1, off_time=0.1)

def alarmOff():
	# turn off RED and turn on GREEN
	redLED.off()
	greenLED.on()
	buzzer.off()

def greenBlinkerOn():
	greenLED.off()
	greenLED.blink(on_time=0.1, off_time=0.1)
	if not cn.QUIET_MODE:
		buzzer.beep(on_time=0.1, off_time=0.1, n=1)
	
def redBlinkerOn():
	redLED.off()
	redLED.blink(on_time=0.1, off_time=0.1)
	if not cn.QUIET_MODE:
		buzzer.beep(on_time=0.1, off_time=0.1, n=1)

def greenBlinkerOff():
	greenLED.off()

def redBlinkerOff():
	redLED.off()

def beepOnce():
	buzzer.beep(on_time=0.1, off_time=0.1, n=1)
	
def greenBlinkOnce():
	greenLED.blink(on_time=0.1, off_time=0.1, n=3)
	
def redBlinkOnce():
	redLED.blink(on_time=0.1, off_time=0.1, n=3)
