# -*- coding: utf-8 -*- 
import GenerateVector
import os
class Classifier:
	result=[]
	cMat=[[0,0],[0,0]]
	cMatStr=''
	def __getConfusionMatProcess(self):
		count=0
		for line in self.result:
			if line == '=== Confusion Matrix ===':
				data = self.result[count+3:count+5]
				self.cMat[0][0] = int(data[0].split()[0])
				self.cMat[0][1] = int(data[0].split()[1])
				self.cMat[1][0] = int(data[1].split()[0])
				self.cMat[1][1] = int(data[1].split()[1])
				self.cMatStr = ''.join(self.result[count+2:count+5])
				break
			count+=1
	def initTrain(self, trainPath):
		print 'Training in Weka...'
		self.result = os.popen('java -classpath "C:/Program Files (x86)/Weka-3-6/weka.jar;C:/Program Files (x86)/Weka-3-6/libsvm-3.21/java/libsvm.jar" weka.classifiers.functions.LibSVM -S 0 -K 2 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.001 -P 0.1 -seed 1 -t %s'%(trainPath)).read()
		self.result = self.result.split('\n')
		self.__getConfusionMatProcess()
		print self.cMat
		print 'Training Complete!'
	def getConfusionMat(self):
		return self.cMatStr
	def getPrecision(self):
		return self.cMat[0][0]*1.0/(self.cMat[0][0] + self.cMat[1][0])
	def getRecall(self):
		return self.cMat[0][0]*1.0/(self.cMat[0][0] + self.cMat[0][1])
	def getFval(self):
		a=self.getPrecision()
		b=self.getRecall()
		return 2.0*a*b/(a+b)
if __name__ == '__main__':
	trainPath = 'C:/Users/rainto96/Desktop/vector.arff'
	c = Classifier()
	c.initTrain(trainPath)
	print c.getPrecision()
	print c.getRecall()
	print c.getFval()