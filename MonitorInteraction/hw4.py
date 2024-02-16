import numpy as np 
import cv2 
import webbrowser

cap = cv2.VideoCapture(0)
subtractor = cv2.createBackgroundSubtractorMOG2(history=30, varThreshold=30)
h=50
w=115

leftstart=85
rightstart=490

upstart=40
downstart=340

closekey=False
first=True

threshold=50

added = np.zeros((h, w), np.uint8)
added2 = np.zeros((h, w), np.uint8)
added3 = np.zeros((h, w), np.uint8)
added4 = np.zeros((h, w), np.uint8)

count=0

def getacol(img):
    avglist=[]
    for i in range(h):
        avg=sum(img[i])/len(img[i])
        avglist.append(avg)
    avg=sum(avglist)/h
    return avg


cv2.namedWindow('frame',0)
cv2.resizeWindow('frame',640,480)



while(True):
	ret, frame = cap.read()
	frame = cv2.flip(frame,1)
	mask = subtractor.apply(frame)

	cimg1 = mask[upstart:upstart+h, leftstart:leftstart+w]
	cimg2 = mask[downstart:downstart+h, leftstart:leftstart+w]
	cimg3 = mask[upstart:upstart+h, rightstart:rightstart+w]
	cimg4 = mask[downstart:downstart+h, rightstart:rightstart+w]
    
	text1='show'
	text2='gray'
	text3='exit'
	text4='takpic'
    
	cv2.putText(frame, text1, (leftstart+15, upstart+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1, cv2.LINE_AA)
	cv2.putText(frame, text2, (leftstart+15, downstart+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1, cv2.LINE_AA)
	cv2.putText(frame, text3, (rightstart+10, upstart+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1, cv2.LINE_AA)
	cv2.putText(frame, text4, (rightstart+10, downstart+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1, cv2.LINE_AA)
    
	cv2.rectangle(frame, (leftstart, upstart), (leftstart+w, upstart+h), (0, 255, 0), 2)
	cv2.rectangle(frame, (leftstart, downstart), (leftstart+w, downstart+h), (0, 255, 0), 2)
	cv2.rectangle(frame, (rightstart, upstart), (rightstart+w, upstart+h), (0, 255, 0), 2)
	cv2.rectangle(frame, (rightstart, downstart), (rightstart+w, downstart+h), (0, 255, 0), 2)
	cv2.imshow('frame',frame)

	if count<31:
		added = cv2.add(added,cimg1)
		added2 = cv2.add(added2,cimg2)
		added3 = cv2.add(added3,cimg3)
		added4 = cv2.add(added4,cimg4)

		count+=1
	else:
		if first==False:
			picture = cv2.imread('pic.jpg')

			firstsection=getacol(added)
			secondsection=getacol(added2)
			thirdsection=getacol(added3)
			forthsection=getacol(added4)

			if firstsection>threshold:
				cv2.imshow('picture',picture)
				print('show the picture.')

			if secondsection>threshold:
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				cv2.imshow('frame',gray)
				print('turn your camera to grayscale.')

			if thirdsection>threshold:
				closekey=True
				print('close the window')


			if forthsection>threshold:
				cv2.imwrite("mypicture.jpg", frame)
				print('your face camera picture is taken.')

		else:
			first=False





		added.fill(0)
		added2.fill(0)
		added3.fill(0)
		added4.fill(0)
		count=0
		if (cv2.waitKey(1) & 0xFF == ord('q')) or (closekey==True):
			break

cap.release()
cv2.destroyAllWindows()