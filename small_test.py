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
import pyaudio
import wave
import os, sys, subprocess, contextlib
from location import gps

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def testGPS():
    # Test out GPS
    lat, lng = gps.getLatNLng()
    logging.debug("Lat: " + lat + "; lng: " + lng)

def testSMS():
    sms.sendsms("Testing", cn.TO_NUMBER)

if __name__ == '__main__':
    # wav_output_filename = 'test.wav' # name of .wav file
            
    # # convert the .wav file into text
    # print("start speech-to-text")        
    # s = subprocess.run(["spchcat", wav_output_filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # print(s.stdout)
    # print(s.stderr)
    # print("finished speech-to-text")        
        
    # test = "My name"
    # print(test.find("is"))

    testSMS()
    
