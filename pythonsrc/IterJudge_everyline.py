# -*- coding: utf-8 -*- 
import Judger
import os
import pickle
import GenerateVector
import copy
import VectorManager
import Config
os.chdir(Config.WORKSPACE)
#���ö����з���Judgerд��Ԥ��
#����contexualά��
#��contexual����Judgerд��Ԥ��
#��ӡ��׼���
#����contexualά��
#��contexual����Judgerд��Ԥ��
#��ӡ��׼���
PRE_LIMIT = 5
NEXT_LIMIT = 5
INDEPENDENT_CLSTAG = 'classfication_tag'
CONTEXTUAL_CLSTAG = 'classification_tag'
classification=['abstract','address','affiliation','author','date','degree','email','intro','keyword','note','page','phone','pubnum','title','web']
def updateContextualAttr(vecList, predict):
	if len(vecList) != len(predict): print '!!!Error in updateContextualAttr'
	for i in range(0,len(vecList)):
		curPageNo = vecList[i]['z_pageNo']
		for pre in range(1,PRE_LIMIT): 
			for cls in classification : vecList[i]['pre'+str(pre)+cls]=0
		for next in range(1,NEXT_LIMIT): 
			for cls in classification : vecList[i]['next'+str(next)+cls]=0
		for pre in range(1,PRE_LIMIT):
			if i-pre < 0 : break
			if vecList[i-pre]['z_pageNo'] != curPageNo : break
			for cls in classification:
				ct = 0
				if '1:true' in predict[i][cls]: ct = 0.5
				vecList[i]['pre'+str(pre)+cls] = ct
		for next in range(1,NEXT_LIMIT):
			if i+next >= len(vecList) : break
			if vecList[i+next]['z_pageNo'] != curPageNo : break
			for cls in classification:
				ct = 0
				if '1:true' in predict[i][cls]: ct = 0.5
				vecList[i]['next'+str(next)+cls] = ct

def printPresionRecall(vecList, predict, iteResult):
	if len(vecList) != len(predict) : print '!!!Error in printPresionRecall'
	for cls in classification:
		aa=0
		ab=0
		ba=0
		bb=0
		for i in range(0,len(vecList)):
			if vecList[i]['classification'] == cls:
				if 'true' in predict[i][cls]:#ATTENTION!!!!!!!!!!!!!!!!!!!!!
					aa+=1
				else: ab+=1
			else:
				if 'true' in predict[i][cls]: ba+=1
				else: bb+=1
		presion = aa*1.0/(aa+ba+0.0000001)
		recall = aa*1.0/(aa+ab+0.0000001)
		fval = 2*presion*recall/(presion+recall+0.000001)
		if not iteResult.has_key(cls): iteResult[cls]=[]
		iteResult[cls].append([presion, recall, fval])
	showIteResultExcel(iteResult)
	
def getIndexDicPredictFromDicIndexPredict(dicIndexPredict):
	indexDicPredict = []
	siz=0
	for key in dicIndexPredict:
		siz = len(dicIndexPredict[key])
		break
	for i in range(0,siz): indexDicPredict.append({})
	for key in dicIndexPredict:
		for i in range(0,siz):
			indexDicPredict[i][key] = dicIndexPredict[key][i]
	return indexDicPredict
	
def getVecListNoContext(vecListWithContext):
	vecListWithContextCpy = copy.deepcopy(vecListWithContext)
	vecListNoContext = []
	for vector in vecListWithContextCpy:
		tmpVec = {}
		for key in vector:
			if 'pre' in key or 'next' in key:
				continue
			tmpVec[key] = vector[key]
		vecListNoContext.append(tmpVec)
	return vecListNoContext

def showIteResultExcel(iteResult):
	fout = open(r'./pythonsrc/tmp/iteResult.csv','w')
	fout.write('���,׼ȷ��,�ٻ���,Fֵ,������Ŀ\n')
	for cls in classification:
		for result in iteResult[cls]:
			fout.write(cls + ',' + str(result[0]) + ',' + str(result[1]) + ',' + str(result[2]) + '\n')
	fout.close()
	#os.system(r'./pythonsrc/tmp/iteResult.csv')

#������������ÿ����������������Ϣ���
def clearContexualInfo(vecList):
	for vec in vecList:
		for key in vec:
			if key.startswith("pre") or key.startswith("next"):
				vec[key] = 0.0
				
def toBinary(result):
	dic_idx_predict={}
	siz = len(result)
	for cls in classification:
		dic_idx_predict[cls]=[]
		for i in range(0,siz):
			dic_idx_predict[cls].append('0:false')
	for i in range(0,siz):
		pos = result[i].find(':')
		index = int(result[i][:pos]) - 1
		label = classification[index]
		dic_idx_predict[label][i] = '1:true'
	return dic_idx_predict
	
