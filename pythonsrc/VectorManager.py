# -*- coding: utf-8 -*- 
import Config
'''
打印一个vectorList成csv文件格式，指定人工标注的tag列名，且该列放在最后
'''
def printVectorListToCSV(vectorList, outputPath, tagColName):
	if len(vectorList) == 0:
		print '向量列表为空'
		return
	
	fout = open(outputPath, 'w')
	#打印元信息
	for key in vectorList[0]:
		if key==tagColName:
			continue
		fout.write(str(key)+',')
	fout.write(tagColName+'\n')
	#打印向量
	for vector in vectorList:
		for key in vector:
			if key==tagColName:
				continue
			fout.write(str(vector[key])+',')
		fout.write(str(vector[tagColName])+'\n')
	fout.close()
'''
打印一个vectorList成arff文件格式，指定人工标注的tag列名，且该列放在最后
'''
def printVectorListToARFF(vectorList, outputPath, tagColName):
	tmpCSV_Addr = Config.TMP_ADDR+r'/tmp.csv'
	printVectorListToCSV(vectorList,tmpCSV_Addr,tagColName)
	print '正在转化为arff'
	os.system(r'java -classpath "C:/Program Files (x86)/Weka-3-6/weka.jar" weka.core.converters.CSVLoader %s > %s'%(tmpCSV_Addr, outputPath))
	print 'arff转化完毕'
	