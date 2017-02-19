from LogReader import LogReader
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

up=1
left=2
right=3
down=4
ctrl=5
space=6

manasX=[]
khalidX=[]

manas=LogReader("manasLog.txt")
khalid=LogReader("khalidLog.txt")
bhoomi=LogReader("bhoomiLog.txt")

#data=refernce to LogReader instance
#key=key constant
#name1=player name1
#name2=player name2
#kName=name of key
#twoPlayer= decides wheather to show graph for  two players

def showKeyPressTimes(data,key,kName,name1,name2=None,twoPlayer=False):			
	#shows time pressed v/s time of press for one user for each lap for a key
	duration=[]		#store key press durations per lap
	for i in data.keyPressesPerLap:
		duration.append(i[1][key])

	x=[]
	for i in data.perLap:
		tmp=[]
		for j in i[1]:
			if j[0]==key and j[1]==0:
				tmp.append(j[2])
		x.append(tmp)

	for i in range(0,len(x)):		#to remove extra data
		if len(duration[i])<len(x[i]):
			x[i].pop()
		elif len(duration[i])>len(x[i]):
			duration[i].pop()

	x=np.array(x)
	for i in range(0,len(x)):
	
		for j in range(0,len(x[i])):
			x[i][j]=x[i][j]-data.lapStartTimes[i]
	
	s=name1+' , '+kName
	fig = plt.figure()
	fig.canvas.set_window_title(s)
	plt.title(s)
	plt.xlabel('lap time (seconds)')
	plt.ylabel('time key pressed (seconds)')

	for i in range(0,len(x)):
		lap="LAP "+str(i)
		plt.plot(x[i],duration[i], '.-',label=lap)
		#print ' x is ',x[i], ' length is ',len(x[i])
		#print ' y is ',duration[i], ' length is ',len(duration[i])

		for j in range (0,len(x[i])):
			if name1=='MANAS':
				manasX.append([x[i][j],duration[i][j]])
			elif name1=='KHALID':
				khalidX.append([x[i][j],duration[i][j]])
		
	figManager = plt.get_current_fig_manager()
	figManager.window.showMaximized()
	plt.legend()

	



showKeyPressTimes(manas,left,'LEFT','MANAS')
showKeyPressTimes(khalid,left,'LEFT','KHALID')
print len(manasX)
print len(khalidX)
regr = linear_model.LinearRegression()


xLearn=[]
labels=[]
mTrain=manasX[:len(manasX)/2]
mTest=manasX[len(manasX)/2:]


kTrain=manasX[:len(khalidX)/2]
kTest=manasX[len(khalidX)/2:]

for i in mTrain:
	xLearn.append(i)
	labels.append(0)


for i in kTrain:
	xLearn.append(i)
	labels.append(1)

 
regr.fit(xLearn, labels)
#print regr.score(mTest,kT)
plt.show()