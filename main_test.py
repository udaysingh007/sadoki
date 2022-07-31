import RPi.GPIO as GPIO         # using Rpi.GPIO module
from time import sleep          # import function sleep for delay
import threading
import logging
import cloudinary
from constants import const as cn
from detection import objectdetection as od
from temperature import thermalsensor as ts 
from sms import twilioagent as sms
from sms import postImages as pImages
from led import status as led
from motion import msensor as ms
from sound import texttospeech as tts
# from gui import display as dp
import cv2
import pyaudio
import wave
import os, sys, subprocess, contextlib

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

@contextlib.contextmanager
def ignoreStderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)
        
def test_cv():
    img = cv2.imread(cn.LOGO_IMAGE)
    od.addTempAndGPS(img, 10, 100, 1000)
    cv2.imwrite(cn.LOCAL_SNAPSHOT_FILENAME, img)
    cv2.namedWindow('LOGO', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('LOGO', img)
    cv2.waitKey()
    return

def indexOfAudioDevice():    
    p = pyaudio.PyAudio()
    for ii in range(p.get_device_count()):
        print(p.get_device_info_by_index(ii).get('name'))

def callback(in_data, frame_count, time_info, status):
    logging.debug('In the callback function, with Frame Count:' + str(frame_count))
    # data = wf.readframes(frame_count)
    return (None, pyaudio.paContinue)
    
def takeAction(line):
    acted = True
    
    if (line.find("help") >= 0):
        led.redBlinkOnce()
        led.greenBlinkOnce()
        led.beepOnce()
        return
    
    if (line.find("eep") >= 0) or (line.find("sound")>=0) or (line.find("alarm")>=0):
        led.beepOnce()
        return
        
    if (line.find("ink") >= 0):
        if (line.find("gree") >= 0):
            led.greenBlinkOnce()
        else: 
            if (line.find("red") >= 0):
                led.redBlinkOnce()
            else:
                led.greenBlinkOnce()
                led.redBlinkOnce()
        return
        
    print("No action taken, as there no action in the STT")
            
def test_stt_audio():
    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 3 # seconds to record
    dev_index = 2 # device index found by p.get_device_info_by_index(ii)
    wav_output_filename = 'test1.wav' # name of .wav file
    
    with ignoreStderr():
        audio = pyaudio.PyAudio() # create pyaudio instantiation
    
    # create pyaudio stream
    use_callback = False
    if use_callback:
        stream = audio.open(format = form_1, \
                            rate = samp_rate, \
                            channels = chans, \
                            input_device_index = dev_index, \
                            input = True, \
                            frames_per_buffer=chunk,
                            stream_callback=callback)
        # start the stream (4)
        stream.start_stream()
        
        # wait for stream to finish (5)
        while stream.is_active():
            sleep(0.1)
        
        # stop stream (6)
        stream.stop_stream()
        stream.close()
        wf.close()
        
        # close PyAudio (7)
        p.terminate()
    
    else:
        
        while True:
            stream = audio.open(format = form_1, \
                                rate = samp_rate, \
                                channels = chans, \
                                input_device_index = dev_index, \
                                input = True, \
                                frames_per_buffer=chunk)

            frames = []
            print("start recording")
            # loop through stream and append audio chunks to frame array
            for ii in range(0,int((samp_rate/chunk)*record_secs)):
                data = stream.read(chunk,exception_on_overflow=False)
                frames.append(data)
            print("finished recording")

            # save the audio frames as .wav file
            wavefile = wave.open(wav_output_filename,'wb')
            wavefile.setnchannels(chans)
            wavefile.setsampwidth(audio.get_sample_size(form_1))
            wavefile.setframerate(samp_rate)
            wavefile.writeframes(b''.join(frames))
            wavefile.close()

            # convert the .wav file into text
            print("start speech-to-text")
            s = subprocess.run(["spchcat", "--stream", "1600", \
				"--hot_words", "help:20,red:20,green:20,blink:20,sound:20,alarm:20", \
				wav_output_filename], stdout=subprocess.PIPE,\
				stderr=subprocess.PIPE, text=True)
            print(s.stdout)
            takeAction(s.stdout)
            print("finished speech-to-text")

            # delete the file as it is no longer required
            subprocess.run(["rm", "-rf", wav_output_filename], capture_output=True)

            # stop the stream, close it, and terminate the pyaudio instantiation
            stream.stop_stream()
            stream.close()

            #sleep a second for the file to be written
            sleep(0.2)

        audio.terminate()
    
    
if __name__ == '__main__':

    # test audio speech to text (STT)
    # test_stt_audio()
    
    # convert the local file into a publicly accessible URL for Twilio
    # POST to Google Drive or a specicalized web service for Sadoki
    # imageurl = pImages.uploadFile(cn.LOCAL_SNAPSHOT_FILENAME)
    # sms.sendmms("Test", imageurl, cn.TO_NUMBER)
    
    logging.debug("About to blink green")
    c = input('press enter')
    tts.speakOut("Blinking Green L.E.D!  Blinking Green L.E.D!")
    led.greenBlinkerOn()
    sleep(3)
    led.greenBlinkerOff()
    
    logging.debug("About to blink red")
    c = input('press enter')
    tts.speakOut("Blinking Red L.E.D!  Blinking Red L.E.D!")
    led.redBlinkerOn()
    sleep(3)
    led.redBlinkerOff()

    logging.debug("About to blink all LEDs")
    c = input('press enter')
    tts.speakOut("Blinking all L.E.Ds!  Blinking all L.E.D!")
    led.redBlinkerOn()
    led.greenBlinkerOn()
    sleep(3)
    led.redBlinkerOff()
    led.greenBlinkerOff()
    
    logging.debug("Sound alarm")
    c = input('press enter')
    tts.speakOut("Danger!  Danger!   Occcupants left behind in the car!")
    led.redBlinkerOn()
    led.greenBlinkerOn()
    led.beepOnce()
    sleep(3)
    tts.speakOut("Danger!  Danger!   Occcupants left behind in the car!")
    led.redBlinkerOff()
    led.greenBlinkerOff()
    

    
