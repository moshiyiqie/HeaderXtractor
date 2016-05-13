# -*- coding: utf-8 -*- 
import GenerateVector
import os
import pickle
import Config
os.chdir(Config.WORKSPACE)
class ModelTrainer:
	result=[]
	cMat=[[0,0],[0,0]]
	cMatStr=''
	'''好像有点问题，没写好
	def loadFrom(self, path):
		self=pickle.load(open(path))
	def dumpTo(self, path):
		pickle.dump(self, open(path,'w'), 0)
	'''
	def __getConfusionMatProcess(self):
		count=0
		for line in self.result:
			if line == '=== Confusion Matrix ===':
				data = self.result[count+3:count+5]
				self.cMat[0][0] = int(data[0].split()[0])
				self.cMat[0][1] = int(data[0].split()[1])
				self.cMat[1][0] = int(data[1].split()[0])
				self.cMat[1][1] = int(data[1].split()[1])
				self.cMatStr = '\n'.join(self.result[count+2:count+5])
				break
			count+=1
	def initTrain(self, trainPath, modelOutPath):
		print 'Training in Weka...'
		self.result = os.popen('java -classpath '+Config.LIBSVM_CLASSPATH+' weka.classifiers.functions.LibSVM -S 0 -K 2 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.001 -P 0.1 -seed 1 -t %s -d %s'%(trainPath,modelOutPath)).read()
		self.result = self.result.split('\n')
		self.__getConfusionMatProcess()
		print 'Training Complete!'
		if self.cMat[0][0] == 0:
			print self.result
			print '!!!Train Error!!!'
	def outputResult2File(self,path):
		fout = open(path,'w')
		fout.write(str(self.getPrecision())+'\n')
		fout.write(str(self.getRecall())+'\n')
		fout.write(str(self.getFval())+'\n')
		fout.write(str(self.getConfusionMat())+'\n')
		fout.write(str(self.getNumOfA())+'\n')
		fout.close()
	def getConfusionMat(self):
		return self.cMatStr
	def getPrecision(self):
		if self.cMat[0][0] + self.cMat[1][0] == 0: return 0
		return self.cMat[0][0]*1.0/(self.cMat[0][0] + self.cMat[1][0])
	def getRecall(self):
		if self.cMat[0][0] + self.cMat[0][1] == 0: return 0
		return self.cMat[0][0]*1.0/(self.cMat[0][0] + self.cMat[0][1])
	def getFval(self):
		a=self.getPrecision()
		b=self.getRecall()
		if a+b == 0: return 0
		return 2.0*a*b/(a+b)
	def getNumOfA(self):
		return self.cMat[0][0] + self.cMat[0][1]
	def getNumOfB(self):
		return self.cMat[1][0] + self.cMat[1][1]
	def getAllModel(self):
		trainPath = r'./vector.arff'
		for file in os.listdir(r'./resource/allClassification'):
			print 'Now classifying '+ file
			GenerateVector.generateVectorFor(file)
			self.initTrain(trainPath, r'./resource/svm_result/'+file+'_svm.model')
			self.outputResult2File(r'./resource/svm_result/'+file+'_svm.txt')
	def getModelFor(self, cls):
		trainPath = r'./vector.arff'
		if not cls.endswith('.txt'):
			cls += '.txt'
		print 'Now classifying '+ cls
		GenerateVector.generateVectorFor(cls)
		self.initTrain(trainPath, r'./resource/svm_result/'+cls+'_svm.model')
		self.outputResult2File(r'./resource/svm_result/'+cls+'_svm.txt')
if __name__ == '__main__':
	#ModelTrainer().getModelFor('abstract')
	#ModelTrainer().getAllModel()
	
	'''
	path = './resource/svm_result'
	for file in os.listdir(path):
		if file.endswith('.pickle'):
			c = Classifier()
			c = pickle.load(open(path+'/'+file))
			print c.getRecall()
	'''