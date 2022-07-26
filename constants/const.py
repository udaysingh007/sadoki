# const.py - list of all constants
import board
import pyaudio

# Serial Number of this unit
SADOKI_SERIAL_NUM = "00000001"

# Global flag to stop threads
EXIT_THREADS = False

# turn off sounds and sms while in quiet mode
QUIET_MODE = True
SEND_SMS = True
SEND_MMS = True

# paths of weights, config, and coco.names
HOME_DIR="/home/pi/sadoki/"
YOLOV3_WEIGHTS = HOME_DIR+"yolov3.weights"
YOLOV3_CONFIG = HOME_DIR+"yolov3.cfg"
COCO_NAMES = HOME_DIR+"coco.names"
LOGO_IMAGE = HOME_DIR+"sadoki_logo.jpg"
LOCAL_SNAPSHOT_FILENAME = HOME_DIR+"snapshot.jpg"

# GUI STRING
GUI_TITLE = "Sadoki"

# for SMS messaging
ACCOUNT_SID = 'AC90500fd622ea00db67e19e8e44854c30'
AUTH_TOKEN = 'cb5c15ea61240b726acfdf148d3eb84f'
FROM_NUMBER = '+12513027736'
TO_NUMBER = '+19175824874'

# thresholds
TEMP_THRESHOLD = 19

# GPIO PINS used
GPIO_RED_LED = 17
GPIO_GREEN_LED = 18
GPIO_IR_SENSOR = 22
DHT_PIN = 23  # board.D23
GPIO_BUZZER = 27

# string constants
PERSON = "person"
DOG = "dog"
CAT = "cat"

# speech processing related constants
AUDIO_FORMAT = pyaudio.paInt16 	# 16-bit resolution
AUDIO_NUM_CHANNELS = 1 			# 1 channel
AUDIO_SAMPLING_RATE = 44100 	# 44.1kHz sampling rate
AUDIO_CHUNK_SIZE = 4096 		# 2^12 samples for buffer
AUDIO_RECORDING_TIME = 3 		# seconds to record
AUDIO_DEVICE_INDEX = 2 			# device index found by p.get_device_info_by_index(ii)
AUDIO_TEMP_OUTPUT_FILE = HOME_DIR+'test1.wav' 

# GPS
UART_PORT="/dev/ttyAMA0"

# constants for CLOUDINARY
CLOUDINARY_NAME = "sadoki-monitor-kids-and-pets-left-behind-in-the-car" 
CLOUDINARY_API_KEY = "989645534825673"
CLOUDINARY_API_SECRET = "xAP3vUE7pbgkZcwRqbyiM_DcpAs" 
CLOUDINARY_TAG = "SADOKI_"+SADOKI_SERIAL_NUM
