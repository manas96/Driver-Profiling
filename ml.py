
#from sklearn import tree,svm
import numpy as np
from LogReader import LogReader

import matplotlib.pyplot as plt

data1=LogReader("manasLog.txt")
data2=LogReader("khalidLog.txt")
data3=LogReader("bhoomiLog.txt")

gaussian_numbers = np.random.randn(1000)
a=[]
b=[]
c=[]
x=[0,1,2,3,4,5,6,7]
keys=["NULL","UP","LEFT","RIGHT","DOWN","CTRL","SPACE"]
for i in data1.rawFeatures:
	a.append(i[0])
for i in data2.rawFeatures:
	b.append(i[0])
for i in data3.rawFeatures:
	c.append(i[0])
plt.figure(1)
plt.title("Times keys pressed")
plt.xlabel("key")
plt.ylabel("Frequency")
plt.xticks(x,keys)
plt.hist([a,b,c],x,label=['Manas','Khalid','Bhoomi'],align='left')
plt.legend()

fig, ax = plt.subplots()
nGroups=7
barWidth=0.35
plt.title("Duration of key presses")
index=np.arange(nGroups)
y=[data1.totalKeyPressTimes,data2.totalKeyPressTimes,data3.totalKeyPressTimes]
rec1=ax.bar(index+.1,y[0],barWidth,color='b',label='Manas',align='center')
rec2=ax.bar(index+barWidth,y[1],barWidth,color='g',label='Khalid',align='center')
rec3=ax.bar(index+2*barWidth,y[2],barWidth,color='r',label='Bhoomi',align='center')
plt.xlabel('Keys')
plt.ylabel('Duration in seconds')
ax.set_xticks(index)
ax.set_xticklabels(keys)
ax.legend()
plt.show()





#data1.printData()
#data2.printData()


'''
featuresNormal,featuresRash=addPadding(featuresNormal,featuresRash)
addPadding(featuresNormal,featuresTest)
#print len(featuresTestN)


features=[featuresNormal,featuresRash]
#print features

labels=[0,1]#0=normal, 1=rash driver

print featuresNormal
clf=tree.DecisionTreeClassifier()
n=0
r=0
for i in range (0,1000):
	clf=clf.fit(features,labels)
	p=clf.predict([featuresTest])
	print p
	#s=svm.SVC()
	#s=s.fit(features,labels)
	#p=s.predict([featuresTest])
	if p==[0]:
		n=n+1.0
	else:
		r=r+1.0
print "n is ",n," r is ",r
print "n/(n+r) is ",n/(n+r)'''

		
