import cv2
import numpy as np
import time

font = cv2.FONT_HERSHEY_PLAIN
def found_object_by_name(frame, cv2, net, outputlayers, classes, colors, objectname):
	starting_time = time.time()
	height,width,channels = frame.shape
	#detecting objects
	blob = cv2.dnn.blobFromImage(frame,0.00392,(320,320),(0,0,0),True,crop=False) #reduce 416 to 320    


	net.setInput(blob)
	outs = net.forward(outputlayers)
	#print(outs[1])


	#Showing info on screen/ get confidence score of algorithm in detecting an object in blob
	class_ids=[]
	confidences=[]
	boxes=[]
	for out in outs:
		for detection in out:
			scores = detection[5:]
			class_id = np.argmax(scores)
			confidence = scores[class_id]
			if confidence > 0.2:
				#onject detected
				center_x= int(detection[0]*width)
				center_y= int(detection[1]*height)
				w = int(detection[2]*width)
				h = int(detection[3]*height)

				#cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
				#rectangle co-ordinaters
				x=int(center_x - w/2)
				y=int(center_y - h/2)
				#cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

				boxes.append([x,y,w,h]) #put all rectangle areas
				confidences.append(float(confidence)) #how confidence was that object detected and show that percentage
				class_ids.append(class_id) #name of the object tha was detected

	indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

	retVal = 0

	for i in range(len(boxes)):
		if i in indexes:
			x,y,w,h = boxes[i]
			label = str(classes[class_ids[i]])
			if (label == objectname):
				retVal = 1
			confidence= confidences[i]
			color = colors[class_ids[i]]
			cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
			cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(255,255,255),2)


	elapsed_time = time.time() - starting_time
	print ("Time:"+str(elapsed_time))

	# cv2.putText(frame, "TIME:"+str(round(elapsed_time,2)), (10,50), font, 2, (0,0,0), 1)
	# cv2.imshow("DNN Image",frame)
	return retVal;
	
