# -*- coding: utf-8 -*- 
import LineSpecific
import WordSpecific
import re
import os
import pickle
addrpre = r'C:/Users/rainto96/workspace/HeaderXtractor/resource/allClassification/'
startFlag=True
fout=open('C:/Users/rainto96/workspace/HeaderXtractor/vector.csv','w')
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
def __getPositive(classification):
	if not CACHE_VECTOR.has_key(classification):
		CACHE_VECTOR[classification]=[]
		print 'Geting File:%s Vector ...'%classification
		s=open(addrpre+classification).readlines()
		for line in s:
			vector = {}
			vector['classfication_tag'] = 'true'
			#vector['origin_data'] = '"'+line.strip().replace('"','')+'"'
			line = line.strip()
			line = __removeTag(line)
			line = line.strip()
			line = line.replace(',',' ')
			for word in line.split(' '):
				WordSpecific.updateWordSpecificVector(word,vector)
			LineSpecific.updateLineSpecificVector(line,vector)
			CACHE_VECTOR[classification].append(vector)
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
			for line in s:
				vector = {}
				vector['classfication_tag'] = 'false'
				#vector['origin_data'] = '"'+line.strip().replace('"','')+'"'
				line = line.strip()
				line = __removeTag(line)
				line = line.strip()
				line = line.replace(',',' ')
				for word in line.split(' '):
					WordSpecific.updateWordSpecificVector(word,vector)
				LineSpecific.updateLineSpecificVector(line,vector)
				CACHE_VECTOR[file].append(vector)
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
	
	
	if os.path.exists(r'C:\Users\rainto96\workspace\HeaderXtractor\CACHE_VECTOR'):
		print 'Load CACHE_VECTOR from disk ...'
		CACHE_VECTOR=pickle.load(open(r'C:\Users\rainto96\workspace\HeaderXtractor\CACHE_VECTOR'))
	print 'Generating Vectoring ...'
	__getPositive(classification)
	__getNegative(classification)
	fout.close()
	
	print 'CSV向量生成完毕，正在转化为arff'
	#os.popen(r'java -classpath "C:/Program Files (x86)/Weka-3-6/weka.jar" weka.core.converters.CSVLoader C:/Users/rainto96/workspace/HeaderXtractor/vector.csv > C:/Users/rainto96/workspace/HeaderXtractor/vector.arff')
	os.system(r'java -classpath "C:/Program Files (x86)/Weka-3-6/weka.jar" weka.core.converters.CSVLoader C:/Users/rainto96/workspace/HeaderXtractor/vector.csv > C:/Users/rainto96/workspace/HeaderXtractor/vector.arff')
	print 'arff向量转化完毕'
	print 'Write CACHE_VECTOR to disk ...'
	pickle.dump(CACHE_VECTOR,open(r'C:\Users\rainto96\workspace\HeaderXtractor\CACHE_VECTOR','w'),0)

	
if __name__ == '__main__':
	generateVectorFor('title.txt')
	'''
	测试
	'''
	#print __removeTag(r'<address> Pittsburgh, PA 15213 D-79110 Freiburg, Germany D-53117 Bonn, Germany Austin, TX 78712  </address>')
	#getPositive('address.txt')
	#getNegative('address.txt')