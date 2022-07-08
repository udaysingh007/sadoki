# start of motor module

import cv2
import numpy as np
from time import sleep          # import function sleep for delay
from imutils.video import VideoStream
from detection import processDNN
from constants import const as cn
import argparse
import datetime
import imutils
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

# load YOLO and DEEP NEURAL NETWORK
net =  cv2.dnn.readNet(cn.YOLOV3_WEIGHTS, cn.YOLOV3_CONFIG)

# load up all the class names
classes = []
with open(cn.COCO_NAMES,"r") as f:
	classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors= np.random.uniform(0,255,size=(len(classes),3))

# reading from webcam
vs = VideoStream(src=0).start()

def rotate_image(frame, angle):
	(h, w) = frame.shape[:2]
	# calculate the center of the image
	center = (w / 2, h / 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotated = cv2.warpAffine(frame, M, (w, h))
	return rotated;

def detect_object():

	# initialize the first frame in the video stream
	firstFrame = None

	retVal = {cn.PERSON: 0, cn.DOG: 0, cn.CAT: 0}
		
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = vs.read()
		
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		return retVal

	# identify objects in the frame
	objectnames = [cn.PERSON, cn.DOG, cn.CAT]
	retVal = processDNN.find_object_by_name(frame, cv2, net, outputlayers, classes, colors, objectnames)
	print(retVal)
		
	if (retVal.get(cn.PERSON) or retVal.get(cn.DOG) or retVal.get(cn.CAT)):
		logging.debug('Found car occupants; human: ' + str(retVal.get(cn.PERSON)) 
		                                  + ' pets:' + str(retVal.get(cn.DOG)+retVal.get(cn.CAT)))
		
		# rotate the image by 180, as the webcam is offset by 180 degrees
		frame = rotate_image(frame, 180)
		
		cv2.imshow("people view", frame)
		
		# wait for user input
		# cv2.waitKey(0) 
		sleep(30)
  
		#closing all open windows 
		cv2.destroyAllWindows() 
	
	return retVal
