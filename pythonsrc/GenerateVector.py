# -*- coding: utf-8 -*- 
import LineSpecific
import WordSpecific
import re
import os
import pickle
addrpre = r'C:/Users/rainto96/workspace/HeaderXtractor/resource/allClassification/'
startFlag=True
def __printVector(vector):
	global startFlag
	if startFlag == True:
		startFlag=False
		for key in vector:
			if key=='classfication_tag':
				continue
			fout.write(str(key)+',')
		fout.write('classfication_tag'+'\n')
	for key in vector:
		if key=='classfication_tag':
			continue
		fout.write(str(vector[key])+',')
	fout.write(str(vector['classfication_tag'])+'\n')
def __removeTag(line):
	str=line
	for tag in re.findall(r'<\w+>',line):
		str = str.replace(tag, '')
	for tag in re.findall(r'</\w+>',line):
		str = str.replace(tag, '')
	return str

CACHE_VECTOR={}
CACHE_VECTOR_PATH=r'C:\Users\rainto96\workspace\HeaderXtractor\CACHE_VECTOR'
def __clearCache():
	if os.path.exists(CACHE_VECTOR_PATH):
		os.remove(CACHE_VECTOR_PATH)

#只具有行特征和词特征的特征向量
def __getBasicVector(oneline):
	list = oneline.split('::line_number::')
	line = list[0].strip()
	linePos = list[1].strip()
	
	vector = {}
	vector['linePos'] = linePos
	#vector['origin_data'] = '"'+line.strip().replace('"','')+'"'
	line = line.strip()
	line = __removeTag(line)
	line = line.strip()
	line = line.replace(',',' ')
	list = line.split()
	for word in list:
		WordSpecific.updateWordSpecificVector(word,vector)
	LineSpecific.updateLineSpecificVector(line,vector)
	return vector
def __handleTaggedLine(s,pos_neg,filename):
	line_count=0
	for oneline in s:
		if line_count%100 == 0:
			print filename+':'+str(line_count)+' row'
		line_count+=1
		list = oneline.split('::line_number::')
		line = list[0].strip()
		linePos = list[1].strip()
		
		vector = {}
		vector['classfication_tag'] = pos_neg
		vector['linePos'] = linePos
		#vector['origin_data'] = '"'+line.strip().replace('"','')+'"'
		line = line.strip()
		line = __removeTag(line)
		line = line.strip()
		line = line.replace(',',' ')
		list = line.split()
		for word in list:
			WordSpecific.updateWordSpecificVector(word,vector)
		LineSpecific.updateLineSpecificVector(line,vector)
		CACHE_VECTOR[filename].append(vector)
def __getPositive(classification):
	if not CACHE_VECTOR.has_key(classification):
		CACHE_VECTOR[classification]=[]
		print 'Geting File:%s Vector ...'%classification
		s=open(addrpre+classification).readlines()
		__handleTaggedLine(s,'true',classification)
	for vector in CACHE_VECTOR[classification]:
		vector['classfication_tag'] = 'true'
		__printVector(vector)

def __getNegative(classification):
	for file in os.listdir(addrpre):
		if file == classification:
			continue
		if not CACHE_VECTOR.has_key(file):
			CACHE_VECTOR[file]=[]
			print 'Geting File:%s Vector ...'%file
			s=open(addrpre+file).readlines()
			__handleTaggedLine(s,'false',file)
		for vector in CACHE_VECTOR[file]:
			vector['classfication_tag'] = 'false'
			__printVector(vector)
'''
生成向量文件到C:/Users/rainto96/workspace/HeaderXtractor/vector.csv
classification: 文件名称 ，如address.txt
'''
def generateVectorFor(classification):
	global fout
	global startFlag
	global CACHE_VECTOR
	startFlag=True
	fout=open('C:/Users/rainto96/workspace/HeaderXtractor/vector.csv','w')
	fout.close()
	fout=open('C:/Users/rainto96/workspace/HeaderXtractor/vector.csv','w+')
	
	
	if os.path.exists(CACHE_VECTOR_PATH):
		print 'Load CACHE_VECTOR from disk ...'
		CACHE_VECTOR=pickle.load(open(CACHE_VECTOR_PATH))
	print 'Generating Vectoring ...'
	__getPositive(classification)
	__getNegative(classification)
	fout.close()
	
	print 'CSV向量生成完毕，正在转化为arff'
	#os.popen(r'java -classpath "C:/Program Files (x86)/Weka-3-6/weka.jar" weka.core.converters.CSVLoader C:/Users/rainto96/workspace/HeaderXtractor/vector.csv > C:/Users/rainto96/workspace/HeaderXtractor/vector.arff')
	os.system(r'java -classpath "C:/Program Files (x86)/Weka-3-6/weka.jar" weka.core.converters.CSVLoader C:/Users/rainto96/workspace/HeaderXtractor/vector.csv > C:/Users/rainto96/workspace/HeaderXtractor/vector.arff')
	print 'arff向量转化完毕'
	print 'Write CACHE_VECTOR to disk ...'
	pickle.dump(CACHE_VECTOR,open(CACHE_VECTOR_PATH,'w'),0)

	
if __name__ == '__main__':
	#__clearCache()
	generateVectorFor('abstract.txt')
	'''
	测试
	'''
	#print __removeTag(r'<address> Pittsburgh, PA 15213 D-79110 Freiburg, Germany D-53117 Bonn, Germany Austin, TX 78712  </address>')
	#getPositive('address.txt')
	#getNegative('address.txt')