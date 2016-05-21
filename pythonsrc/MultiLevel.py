# -*- coding: utf-8 -*- 
import os
import re
import Config
import pickle
import VectorManager
import GenerateCRF
os.chdir(Config.WORKSPACE)

#抽取前200个pdf文件的头部给SVM作为训练，输出为ARFF格式
def getSVMTrainFile():
	outputPath = r'./resource/MulLevel/train_svm.arff'
	
	
	print '正在从磁盘读入向量化后的文件'
	vecList = pickle.load(open(r'./resource/向量化后_带上下文信息_everyline.pickle'))
	print '读入完毕'
	outList = []
	filterList = ['z_pageNo', 'z_origin']
	for vector in vecList:
		if int(vector['z_pageNo']) <= 600:
			for key in filterList:
				vector.pop(key)
			outList.append(vector)
	VectorManager.printVectorListToARFF(outList, outputPath, 'classification')

def getSVMTestFile():
	outputPath = r'./resource/MulLevel/test_svm.arff'
	
	
	print '正在从磁盘读入向量化后的文件'
	vecList = pickle.load(open(r'./resource/向量化后_带上下文信息_everyline.pickle'))
	print '读入完毕'
	outList = []
	filterList = ['z_pageNo', 'z_origin']
	for vector in vecList:
		if int(vector['z_pageNo']) > 200:
			for key in filterList:
				vector.pop(key)
			outList.append(vector)
	VectorManager.printVectorListToARFF_mul(outList, outputPath, 'classification')

#抽取201-400的pdf文件的头部给J48作为训练，输出为ARFF格式
def getJ48TrainFile():
	outputPath = r'./resource/MulLevel/train_J48.arff'
	
	
	print '正在从磁盘读入向量化后的文件'
	vecList = pickle.load(open(r'./resource/向量化后_带上下文信息_everyline.pickle'))
	print '读入完毕'
	svm_predict = open('./resource/MulLevel/svm_200-900.txt').readlines()
	idx=0
	
	outList = []
	filterList = ['z_pageNo', 'z_origin']
	for vector in vecList:
		if int(vector['z_pageNo']) > 200 and int(vector['z_pageNo']) < 400:
			vector['svm_predict'] = svm_predict[idx].strip()
			idx+=1
			for key in filterList:
				vector.pop(key)
			outList.append(vector)
	VectorManager.printVectorListToARFF_mul(outList, outputPath, 'classification')
def getJ48TestFile():
	outputPath = r'./resource/MulLevel/test_J48.arff'
	
	
	print '正在从磁盘读入向量化后的文件'
	vecList = pickle.load(open(r'./resource/向量化后_带上下文信息_everyline.pickle'))
	print '读入完毕'
	svm_predict = open('./resource/MulLevel/svm_200-900.txt').readlines()
	idx=0
	
	outList = []
	filterList = ['z_pageNo', 'z_origin']
	for vector in vecList:
		if int(vector['z_pageNo']) >= 400:
			vector['svm_predict'] = svm_predict[idx].strip()
			idx+=1
			for key in filterList:
				vector.pop(key)
			outList.append(vector)
	VectorManager.printVectorListToARFF_mul(outList, outputPath, 'classification')

def getCrfTrainTest_File():
	print '正在从磁盘读入向量化后的文件'
	vecList = pickle.load(open(r'./resource/向量化后_带上下文信息_everyline.pickle'))
	print '读入完毕'
	
	fout = open('./CRF++/train/crf_train.txt','w')
	idx=0
	svm_predict = [x.strip() for x in open('./resource/MulLevel/svm_400-900.txt').readlines()]
	j48_predict = [x.strip() for x in open('./resource/MulLevel/J48_400-900.txt').readlines()]
	for vector in vecList:
		if int(vector['z_pageNo']) >= 400:
			if int(vector['z_pageNo']) == 850:
				fout.close()
				fout = open('./CRF++/train/crf_test.txt','w')
			line = vector['z_origin'][1:-1]
			featureStr = GenerateCRF.getFeatureStr(line)
			featureStr += 'svm_predict:'+svm_predict[idx] + ' j48_predict:' + j48_predict[idx] + ' '
			idx += 1
			text = re.sub(r'</?\w+>','',vector['z_origin'][:]).strip()
			label = '<'+vector['classification']+'>'
			fout.write(' '.join([text.replace(' ','|||'), featureStr, label]) + '\n')
	fout.close()
if __name__ == '__main__':
	getSVMTrainFile()