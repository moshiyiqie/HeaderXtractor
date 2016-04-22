# -*- coding: utf-8 -*- 
import GenerateVector
import VectorManager
import pickle
import Config
import ModelTrainer

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
#生成所有向量到磁盘，包括一个csv文件和一个对象序列化pickle文件
def genMulLinesVectorToDisk():
	add=r'C:\Users\rainto96\workspace\HeaderXtractor\resource\sparsed_tagged_header_with_line_number.txt'
	pages=[[]]
	tag=[[]]
	startFlag=True
	pageNo=0
	l=open(add).readlines()
	for oneline in l:
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
	VectorManager.printVectorListToCSV(allVec,Config.TMP_ADDR+r'/look.csv', 'classification' )
	
	pickle.dump(allVec,open(Config.TMP_ADDR+r'/allVec.pickle','w'),0)
	print 'train和test上下文向量已写入磁盘'
	'''
	trainList=[]
	testList=[]
	for i in range(0,int(percentage*len(pages))):
		trainList += pages[i]
	for i in range(int(percentage*len(pages)),len(pages)):
		testList += pages[i]
	VectorManager.printVectorListToARFF(trainList, r'C:\Users\rainto96\workspace\HeaderXtractor\vec_mullines_for_train.arff' , 'classification_tag')
	VectorManager.printVectorListToARFF(testList, r'C:\Users\rainto96\workspace\HeaderXtractor\vec_mullines_for_test.arff' , 'classification_tag')
	'''

	
def extractTrainTestSetToDisk(percent):
	print '从磁盘中载入向量 ing'
	allVec = pickle.load(open(r'C:\Users\rainto96\workspace\HeaderXtractor\resource\向量化后_带上下文信息.pickle'))
	print '从磁盘中载入向量 over'
	cVec = {}
	for vector in allVec:
		if not cVec.has_key(vector['classification']): cVec[vector['classification']]=[]
		cVec[vector['classification']].append(vector)
	for cls in cVec:
		print cls
		pickle.dump(cVec[cls][ : int(percent*len(cVec[cls]))],open(r'C:/Users/rainto96/workspace/HeaderXtractor/resource/MulLine_allClassification/'+cls+'_train.pickle','w'),0)
		pickle.dump(cVec[cls][int(percent*len(cVec[cls])) : ],open(r'C:/Users/rainto96/workspace/HeaderXtractor/resource/MulLine_allClassification/'+cls+'_test.pickle','w'),0)


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
	vecs = pickle.load(open(r'C:/Users/rainto96/workspace/HeaderXtractor/resource/MulLine_allClassification/'+cls+'_train.pickle') )
	tmpVecs = veclistFilter(vecs, filterList)
	for vector in tmpVecs:
		vector['classification_tag']='true'
	filteredVecs = tmpVecs
	
	for othercls in classification:
		if othercls == cls : continue
		vecs = pickle.load(open(r'C:/Users/rainto96/workspace/HeaderXtractor/resource/MulLine_allClassification/'+othercls+'_train.pickle') )
		tmpVecs = veclistFilter(vecs, filterList)
		for vector in tmpVecs:
			vector['classification_tag']='false'
		filteredVecs += tmpVecs
	VectorManager.printVectorListToARFF(filteredVecs, arffPath , 'classification_tag')
def trainAllModels():
	addr = r'C:/Users/rainto96/workspace/HeaderXtractor/resource/MulLine_svm_result'
	filteredVecs=[]
	modelTrainer = ModelTrainer.ModelTrainer()
	for cls in classification:
		print 'Now traing for: '+cls
		arffPath = r'C:\Users\rainto96\workspace\HeaderXtractor\vector.arff'
		print 'Generating ARFF now...'
		__genArffFor(cls,arffPath)
		print 'ARFF generating complete'
		modelTrainer.initTrain(arffPath, addr+'/'+cls+'_svm.model')
		modelTrainer.outputResult2File(addr+'/'+cls+'_svm.txt')
		print modelTrainer.getConfusionMat()

if __name__ == '__main__':
	trainAllModels()