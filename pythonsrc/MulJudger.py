# -*- coding: utf-8 -*- 
import VectorManager
import Config
import os
import copy
os.chdir(Config.WORKSPACE)
filterList = ['z_origin','z_pageNo']
class MulJudger:
	tmpAddr=r'./pythonsrc/tmp'
	modelAddr=''
	def __init__(self, modelAddr):
		if modelAddr.startswith("."):
			modelAddr = Config.WORKSPACE + modelAddr
		self.modelAddr = modelAddr
	def __getPredictFromFile(self,predict,tmpJudgeAddr, vecNum): 
		l = open(tmpJudgeAddr,'r').readlines()
		for i in range(5,5+vecNum):
			predict.append(l[i].split()[2])
	def judgeVectorList(self,vectorList, tagColName, testTag = 'title'):
		filteredVecList = copy.deepcopy(vectorList)
		#print 'after deepcopy filteredVecList is vectorList ? ' + str(filteredVecList is vectorList)
		for vector in filteredVecList:
			for col in filterList:
				if vector.has_key(col): vector.pop(col)
		tmpARFF_Addr = Config.TMP_ADDR+'/tmp.arff'
		tmpJudgeAddr = Config.TMP_ADDR+'/tmpJudge.txt'
		#print 'tmpARFF_Addr',tmpARFF_Addr
		#print 'tmpJudgeAddr',tmpJudgeAddr
		VectorManager.printVectorListToARFF(filteredVecList, tmpARFF_Addr, tagColName, testTag)
		oscmd = r'java -classpath %s weka.classifiers.functions.LibSVM -l %s -T %s -p 0 > %s'%(Config.LIBSVM_CLASSPATH, self.modelAddr, tmpARFF_Addr, tmpJudgeAddr) #SVM
		#oscmd = r'java -classpath %s weka.classifiers.trees.J48 -l %s -T %s -p 0 > %s'%(Config.J48_CLASSPATH, self.modelAddr, tmpARFF_Addr, tmpJudgeAddr) #J48
		print '[Judge]: OS run cmd : '+oscmd
		os.system(oscmd)
		predict=[]
		self.__getPredictFromFile(predict, tmpJudgeAddr, len(filteredVecList))
		return predict
