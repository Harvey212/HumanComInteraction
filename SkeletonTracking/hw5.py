#!pip install mediapipe opencv-python
import cv2
import pip

def install(package):
	if hasattr(pip, 'main'):
		pip.main(['install', package])
	else:
		pip._internal.main(['install', package])

try:
	import mediapipe as mp
except ImportError:
	install('mediapipe')
finally:
	import mediapipe as mp

######################
#for button exit
closekey=False

####################
#for rectangle adjustment
h=50
w=115
#####################
#for text adjustment
textadjX=15
textadjY=30
#####################
#for button positions
leftstart=85
rightstart=490

upstart=40
middle1=140
middle2=240
downstart=340
######################3
#mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
##################
#window setting
width=640  
height=480  

cv2.namedWindow('hw_5', 0)
cv2.resizeWindow('hw_5', width, height)
cap = cv2.VideoCapture(0)
#########################

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
	while cap.isOpened():
		########################
		#frame design setting
		ret, frame = cap.read()
		frame = cv2.flip(frame,1)

		text1='takpic'
		text2='gray'
		text3='show'
		text4='exit' 

		cv2.putText(frame, text1, (leftstart+textadjX, upstart+textadjY), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1, cv2.LINE_AA)
		cv2.putText(frame, text2, (leftstart+textadjX, middle1+textadjY), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1, cv2.LINE_AA)
		cv2.putText(frame, text3, (leftstart+textadjX, middle2+textadjY), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1, cv2.LINE_AA)
		cv2.putText(frame, text4, (leftstart+textadjX, downstart+textadjY), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1, cv2.LINE_AA)
		
		cv2.rectangle(frame, (leftstart, upstart), (leftstart+w, upstart+h), (0, 255, 0), 2)
		cv2.rectangle(frame, (leftstart, middle1), (leftstart+w, middle1+h), (0, 255, 0), 2)
		cv2.rectangle(frame, (leftstart, middle2), (leftstart+w, middle2+h), (0, 255, 0), 2)
		cv2.rectangle(frame, (leftstart, downstart), (leftstart+w, downstart+h), (0, 255, 0), 2)
		
		picture = cv2.imread('pic.jpg')
		############################################
		# Recolor Feed
		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		image.flags.writeable = False        
        
		# Make Detections
		results = holistic.process(image)
        
        # Recolor image back to BGR for rendering
		image.flags.writeable = True   
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		#####################################################
		#for buttons
		store=[]
		store2=[]
		store3=[]
		store4=[]
		##############3##########################
		#to see if right hand index finger is within the button range
		if results.left_hand_landmarks:

			tar=results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP.value]
			myX=tar.x*width
			myY=tar.y*height

			if (myX>leftstart) and (myX<leftstart+w) and (myY>upstart) and (myY<upstart+h):
				store.append(myX)
				store.append(myY)

			if (myX>leftstart) and (myX<leftstart+w) and (myY>middle1) and (myY<middle1+h):
				store2.append(myX)
				store2.append(myY)

			if (myX>leftstart) and (myX<leftstart+w) and (myY>middle2) and (myY<middle2+h):
				store3.append(myX)
				store3.append(myY)

			if (myX>leftstart) and (myX<leftstart+w) and (myY>downstart) and (myY<downstart+h):
				store4.append(myX)
				store4.append(myY)

		###################################################
        # 1. Draw face landmarks
		mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                 )
        
        # 2. Right hand
		mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                 )

        # 3. Left Hand
		mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                 )

        # 4. Pose Detections
		mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )

		############################################################
		cv2.imshow('hw_5', image)

		if len(store)!=0:
			cv2.imwrite("mypicture.jpg", image)
			print('your face camera picture is taken.')

		if len(store2)!=0:
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			cv2.imshow('hw_5',gray)
			print('turn your camera to grayscale.')

		if len(store3)!=0:
			cv2.imshow('picture',picture)
			print('show the picture.')

		if len(store4)!=0:
			closekey=True
			print('close the window')
		
		if (cv2.waitKey(10) & 0xFF == ord('q')) or (closekey==True):
			break
		#################################################


cap.release()
cv2.destroyAllWindows()