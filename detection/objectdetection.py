# start of motor module

import cv2
import numpy as np
import time
from imutils.video import VideoStream
from detection import processDNN
import argparse
import datetime
import imutils
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)


# load YOLO and DEEP NEURAL NETWORK
net =  cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

classes = []
with open("coco.names","r") as f:
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

	retVal = 0
		
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = vs.read()
		
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		return retVal

	# identify objects in the frame
	retVal = processDNN.found_object_by_name(frame, cv2, net, outputlayers, classes, colors, "person")
		
	# show the frame and record if the user presses a key
	# cv2.imshow("people view", frame)
	if retVal :
		logging.debug('Found person')
	
	return retVal
