
'''
total key presses
time keys pressed

'''
import pdb
class LogReader:

	def __init__(self,filename):

		self.file=open(filename)
		self.rawFeatures=[]	#format: [keyName,keyState,time]
		self.laps=[]		#format: [lapnumber,time]					
		self.perLap=[]		#format: [[lap1 rawFeatures],[lap2 rawFeatures]]
		self.totalKeyPressTimesTimes=[0,0,0,0,0,0,0]	#format: [0,up,left,right,down,ctrl,space]
		self.perLapKeyData=[]  	#format: [lapnumber,keyTimes,timesPressed]
		self.timesPressed=[0,0,0,0,0,0,0] #format: [0,up,left,right,down,ctrl,space]

		
		self.keyPressesPerLap=[] #format:[[],lap1[keyPresses],lap2[keyPresses]]

		self.firstPress=0				#to store first key press time to calculate first lap time

		self.read()
		self.calcLapTimes()
		self.findKeyPresses()
	def read(self):
		
		tmp=[]

		keyStack=[0,0,0,0,0,0,0] #format: [0,up,left,right,down,ctrl,space]

		flag=True

		for line in self.file:
			if line=='\n':			#skip empty lines
				continue
			record = line.split(',')
			if 'Log ' in record[0] or 'Car ' in record[0]:
				continue			#skip over log generation date and car name lines

			if 'lap ' in record[0]:
				lapInfo=record[0].split(' ')
				del lapInfo[0]
				lapInfo.append(tmp)			#store [lapNo,[rawFeatures]]
				self.perLap.append(lapInfo)
				tmp=[]

				self.laps.append(self.extractLaps(record))
				continue


			record[0]=self.keyNameToNumber(record[0])		#convert keynames to numbers
			record[1]=self.keyStateToNumber(record[1])		#convert key state to number 0=pressed 1=released
			record[2]=self.convertTime(record[2])			#extract seconds

			

			tmp.append(record)		#stores per-lap raw data

			self.rawFeatures.append(record)



			#later used to find first lap time
			if flag==True:
				flag=False;
				self.firstPress=record[2]

				#to calculate total times a key was presssed:
			keyCode=record[0]
			keyState=record[1]
			keyTimestamp=record[2]
			if keyState==0:		#key pressed
				keyStack[keyCode]=keyTimestamp
			elif keyState==1:		#key released
				self.totalKeyPressTimesTimes[keyCode]+=(keyTimestamp-keyStack[keyCode])
				self.timesPressed[keyCode]+=1


		#print self.rawFeatures
		#print self.laps
		#print self.perLap
		#print self.totalKeyPressTimesTimes
		#print self.timesPressed
		#print self.firstPress
		
	def calcLapTimes(self):						#calculates time taken for each lap

		previousTime=self.firstPress
		for i in range(0,len(self.laps)):
			tmp=self.laps[i][1]
			self.laps[i][1]-=previousTime
			previousTime=tmp

	def findKeyPresses(self):

		tup=0
		tleft=0
		tright=0
		tdown=0
		tctrl=0
		tspace=0
		for lap in self.perLap:
			x=[0,0,0,0,0,0,0]						#[0,up,left,right,down,ctrl,space]
			#up=left=right=down=ctrl=space=[]		never do
			left=[]
			right=[]
			down=[]
			ctrl=[]
			space=[]
			up=[]

			totalKeyPressTimes=[0,0,0,0,0,0,0]			#[0,up,left,right,down,ctrl,space]
			totalKeyPresses=[0,0,0,0,0,0,0]			#[0,up,left,right,down,ctrl,space]

			for rawFeature in lap[1]:
				
				if rawFeature[0]==1:		#up
					
					if rawFeature[1]==0:	#pressed
						tup=rawFeature[2]
					elif rawFeature[1]==1:	#released
						timePressed=rawFeature[2]-tup
						up.append(timePressed)

						totalKeyPressTimes[1]+=timePressed
						totalKeyPresses[1]+=1
				
				elif rawFeature[0]==2:		#left
					
					if rawFeature[1]==0:
						tleft=rawFeature[2]
					elif rawFeature[1]==1:
						timePressed=rawFeature[2]-tleft
						left.append(timePressed)

						totalKeyPressTimes[2]+=timePressed
						totalKeyPresses[2]+=1
					  
				elif rawFeature[0]==3:		#right
					
					if rawFeature[1]==0:
						tright=rawFeature[2]
					elif rawFeature[1]==1:
						timePressed=rawFeature[2]-tright
						right.append(timePressed)

						totalKeyPressTimes[3]+=timePressed
						totalKeyPresses[3]+=1

				elif rawFeature[0]==4:		#down
					
					if rawFeature[1]==0:
						tdown=rawFeature[2]
					elif rawFeature[1]==1:
						timePressed=rawFeature[2]-tdown
						down.append(timePressed)

						totalKeyPressTimes[4]+=timePressed
						totalKeyPresses[4]+=1
				
				elif rawFeature[0]==5:      #ctrl
				
					if rawFeature[1]==0:
						tctrl=rawFeature[2]
					elif rawFeature[1]==1:
						timePressed=rawFeature[2]-tctrl
						ctrl.append(timePressed)

						totalKeyPressTimes[5]+=timePressed
						totalKeyPresses[5]+=1

				elif rawFeature[0]==6:      #space
					
					if rawFeature[1]==0:
						tspace=rawFeature[2]
					elif rawFeature[1]==1:
						timePressed=rawFeature[2]-tspace
						space.append(timePressed)	

						totalKeyPressTimes[6]+=timePressed
						totalKeyPresses[6]+=1	
						
			x[1]=up
			x[2]=left
			x[3]=right
			x[4]=down
			x[5]=ctrl
			x[6]=space
			
			self.keyPressesPerLap.append([lap[0],x])
			self.perLapKeyData.append([lap[0],totalKeyPressTimes,totalKeyPresses])
			
		
		
	def extractLaps(self,record):

		lapInfo=record[0].split(' ')
		del lapInfo[0]
		lapInfo.append(self.convertTime(record[1]))	#extract seconds
		#lapInfo now has [lapNumber,time]
		return lapInfo

	def convertTime(self,time):		

		#returns time in seconds
		
		h, m, s = time.split(':')
		s=s[:-1]						#remove newline character from seconds
		return float(h) * 3600 + float(m) * 60 + float(s)
		


	def keyNameToNumber(self,keyName):		

		if keyName=="UP":
			return 1
		if keyName=="LEFT":
			return 2
		if keyName=="RIGHT":
			return 3
		if keyName=="DOWN":
			return 4
		if keyName=="CTRL":
			return 5
		if keyName=="SPACE":
			return 6 

	def keyStateToNumber(self,keyState):	#0=pressed 1=released

		if keyState=="PRESSED":
			return 0
		if keyState=="RELEASED":
			return 1		

	def printData(self):

		print "Key 'UP' was pressed ",self.timesPressed[1]," times. Pressed for ",self.totalKeyPressTimesTimes[1]," seconds."
		print "Key 'LEFT' was pressed ",self.timesPressed[2]," times. Pressed for ",self.totalKeyPressTimesTimes[2]," seconds."
		print "Key 'RIGHT' was pressed ",self.timesPressed[3]," times. Pressed for ",self.totalKeyPressTimesTimes[3]," seconds."
		print "Key 'DOWN' was pressed ",self.timesPressed[4]," times. Pressed for ",self.totalKeyPressTimesTimes[4]," seconds."
		print "Key 'CTRL' was pressed ",self.timesPressed[5]," times. Pressed for ",self.totalKeyPressTimesTimes[5]," seconds."
		print "Key 'SPACE' was pressed ",self.timesPressed[6]," times. Pressed for ",self.totalKeyPressTimesTimes[6]," seconds."

		for i in self.laps:
			print "Lap ",i[0]," lasted for ",i[1]," seconds."

		for i in self.perLapKeyData:
			print "------------------------------LAP ",i[0],"-----------------------------------"
			print "Key 'UP' was pressed ",i[2][1],"times. Pressed for ",i[1][1]," seconds."	
			print "Key 'LEFT' was pressed ",i[2][2],"times. Pressed for ",i[1][2]," seconds."
			print "Key 'RIGHT' was pressed ",i[2][3],"times. Pressed for ",i[1][3]," seconds."
			print "Key 'DOWN' was pressed ",i[2][4],"times. Pressed for ",i[1][4]," seconds."
			print "Key 'CTRL' was pressed ",i[2][5],"times. Pressed for ",i[1][5]," seconds."
			print "Key 'SPACE' was pressed ",i[2][6],"times. Pressed for ",i[1][6]," seconds."


		''' raw data printing
		for x in self.keyPressesPerLap:
			print "-------------LAP ",x[0],'------------------------'
			print 'up ',len(x[1][1]),x[1][1]
			print 'left ',len(x[1][2]),x[1][2]
			print 'right ',len(x[1][3]),x[1][3]
			print 'down ',len(x[1][4]),x[1][4]
			print 'ctrl ',len(x[1][5]),x[1][5]
			print 'space ',len(x[1][6]),x[1][6]
		'''
		



if(__name__=="__main__"):
	l=LogReader("manasLog.txt")
	l.printData()
	
	