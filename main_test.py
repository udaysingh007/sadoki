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
import cv2

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

if __name__ == '__main__':
    img = cv2.imread(cn.LOGO_IMAGE)
    od.addTempAndGPS(img, 10, 100, 1000)
    cv2.namedWindow('LOGO', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('LOGO', img)
    cv2.waitKey()

