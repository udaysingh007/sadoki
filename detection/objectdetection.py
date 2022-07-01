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
# net =  cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
net =  cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

classes = []
with open("coco.names","r") as f:
	classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors= np.random.uniform(0,255,size=(len(classes),3))

def rotate_image(frame, angle):
	(h, w) = frame.shape[:2]
	# calculate the center of the image
	center = (w / 2, h / 2)
	M = cv2.getRotationMatrix2D(center, 180, 1.0)
	rotated = cv2.warpAffine(frame, M, (w, h))
	return rotated;

def detect_object():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", help="path to the video file")
	ap.add_argument("-a", "--min-area", type=int, default=30000, help="minimum area size")
	args = vars(ap.parse_args())

	# if the video argument is None, then we are reading from webcam
	if args.get("video", None) is None:
		vs = VideoStream(src=0).start()
		time.sleep(2.0)

	# otherwise, we are reading from a video file
	else:
		vs = cv2.VideoCapture(args["video"])

	# initialize the first frame in the video stream
	firstFrame = None

	count = 0
	retVal = 0

	# loop over the frames of the video
	while True:
		
		# grab the current frame and initialize the occupied/unoccupied
		# text
		frame = vs.read()
		frame = frame if args.get("video", None) is None else frame[1]
		

		# if the frame could not be grabbed, then we have reached the end
		# of the video
		if frame is None:
			break

		# identify objects in the frame
		retVal = processDNN.found_object_by_name(frame, cv2, net, outputlayers, classes, colors, "person")
		# show the frame and record if the user presses a key
		cv2.imshow("Grobot View", frame)
		if retVal :
			logging.debug('Found person')
			break
