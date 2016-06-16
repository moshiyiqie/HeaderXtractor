# -*- coding: utf-8 -*- 
import GenerateVector
import VectorManager
import pickle
import Config
import ModelTrainer
import os
os.chdir(Config.WORKSPACE)
classification=['abstract','address','affiliation','author','date','degree','email','intro','keyword','note','page','phone','pubnum','title','web']
PRE_LIMIT = 5
NEXT_LIMIT = 5
def updateContextual(onepage, onepageTag):
	if len(onepage) != len(onepageTag): print 'error in updateContextual'
	for i in range(0,len(onepage)):
		for pre in range(1,PRE_LIMIT): 
			for cls in classification : onepage[i]['pre'+str(pre)+cls]=0
		for next in range(1,NEXT_LIMIT): 
			for cls in classification : onepage[i]['next'+str(next)+cls]=0
		for pre in range(1,PRE_LIMIT):
			if i-pre < 0 : break
			onepage[i]['pre'+str(pre)+onepageTag[i-pre]] = 0.5
		for next in range(1,NEXT_LIMIT):
			if i+next >= len(onepage) : break
			onepage[i]['next'+str(next)+onepageTag[i+next]] = 0.5
			
#将头部转化为向量
def transformHeader2Vector(theader):
	header = []
	tmpNo = 0
	for x in theader:
		x = '<title>'+x+'</title>::line_number::' + str(tmpNo)
		header.append(x)
		tmpNo+=1
	l=header
	allVec=[]
	for oneline in l:
		if len(GenerateVector.__removeTag(oneline.split('::line_number::')[0]).strip()) == 0:
			print '空行:'+oneline
			continue
		basicVec = GenerateVector.__getBasicVector(oneline)
		pos = oneline.split('::line_number::')[1].strip()
		basicVec['classification'] = VectorManager.getTag(oneline)
		basicVec['z_pageNo'] = 0
		basicVec['z_origin'] = '"'+oneline.strip().replace('"','')+'"'
		allVec.append(basicVec)
	VectorManager.printVectorListToCSV(allVec,r'./pythonsrc/tmp/look.csv', 'classification' )
	
	pickle.dump(allVec,open(r'./pythonsrc/tmp/header2vector.pickle','w'),0)
	#print '[Step1]Header to vector success!'
	#print allVec
	return allVec

#生成所有向量到磁盘，包括一个csv文件和一个对象序列化pickle文件
def genMulLinesVectorToDisk():
	add=r'./resource/tagged_headers_everyline.txt'
	pages=[[]]
	tag=[[]]
	startFlag=True
	pageNo=0
	l=open(add).readlines()
	for oneline in l:
		if len(GenerateVector.__removeTag(oneline.split('::line_number::')[0]).strip()) == 0:
			print '空行:'+oneline
			continue
		basicVec = GenerateVector.__getBasicVector(oneline)
		pos = oneline.split('::line_number::')[1].strip()
		if int(pos) == 0:
			print '正在处理第'+str(pageNo)+'页'
			if startFlag==False:
				updateContextual(pages[-1], tag[-1])
				tag.append([])
				pages.append([])
				pageNo+=1
			startFlag=False
		tag[-1].append(VectorManager.getTag(oneline))
		basicVec['classification'] = VectorManager.getTag(oneline)
		basicVec['z_pageNo'] = pageNo
		basicVec['z_origin'] = '"'+oneline.strip().replace('"','')+'"'
		pages[-1].append(basicVec)
	if len(pages[-1]) > 0: 
		updateContextual(pages[-1], tag[-1])
	
	
	allVec=[]
	for ele in pages:
		allVec += ele
	VectorManager.printVectorListToCSV(allVec,r'./pythonsrc/tmp/look.csv', 'classification' )
	
	pickle.dump(allVec,open(r'./pythonsrc/tmp/向量化后_带上下文信息_everyline.pickle','w'),0)
	print 'train和test上下文向量已写入磁盘'
	'''
	trainList=[]
	testList=[]
	for i in range(0,int(percentage*len(pages))):
		trainList += pages[i]
	for i in range(int(percentage*len(pages)),len(pages)):
		testList += pages[i]
	VectorManager.printVectorListToARFF(trainList, r'./vec_mullines_for_train.arff' , 'classification_tag')
	VectorManager.printVectorListToARFF(testList, r'./vec_mullines_for_test.arff' , 'classification_tag')
	'''

	
def extractTrainTestSetToDisk(percent):
	print '从磁盘中载入向量 ing'
	allVec = pickle.load(open(r'./resource/向量化后_带上下文信息.pickle'))
	print '从磁盘中载入向量 over'
	cVec = {}
	for vector in allVec:
		if not cVec.has_key(vector['classification']): cVec[vector['classification']]=[]
		cVec[vector['classification']].append(vector)
	for cls in cVec:
		print cls
		pickle.dump(cVec[cls][ : int(percent*len(cVec[cls]))],open(r'./resource/MulLine_allClassification/'+cls+'_train.pickle','w'),0)
		pickle.dump(cVec[cls][int(percent*len(cVec[cls])) : ],open(r'./resource/MulLine_allClassification/'+cls+'_test.pickle','w'),0)


def veclistFilter(vecList, filterList):
	filteredVecs=[]
	for vector in vecList:
		nvec={}
		for key in vector:
			if key in filterList: continue
			nvec[key] = vector[key]
		filteredVecs.append(nvec)
	return filteredVecs
def __genArffFor(cls,arffPath):
	filterList = ['z_origin','z_pageNo','classification']
	vecs = pickle.load(open(r'./resource/MulLine_allClassification/'+cls+'_train.pickle') )
	tmpVecs = veclistFilter(vecs, filterList)
	for vector in tmpVecs:
		vector['classification_tag']='true'
	filteredVecs = tmpVecs
	
	for othercls in classification:
		if othercls == cls : continue
		vecs = pickle.load(open(r'./resource/MulLine_allClassification/'+othercls+'_train.pickle') )
		tmpVecs = veclistFilter(vecs, filterList)
		for vector in tmpVecs:
			vector['classification_tag']='false'
		filteredVecs += tmpVecs
	VectorManager.printVectorListToARFF(filteredVecs, arffPath , 'classification_tag')
def trainAllModels():
	addr = r'./resource/MulLine_svm_result'
	filteredVecs=[]
	modelTrainer = ModelTrainer.ModelTrainer()
	for cls in classification:
		print 'Now traing for: '+cls
		arffPath = r'./vector.arff'
		print 'Generating ARFF now...'
		__genArffFor(cls,arffPath)
		print 'ARFF generating complete'
		modelTrainer.initTrain(arffPath, addr+'/'+cls+'_svm.model')
		modelTrainer.outputResult2File(addr+'/'+cls+'_svm.txt')
		print modelTrainer.getConfusionMat()

if __name__ == '__main__':
	genMulLinesVectorToDisk()