def iterJudge():
	print 'Load Vector With Contextual Info from Disk ...'
	vecList = pickle.load(open(r'./resource/��������_����������Ϣ_everyline.pickle'))
	vecList = vecList[int(0.66*len(vecList)):]
	print 'Load Complete!'
	
	contexualJudge = {}
	contexualPath = r'./resource/everyline/j48_model_66train_contexual.model'
	contexualJudge= Judger.Judger(Config.WORKSPACE+contexualPath)
	
	clearContexualInfo(vecList)#�����ѵ���������е���������Ϣ������һ��ʼ��������ϢΪ0
	#pickle.dump(dic_idx_predict, open('./dic_idx_predict_indpdt.pc','w'))
	#dic_idx_predict = pickle.load(open('./dic_idx_predict_indpdt.pc'))
	
	iteResult={}
	for itTimes in range(0, 5):
		print 'Now '+str(itTimes)+' Generation ...'
		dic_idx_predict={}#���Ԥ����
		result = contexualJudge.judgeVectorList(vecList,CONTEXTUAL_CLSTAG)#���Ԥ�����������ģ���yes|no��
		if len(result) != len(vecList): print 'Error:Ԥ������Ŀ�ͱ�Ԥ���������Ŀ��ͬ' #����
		dic_idx_predict = toBinary(result)#���������Ϊ�����ģ�ת����Ϊ [���j][����i]=����i�����j�����yes|no��
		
		idx_dic_predict = getIndexDicPredictFromDicIndexPredict(dic_idx_predict) #�� [���j][����i]=����i�����j�����yes|no�� ��Ϊ [����i][���j]=����i�����j���
		updateContextualAttr(vecList, idx_dic_predict)#����һ��Ԥ��Ľ��������������������Ϣ
		printPresionRecall(vecList, idx_dic_predict, iteResult)#��ӡ��һ��Ԥ�����׼���ܽ��
		VectorManager.printVectorListToCSV(vecList, r'./pythonsrc/tmp/ite'+str(itTimes)+'vector.csv', CONTEXTUAL_CLSTAG)#��ӡ����-debug��
		
		
	showIteResultExcel(iteResult)
	
			
if __name__ == '__main__':
	
	iterJudge()
	
def unitest():
	'''
	��Ԫ���ԣ������ö����������ಢ��ӡ���
	'''
	
	independentJudge = {}#############################
	independentPath= r'./resource/svm_result'
	filterList = ['z_origin','z_pageNo','classification']
	for file in os.listdir(independentPath):
		if file.endswith('_svm.model'):
			independentJudge[file.replace('.txt_svm.model','')] = Judger.Judger(independentPath+'/'+file)
	contexualJudge = {}
	contexualPath = r'./resource/MulLine_svm_result'
	for file in os.listdir(contexualPath):
		if file.endswith('_svm.model'):
			contexualJudge[file.replace('_svm.model','')] = Judger.Judger(contexualPath+'/'+file)
	'''
	print 'Load Vector From Disk ...'
	vecList=pickle.load(open(r'./resource/��������_����������Ϣ.pickle'))
	print 'Load Complete!'
	vecList_no_context = getVecListNoContext(vecList)
	predict={}
	for cls in classification:
		print 'Predict: ' + cls + '...'
		predict[cls] = independentJudge[cls].judgeVectorList(vecList_no_context,INDEPENDENT_CLSTAG)
	predict = getIndexDicPredictFromDicIndexPredict(predict)#############################
	'''
	print 'Load Vector From Disk ...'
	vecList=pickle.load(open(r'./resource/��������_����������Ϣ.pickle'))
	print 'Load Complete!'
	print '1.VecList has classification? ' + str(vecList[0].has_key('classification'))
	
	#pickle.dump(predict, open('./pre.pc','w'))
	predict = pickle.load(open('./pre.pc'))
	updateContextualAttr(vecList, predict)
	print '2.VecList has classification? ' + str(vecList[0].has_key('classification'))
	'''
	n_predict={}
	for cls in classification:
		n_predict[cls] = contexualJudge[cls].judgeVectorList(vecList, CONTEXTUAL_CLSTAG)
	n_predict = getIndexDicPredictFromDicIndexPredict(n_predict)
	'''
	#pickle.dump(n_predict, open('./n_predict.pc','w'))
	n_predict = pickle.load(open('./n_predict.pc'))
	print '3.VecList has classification? ' + str(vecList[0].has_key('classification'))
	
	iteResult={}
	printPresionRecall(vecList, n_predict, iteResult)#
	print iteResult