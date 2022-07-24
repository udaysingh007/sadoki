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
		return retVal, frame

	# identify objects in the frame
	objectnames = [cn.PERSON, cn.DOG, cn.CAT]
	retVal = processDNN.find_object_by_name(frame, cv2, net, outputlayers, classes, colors, objectnames)
	print(retVal)
		
	if (retVal.get(cn.PERSON) or retVal.get(cn.DOG) or retVal.get(cn.CAT)):
		logging.debug('Found car occupants; human: ' + str(retVal.get(cn.PERSON)) 
		                                  + ' pets:' + str(retVal.get(cn.DOG)+retVal.get(cn.CAT)))
		
		# rotate the image by 180, as the webcam is offset by 180 degrees
		# frame = rotate_image(frame, 180)
		
		# cv2.imshow("people view", frame)
		
		# wait for user input
		# cv2.waitKey(0) 
		# sleep(30)
  
		# closing all open windows 
		# cv2.destroyAllWindows() 
	
	return retVal, frame

def addTempAndGPS(frame, temperature, latitude, longitude):
	
	font = cv2.FONT_HERSHEY_PLAIN

	boxWidth = 200
	boxHeight = 16
	gap = 5
	color = (10, 10, 10)
	
	# add temperature on the image
	cv2.rectangle(frame,(0,0),(boxWidth,boxHeight),color,2)
	cv2.putText(frame,"Temperature: " + str(temperature),(2,boxHeight-2),font,1,color,2)

	# add latitude on the image
	# TODO: Need to properly format the latitude
	cv2.rectangle(frame,(0,boxHeight+gap),(boxWidth,2*boxHeight+gap),color,2)
	cv2.putText(frame,"Latitude (GPS): " + str(latitude),(2,2*boxHeight+gap-2),font,1,color,2)

	# add longitude on the image
	# TODO: Need to properly format the longitude
	cv2.rectangle(frame,(0,2*(boxHeight+gap)),(boxWidth,3*boxHeight+2*gap),color,2)
	cv2.putText(frame,"Longitude (GPS): " + str(longitude),(2,3*boxHeight+2*gap-2),font,1,color,2)
