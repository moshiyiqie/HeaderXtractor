# -*- coding: utf-8 -*- 
import Config
import re
import os
'''
��ӡһ��vectorList��csv�ļ���ʽ��ָ���˹���ע��tag�������Ҹ��з������
'''
def printVectorListToCSV(vectorList, outputPath, tagColName):
	if len(vectorList) == 0:
		print '�����б�Ϊ��'
		return
	
	fout = open(outputPath, 'w')
	#��ӡԪ��Ϣ
	for key in sorted(vectorList[0].keys()):
		if key==tagColName:
			continue
		fout.write(str(key)+',')
	fout.write(tagColName+'\n')
	#��ӡ����
	for vector in vectorList:
		for key in sorted(vector.keys()):
			if key==tagColName:
				continue
			fout.write(str(vector[key])+',')
		if not vector.has_key(tagColName): vector[tagColName] = -1
		fout.write(str(vector[tagColName])+'\n')
	fout.close()
'''
��ӡһ��vectorList��arff�ļ���ʽ��ָ���˹���ע��tag�������Ҹ��з������
'''
def printVectorListToARFF(vectorList, outputPath, tagColName):
	tmpCSV_Addr = Config.TMP_ADDR+r'/tmp.csv'
	printVectorListToCSV(vectorList,tmpCSV_Addr,tagColName)
	print '����ת��Ϊarff'
	os.system(r'java -classpath "C:/Program Files (x86)/Weka-3-6/weka.jar" weka.core.converters.CSVLoader %s > %s'%(tmpCSV_Addr, outputPath))
	print 'arffת�����'

def getTag(oneline):
	list = oneline.split('::line_number::')
	line = list[0].strip()
	for tag in re.findall(r'<\w+>',line):
		return tag[1:-1]

if __name__ == '__main__':
	print getTag(r'<affiliation> Georgia Institute of Technology  </affiliation>')