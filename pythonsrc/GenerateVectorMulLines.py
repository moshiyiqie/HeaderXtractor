# -*- coding: utf-8 -*- 
import GenerateVector
import VectorManager
import pickle
import Config

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
def genVectorMulLinesForTrain(percentage):
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
	
	#trainPages = pages[:int(percentage*len(pages))]
	#testPages = pages[int(percentage*len(pages)):]
	
	allVec=[]
	for ele in pages:
		allVec += ele
	VectorManager.printVectorListToCSV(allVec,Config.TMP_ADDR+r'/look.csv', 'classification' )
	
	pickle.dump(allVec,open(Config.TMP_ADDR+r'/allVec.pickle','w'),0)
	#pickle.dump(testPages,open(Config.TMP_ADDR+r'/testPages','w'),0)
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
if __name__ == '__main__':
	genVectorMulLinesForTrain(1)