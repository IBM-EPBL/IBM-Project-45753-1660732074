import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

class Video(object): 
	def __init__(self):
		self.video = cv2.VideoCapture(0)
		self.roi_start = (50, 150)
		self.roi_end = (250, 350)
		#self.model = load_model('asl_model.h5') # Execute Local Trained Model
		self.model = load_model('realtime.h5') # Execute IBM Trained Model
		self.index=['A','B','C','D','E','F','G','H','I']
		self.y = None
	def __del__(self):
		k = cv2.waitKey(1)
	    
		self.video.release()
	def get_frame(self):
		ret,frame = self.video.read()
		frame = cv2.resize(frame,(640,480))
		copy = frame.copy()
		copy = copy[150:150+200,50:50+200]
		# prediction starts 
		cv2.imwrite('image.jpg',copy)
		copy_img = image.load_img('image.jpg', target_size=(64,64,3))
		x = image.img_to_array(copy_img)
		x = np.expand_dims(x, axis=0)
		pred = np.argmax(self.model.predict(x), axis=1)
		self.y = pred[0]
		cv2.putText(frame,'The Predicted Alphabet is: '+str(self.index[self.y]),(100,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3)
		ret,jpg = cv2.imencode('.jpg', frame)
		return jpg.tobytes()