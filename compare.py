import matplotlib.pyplot as plt
from LogReader import LogReader
import numpy as np
up=1
left=2
right=3
down=4
ctrl=5
space=6

manas=LogReader("manasLog.txt")
khalid=LogReader("khalidLog.txt")
bhoomi=LogReader("bhoomiLog.txt")


'''
perLap=[
	[ int lapNo,
	  [raw features]
	],
	[ int lapNo,
	  [raw features]
	]...
]

'''
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

	'''
	plt.plot(x[0],duration[0], '.r-',label='Lap 1')
	plt.plot(x[1],duration[1], '.g-',label='Lap 2')
	plt.plot(x[2],duration[2], '.b-',label='Lap 3')
	plt.plot(x[3],duration[3], '.y-',label='Lap 4')
	plt.plot(x[4],duration[4], '.-',color='brown',label='Lap 5')
	'''
	figManager = plt.get_current_fig_manager()
	figManager.window.showMaximized()
	plt.legend()
	

#showKeyPressTimes(manas,up,'UP','MANAS')

#showKeyPressTimes(manas,down,'DOWN','MANAS')
showKeyPressTimes(manas,left,'LEFT','MANAS')
#showKeyPressTimes(manas,right,'RIGHT','MANAS')
#showKeyPressTimes(manas,ctrl,'CTRL','MANAS')
#showKeyPressTimes(manas,space,'SPACE','MANAS')

showKeyPressTimes(khalid,left,'LEFT','KHALID')


#showKeyPressTimes(False,bhoomi,up,'BHOOMI','UP')


plt.show()












'''
up=[]#store UP key press durations per lap
for i in manas.keyPressesPerLap:
	up.append(i[1][1])

x=[]
for i in manas.perLap:
	tmp=[]
	for j in i[1]:
		if j[0]==1 and j[1]==0:
			tmp.append(j[2])
	x.append(tmp)
for i in range (0,len(x)):
	print len(x[i]),' ',len(up[i])
for i in range(0,len(x)):			#to remove extra data
	if len(up[i])<len(x[i]):
		x[i].pop()
	elif len(up[i])>len(x[i]):
		up[i].pop()


x=np.array(x)

#print up
#print x
print len(x)
print len(up)
for i in range (0,len(x)):
	print len(x[i]),' ',len(up[i])

for i in range(0,len(x)):
	print x[i]
	for j in range(0,len(x[i])):
		x[i][j]=x[i][j]-manas.lapStartTimes[i]
	print x[i]
#y=np.arange(y)
plt.title('UP key')
plt.xlabel('lap time (seconds)')
plt.ylabel('time key pressed (seconds)')


#plt.subplot(511)
plt.plot(x[0],up[0], '.r-',label='Lap 1')
plt.plot(x[1],up[1], '.g-',label='Lap 2')
plt.plot(x[2],up[2], '.b-',label='Lap 3')
plt.plot(x[3],up[3], '.y-',label='Lap 4')
plt.plot(x[4],up[4], '.-',color='brown',label='Lap 5')
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.legend()
plt.show()

'''






'''
plt.subplot(512)
plt.plot(x[1],up[1], '.-')
plt.subplot(513)
plt.plot(x[2],up[2], '.-')
plt.subplot(514)
plt.plot(x[3],up[3], '.-')
plt.subplot(515)
plt.plot(x[4],up[4], '.-')
plt.show()'''