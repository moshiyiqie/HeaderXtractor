# -*- coding: utf-8 -*- 
import Config
import re
import os
os.chdir(Config.WORKSPACE)
'''
��ӡһ��vectorList��csv�ļ���ʽ��ָ���˹���ע��tag�������Ҹ��з������
'''
def printVectorListToCSV(vectorList, outputPath, tagColName):
	if len(vectorList) == 0:
		print '�����б�Ϊ��'
		return
	
	fout = open(outputPath, 'w')
	
	keys = vectorList[0].keys()
	keys = sorted(keys)
	
	#��ӡԪ��Ϣ
	for key in keys:
		if key==tagColName:
			continue
		fout.write(str(key)+',')
	fout.write(tagColName+'\n')
	#��ӡ����
	for vector in vectorList:
		for key in keys:
			if key==tagColName:
				continue
			if not vector.has_key(key):
				print vector
			fout.write(str(vector[key])+',')
		if not vector.has_key(tagColName): vector[tagColName] = 'title'
		fout.write(str(vector[tagColName])+'\n')
	fout.close()
	
'''
#����@attribute classification_tag �ж�����
def printVectorListToARFF_mul(vectorList, outputPath, tagColName):
	tmpCSV_Addr = Config.TMP_ADDR+r'/tmp.csv'
	printVectorListToCSV(vectorList,tmpCSV_Addr,tagColName)
	print '����ת��Ϊarff'
	print tmpCSV_Addr
	os.system(r'java -classpath '+Config.WEKA_JAR_PATH+' weka.core.converters.CSVLoader %s -B 10000 > %s'%(tmpCSV_Addr, Config.WORKSPACE+outputPath))
	print 'arffת�����'
'''

'''
��ӡһ��vectorList��arff�ļ���ʽ��ָ���˹���ע��tag�������Ҹ��з������
'''
#ֻ����@attribute classification_tag Ϊtrue����false
def printVectorListToARFF(vectorList, outputPath, tagColName):
	tmpCSV_Addr = Config.TMP_ADDR+r'/tmp.csv'
	printVectorListToCSV(vectorList,tmpCSV_Addr,tagColName)
	print '����ת��Ϊarff'
	print r'java -classpath '+Config.WEKA_JAR_PATH+' weka.core.converters.CSVLoader %s -B 100000 > %s'%(tmpCSV_Addr, outputPath)
	os.system(r'java -classpath '+Config.WEKA_JAR_PATH+' weka.core.converters.CSVLoader %s -B 100000 > %s'%(tmpCSV_Addr, outputPath))
	
	lines = open(outputPath).readlines()
	fout = open(outputPath,'w')
	for line in lines:
		if 'true' in line:
			if '@attribute classfication_tag' in line:
				line = '@attribute classfication_tag {true,false}\n'
			if '@attribute classification_tag' in line:
				line = '@attribute classification_tag {true,false}\n'
		else:
			if '@attribute classification_tag' in line:
				line = '@attribute classification {title,author,pubnum,date,abstract,affiliation,address,page,email,degree,note,phone,intro,keyword,web}\n'
		fout.write(line)
	fout.close()
	print 'arffת�����'

def getTag(oneline):
	list = oneline.split('::line_number::')
	line = list[0].strip()
	for tag in re.findall(r'<\w+>',line):
		return tag[1:-1]

if __name__ == '__main__':
	print getTag(r'<affiliation> Georgia Institute of Technology  </affiliation>')