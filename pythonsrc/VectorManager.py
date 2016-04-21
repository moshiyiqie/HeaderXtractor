# -*- coding: utf-8 -*- 
import Config
'''
��ӡһ��vectorList��csv�ļ���ʽ��ָ���˹���ע��tag�������Ҹ��з������
'''
def printVectorListToCSV(vectorList, outputPath, tagColName):
	if len(vectorList) == 0:
		print '�����б�Ϊ��'
		return
	
	fout = open(outputPath, 'w')
	#��ӡԪ��Ϣ
	for key in vectorList[0]:
		if key==tagColName:
			continue
		fout.write(str(key)+',')
	fout.write(tagColName+'\n')
	#��ӡ����
	for vector in vectorList:
		for key in vector:
			if key==tagColName:
				continue
			fout.write(str(vector[key])+',')
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
	