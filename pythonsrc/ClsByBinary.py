# -*- coding: utf-8 -*- 
import Config
import os
import pickle
import Judger
import copy
os.chdir(Config.WORKSPACE)
classification=['abstract','address','affiliation','author','date','degree','email','intro','keyword','note','page','phone','pubnum','title','web']
INDEPENDENT_CLSTAG = 'classfication_tag'
confMat={}
def initConfusionMat():
	t_classification = classification + ['other']
	for label in t_classification:
		for label2 in t_classification:
			if not confMat.has_key(label):
				confMat[label] = {}
			if not confMat[label].has_key(label2):
				confMat[label][label2]=0
def printConfusionMat():
	fout = open('./ClsByBinary_confusionMat.csv','w')
	fout.write(' ,')
	t_classification = classification + ['other']
	
	for label in t_classification: fout.write(label + ',')
	fout.write('\n')
	for label in t_classification:
		fout.write(label + ',')
		for label2 in t_classification:
			fout.write(str(confMat[label][label2])+',')
		fout.write('\n')
	fout.write('\n类别,准确率,召回率,F1值,样本个数')
	for label in t_classification:
		fout.write('\n')
		a2a = confMat[label][label]
		b2a = sum( [confMat[y][label] for y in t_classification if y != label] )
		a2b = sum( [confMat[label][y] for y in t_classification if y != label] )
		b2b = sum( [confMat[y][z] for y in t_classification for z in t_classification if y!=label or z!=label] ) - b2a
		if a2a+b2a == 0: precision = 0
		else:
			precision = a2a*1.0/(a2a+b2a)
		if a2a+a2b == 0: recall = 0
		else:
			recall=a2a*1.0/(a2a+a2b)
		if precision + recall == 0: f1=0
		else:
			f1=2*precision*recall/(precision + recall)
		fout.write(','.join([label, str(precision), str(recall), str(f1), str(a2a + a2b)]))
	fout.close()
			
def showClsResultExcel(clsResult):
	fout = open(r'./pythonsrc/tmp/clsByBinaryResult.csv','w')
	fout.write('类别,准确率,召回率,F值,样本数目\n')
	for cls in classification:
		for result in clsResult[cls]:
			fout.write(cls + ',' + str(result[0]) + ',' + str(result[1]) + ',' + str(result[2]) + '\n')
	fout.close()
	
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
	
#计算各个类别召准性能并打印到excel中
def calPrecisionRecall():
	clsPerformanceResult={}
	for cls in classification:
		aa=0
		ab=0
		ba=0
		bb=0
		for i in range(0,len(vecList)):
			if vecList[i]['classification'] == cls:
				if clsResult[i] == cls:#ATTENTION!!!!!!!!!!!!!!!!!!!!!
					aa+=1
				else: ab+=1
			else:
				if clsResult[i] == cls: ba+=1
				else: bb+=1
		presion = aa*1.0/(aa+ba+0.0000001)
		recall = aa*1.0/(aa+ab+0.0000001)
		fval = 2*presion*recall/(presion+recall+0.000001)
		if not clsPerformanceResult.has_key(cls): clsPerformanceResult[cls]=[]
		clsPerformanceResult[cls].append([presion, recall, fval])
	showClsResultExcel(clsPerformanceResult)

def run():
	initConfusionMat()

	#载入测试数据
	print 'Load Vector With Contextual Info from Disk ...'
	vecList = pickle.load(open(r'./resource/向量化后_带上下文信息_everyline.pickle'))
	vecList = vecList[int(0.66*len(vecList)):]
	print 'Load Complete!'

	#初始化二元分类器
	vecListNoContext = getVecListNoContext(copy.deepcopy(vecList))
	independentJudge = {}
	independentPath= r'./resource/j48_result'
	for file in os.listdir(independentPath):
		if file.endswith('.model'):
			independentJudge[file[:file.find(".")]] = Judger.Judger(independentPath+'/'+file)

	#计算预测结果和置信度
	dic_idx_predict={}
	dic_idx_confidence={}
	for cls in classification:
		dic_idx_predict[cls] = independentJudge[cls].judgeVectorList(vecListNoContext,INDEPENDENT_CLSTAG, 'true')
		dic_idx_confidence[cls] = []
		independentJudge[cls].getConfidenceFromFile(dic_idx_confidence[cls])

	#检查数组大小是否合法
	siz = len(vecList)
	for cls in classification:
		if len(dic_idx_predict[cls]) != siz or len(dic_idx_confidence[cls]) != siz:
			print '[ClsByBinary] Error in Size!!!'
			return
	
	#获得最终分类结果，取confidence最大的那个类
	clsResult=[]
	nolabel={}
	for cls in classification: nolabel[cls] = 0
	fo = open('./look.txt','w')
	for i in range(0, siz):
		maxn = -1
		label = 'other'
		ostr=''
		truenum=0
		for cls in classification:
			ostr+=cls+':'+dic_idx_predict[cls][i] +' conf:'+ dic_idx_confidence[cls][i]+'   '
			if 'true' in dic_idx_predict[cls][i]: truenum+=1
			if 'true' in dic_idx_predict[cls][i] and dic_idx_confidence[cls][i] > maxn:
				maxn = dic_idx_confidence[cls][i]
				label = cls
		fo.write(ostr+'\t'+ str(truenum) +'\t'+vecList[i]['classification']+'\n')
		if label == 'other':
			nolabel[cls]+=1
		clsResult.append(label)#获得预测的最终结果，放在clsResult中
		confMat[vecList[i]['classification']][label] += 1 #更新结果到混淆矩阵中
	fo.close()
	
	printConfusionMat()
if __name__ == '__main__':
	run()