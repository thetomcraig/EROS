#This class is hs preliminary emotion values
class Bot2:
	emotionDict = {"happiness": 0, "sadness": 0}
	happyRange = [0,1,2,3,4]
	sadRange = [0,1,2,3,4]	

	'''----------------------------------------------------------------------------------------'''

	def __init__(self):
		'''nothing needed now'''
		
	def printAnEmotion(self, emotion):
		'''print desired emotion from the dict'''
		print self.emotionDict[emotion]
		return
	
	def setEmotionRange(self, emotion, lowestVal):
		'''set there unique ranges, the current bot's will be in the middle'''
		if (emotion == "happiness"):
			for i in range(5):
				self.happyRange[i] = lowestVal+i
		elif (emotion == "sadness"):
			for i in range(5):
				self.sadRange[i] = lowestVal+i
		return
			
	def setEmotion(self, emotion, value):
		'''sets the bot's current emotion'''
		self.emotionDict[emotion] = value
		return	
			
	def increaseEmotion(self, emotion):
		'''increases emotion by one point'''
		if (emotion == "happiness"):
			if(emotionDict[emotion] == happyRange[4]):
				#happiness at max
				pass
			else:
				emotionDict[emotion] += 1
				
		if (emotion == "sadness"):
			if(emotionDict[emotion] == sadRange[4]):
				#sadness at max
				pass
			else:
				emotionDict[emotion] += 1
		return
		
	def decreaseEmotion(self, emotion):
		'''decreases emotion by one point'''
		if (emotion == "happiness"):
			if(emotionDict[emotion] == happyRange[0]):
				#happiness at min
				pass
			else:
				emotionDict[emotion] +- 1
				
		if (emotion == "sadness"):
			if(emotionDict[emotion] == sadRange[0]):
				#sadness at min
				pass
			else:
				emotionDict[emotion] +- 1
		return
