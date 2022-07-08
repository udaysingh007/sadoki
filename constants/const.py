# const.py - list of all constants
import board

# paths of weights, config, and coco.names
YOLOV3_WEIGHTS = "/home/pi/sadoki/yolov3.weights"
YOLOV3_CONFIG = "/home/pi/sadoki/yolov3.cfg"
COCO_NAMES = "/home/pi/sadoki/coco.names"

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

