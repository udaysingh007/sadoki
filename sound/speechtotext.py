from time import sleep          # import function sleep for delay
import logging
import threading
from constants import const as cn
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
        
############################################################
# indexOfAudioDevice()
# This is a one-time setup function useful to determin the 
# index of the serial USB port that the microphone is plugged 
# into 
############################################################
def indexOfAudioDevice():    
    p = pyaudio.PyAudio()
    for ii in range(p.get_device_count()):
        print(p.get_device_info_by_index(ii).get('name'))

    
def takeAction(line, e):
	acted = False
	helpInvoked = False
	
	if (line.find("elp")>=0):
		helpInvoked = True
		# wake up the main thread to send out SMS after temperature 
		# and occupancy check
		e.set()
    
	if (line.find("eep") >= 0):
		led.beepOnce()
		acted = True
    
	if (line.find("ink") >= 0):
		if (line.find("gree") >= 0):
			led.greenBlinkOnce()
		else: 
			if (line.find("red") >= 0):
				led.redBlinkOnce()
			else:
				led.greenBlinkOnce()
				led.redBlinkOnce()
		acted = True
        
	if not acted:
		logging.debug("No action taken, as there no action in the STT")

def cleanup():
	return
	
def processSpeech(e):
	form_1 = cn.AUDIO_FORMAT
	chans = cn.AUDIO_NUM_CHANNELS
	samp_rate = cn.AUDIO_SAMPLING_RATE
	chunk = cn.AUDIO_CHUNK_SIZE
	record_secs = cn.AUDIO_RECORDING_TIME
	dev_index = cn.AUDIO_DEVICE_INDEX
	wav_output_filename = cn.AUDIO_TEMP_OUTPUT_FILE
    
	with ignoreStderr():
		audio = pyaudio.PyAudio() # create pyaudio instantiation
		stream = audio.open(format = form_1, \
						rate = samp_rate, \
						channels = chans, \
						input_device_index = dev_index, \
						input = True, \
						frames_per_buffer=chunk)

	while not cn.EXIT_THREADS:
		frames = []
		logging.debug("processSpeech: start recording")        
		# loop through stream and append audio chunks to frame array
		for ii in range(0,int((samp_rate/chunk)*record_secs)):
			data = stream.read(chunk,exception_on_overflow=False)
			frames.append(data)
		logging.debug("processSpeech: finished recording")

		# save the audio frames as .wav file            
		wavefile = wave.open(wav_output_filename,'wb')
		wavefile.setnchannels(chans)
		wavefile.setsampwidth(audio.get_sample_size(form_1))
		wavefile.setframerate(samp_rate)
		wavefile.writeframes(b''.join(frames))
		wavefile.close()

		# sleep a second for the file to be written
		# sleep(1)

		# convert the .wav file into text
		logging.debug("processSpeech:start speech-to-text")        
		s = subprocess.run(["spchcat", "--stream", "1600", \
			"--hot_words", "help:20,red:20,green:20,blink:20,sound:20,alarm:20", \
			wav_output_filename], stdout=subprocess.PIPE,\
			stderr=subprocess.PIPE, text=True)
		logging.debug(f'processSpeech: STDOUT: {s.stdout}')
		takeAction(s.stdout, e)
		logging.debug("processSpeech:finished speech-to-text")        

		# delete the file as it is no longer required
		subprocess.run(["rm", "-rf", wav_output_filename], capture_output=True)

		#sleep a second for the file to be written
		sleep(0.2)

	# stop the stream, close it, and terminate the pyaudio instantiation
	stream.stop_stream()
	stream.close()

	audio.terminate()
