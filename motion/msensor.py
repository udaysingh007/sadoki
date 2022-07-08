import RPi.GPIO as GPIO         # using Rpi.GPIO module
from gpiozero import MotionSensor
from time import sleep          # import function sleep for delay
from constants import const as cn

pir = MotionSensor(cn.GPIO_IR_SENSOR)

def waitForMotion(timeout=None):
	pir.wait_for_motion(timeout)
