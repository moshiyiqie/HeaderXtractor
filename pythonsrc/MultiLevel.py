# -*- coding: utf-8 -*- 
import os
import re
import Config
import pickle
import VectorManager
import GenerateCRF
os.chdir(Config.WORKSPACE)

#��ȡǰ200��pdf�ļ���ͷ����SVM��Ϊѵ�������ΪARFF��ʽ
def getSVMTrainFile():
	outputPath = r'./resource/MulLevel/train_svm.arff'
	
	
	print '���ڴӴ��̶�������������ļ�'
	vecList = pickle.load(open(r'./resource/��������_����������Ϣ_everyline.pickle'))
	print '�������'
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
	
	
	print '���ڴӴ��̶�������������ļ�'
	vecList = pickle.load(open(r'./resource/��������_����������Ϣ_everyline.pickle'))
	print '�������'
	outList = []
	filterList = ['z_pageNo', 'z_origin']
	for vector in vecList:
		if int(vector['z_pageNo']) > 200:
			for key in filterList:
				vector.pop(key)
			outList.append(vector)
	VectorManager.printVectorListToARFF_mul(outList, outputPath, 'classification')

#��ȡ201-400��pdf�ļ���ͷ����J48��Ϊѵ�������ΪARFF��ʽ
def getJ48TrainFile():
	outputPath = r'./resource/MulLevel/train_J48.arff'
	
	
	print '���ڴӴ��̶�������������ļ�'
	vecList = pickle.load(open(r'./resource/��������_����������Ϣ_everyline.pickle'))
	print '�������'
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
	
	
	print '���ڴӴ��̶�������������ļ�'
	vecList = pickle.load(open(r'./resource/��������_����������Ϣ_everyline.pickle'))
	print '�������'
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
	print '���ڴӴ��̶�������������ļ�'
	vecList = pickle.load(open(r'./resource/��������_����������Ϣ_everyline.pickle'))
	print '�������'
	
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