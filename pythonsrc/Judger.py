# -*- coding: utf-8 -*- 
import VectorManager
import Config
class Judger:
	tmpAddr=r'C:/Users/rainto96/workspace/HeaderXtractor/pythonsrc/tmp'
	modelAddr=''
	def Judger(self, modelAddr):
		self.modelAddr = modelAddr
	def __getPredictFromFile(self,predict,tmpJudgeAddr, vecNum):
		l = open(tmpJudgeAddr,'r').readlines()
		for i in range(5,5+vecNum):
			predict.append(l[i].split()[2])
	def judgeVectorList(self,vectorList):
		tmpARFF_Addr = Config.TMP_ADDR+'/tmp.arff'
		tmpJudgeAddr = Config.TMP_ADDR+'/tmpJudge.txt'
		VectorManager.printVectorListToARFF(vectorList, tmpARFF_Addr, 'classification_tag')
		os.system(r'java -classpath %s weka.classifiers.functions.LibSVM -l %s -T %s -p 0 > %s'%(Config.LIBSVM_CLASSPATH, self.modelAddr, tmpARFF_Addr, tmpJudgeAddr))
		predict=[]
		self.__getPredictFromFile(predict, tmpJudgeAddr, len(vectorList))
		return predict

		
		
		
'''
def getPredictFromFile(predict,tmpJudgeAddr, vecNum):
	l = open(tmpJudgeAddr,'r').readlines()
	for i in range(5,5+vecNum):
		predict.append(l[i].split()[2])

predict=[]
getPredictFromFile(predict, r'C:\Users\rainto96\workspace\HeaderXtractor\pythonsrc\tmp\out.txt', 5)
print predict
'''