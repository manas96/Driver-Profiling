import matplotlib.pyplot as plt
from LogReader import LogReader
import math
import numpy as np
from sklearn import svm
from sklearn import linear_model

keys=[1,2,3,4,5,6]
up=1
left=2
right=3
down=4
ctrl=5
space=6

class Frequency:
	def __init__(self,fileName,playerName):
		self.data=LogReader(fileName)
		self.name=playerName
		self.x=self.getXValues()
		self.up=[]				#to store frequency array per lap [[lap1 freq.array],[lap2 freq.array]]
		self.left=[]
		self.right=[]
		self.down=[]
		self.ctrl=[]
		self.space=[]
		self.laps=len(self.data.laps)
		counter=0
		for i in self.data.perLap:
			lapStartTime=self.data.lapStartTimes[counter]
			u,l,r,d,c,s=self.getKeyFreq(i[1],lapStartTime)	#pass raw data of each lap
			self.up.append(u)
			self.left.append(l)
			self.right.append(r)
			self.down.append(d)
			self.ctrl.append(c)
			self.space.append(s)
			counter+=1
		self.keyArray=[0,self.up,self.left,self.right,self.down,self.ctrl,self.space]
		

	#find number of seconds taken for the longest lap
	def longestLap(self,data):
		longest=0
		for i in data.laps:
			if i[1]>longest:
				longest=i[1]
		return int(math.ceil(longest))

	#get x values in array in seconds of the longest lap
	def getXValues(self):
		x=[]
		for i in range (0,self.longestLap(self.data)):
			x.append(i)
		return x

	def getTimeStamp(self,startTime,timeStamp):
		return int(round((timeStamp-startTime),2))

	def  getKeyFreq(self,rawData,startTime):
		#returns the 6 key's frequencies in an array for each key
		#Eg. up[i]= the number of times up was pressed till i seconds
		u=[]
		l=[]
		r=[]
		d=[]
		c=[]
		s=[]
		for i in range(0,len(self.x)):
			u.append(0),l.append(0),r.append(0),d.append(0),c.append(0),s.append(0) 
	

		for i in  rawData:
			i[2]=self.getTimeStamp(startTime,i[2])
		#print rawData

		for i in rawData:
			if i[1]==0:		#if key is pressed
				if i[0]==up:
					u[i[2]]+=1
				if i[0]==left:
					l[i[2]]+=1
				if i[0]==right:
					r[i[2]]+=1
				if i[0]==down:
					d[i[2]]+=1
				if i[0]==ctrl:
					c[i[2]]+=1
				if i[0]==space:
					s[i[2]]+=1
	
		prev=[0,u[0],l[0],r[0],d[0],c[0],s[0]] 	#to store previous second's element
		for i in range(1 ,len(self.x)):
			prev[up]+=u[i]
			prev[left]+=l[i]
			prev[right]+=r[i]
			prev[down]+=d[i]
			prev[ctrl]+=c[i]
			prev[space]+=s[i]

			u[i]=prev[up]
			l[i]=prev[left]
			r[i]=prev[right]
			d[i]=prev[down]
			c[i]=prev[ctrl]
			s[i]=prev[space]
	
		return u,l,r,d,c,s

def getKeyName(key):
	if key==up:
		return 'UP'
	if key==left:
		return 'LEFT'
	if key==right:
		return 'RIGHT'
	if key==down:
		return 'DOWN'
	if key==ctrl:
		return 'CTRL'
	if key==space:
		return 'SPACE'

def plot(data,key):
	fig = plt.figure()
	title=getKeyName(key)+' key, player '+data.name
	fig.canvas.set_window_title(title)
	plt.title(title)
	plt.xlabel('Lap time (seconds)')
	plt.ylabel('Times key pressed')
	for i in range(0,data.laps):
		lap='Lap '+str(i)
		plt.plot(data.x,data.keyArray[key][i],label=lap)
	plt.legend(loc='upper left')

def getKeyFeatureVectors(data,label,key,exclude=-1):
	features=[]
	labels=[]
	for i in range(0,data.laps):

		if i==exclude:
			continue
		for j in range(0,len(data.x)):
			features.append([data.x[j],data.keyArray[key][i][j]])
			labels.append(label)
	return features,labels

def getAllFeatureVectors(data,label,exclude=-1):
	features=[]
	labels=[]
	for i in keys:
		f,l=getKeyFeatureVectors(data,label,i,exclude)
		features+=f
		labels+=l
	return features,labels




manas=Frequency('manasLog.txt','Manas')
khalid=Frequency('khalidLog.txt','Khalid')
bhoomi=Frequency('bhoomiLog.txt','Bhoomi')

manasTest=Frequency('manasTest.txt','Manas test')

#plot(manas,right)
plot(manas,left)
#plot(bhoomi,right)
plot(khalid,left)

clf=svm.SVC()
lm=linear_model.LinearRegression()

features=[]
labels=[]

f,l=getAllFeatureVectors(manas,0)
features+=f
labels+=l

f,l=getAllFeatureVectors(khalid,1)
features+=f
labels+=l

f,l=getAllFeatureVectors(manasTest,0)
features+=f
labels+=l

clf.fit(features,labels)
lm.fit(features,labels)


p=clf.predict(f)
c=0
for i in p:
	if i==1:
		c+=1
acc=c/float(len(p))
print acc
print np.mean(lm.predict(f))

#plt.show()