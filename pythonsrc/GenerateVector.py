# -*- coding: utf-8 -*- 
import LineSpecific
import WordSpecific
import re
import os
addrpre = r'C:/Users/rainto96/workspace/HeaderXtractor/resource/allClassification/'
fout=open('C:/Users/rainto96/workspace/HeaderXtractor/vector.csv','w')
fout.close()
fout=open('C:/Users/rainto96/workspace/HeaderXtractor/vector.csv','w+')
startFlag=True

def __printVector(vector):
	global startFlag
	if startFlag == True:
		startFlag=False
		for key in vector:
			fout.write(str(key)+',')
		fout.write('\n')
	for key in vector:
		fout.write(str(vector[key])+',')
	fout.write('\n')
def __removeTag(line):
	str=line
	for tag in re.findall(r'<\w+>',line):
		str = str.replace(tag, '')
	for tag in re.findall(r'</\w+>',line):
		str = str.replace(tag, '')
	return str
def __getPositive(classification):
	s=open(addrpre+classification).readlines()
	for line in s:
		vector = {}
		vector['classfication_tag'] = 'true'
		line = line.strip()
		line = __removeTag(line)
		line = line.strip()
		line = line.replace(',',' ')
		for word in line.split(' '):
			WordSpecific.updateWordSpecificVector(word,vector)
		LineSpecific.updateLineSpecificVector(line,vector)
		__printVector(vector)

def __getNegative(classification):
	for file in os.listdir(addrpre):
		if file == classification:
			continue
		s=open(addrpre+file).readlines()
		for line in s:
			vector = {}
			vector['classfication_tag'] = 'false'
			line = line.strip()
			line = __removeTag(line)
			line = line.strip()
			line = line.replace(',',' ')
			for word in line.split(' '):
				WordSpecific.updateWordSpecificVector(word,vector)
			LineSpecific.updateLineSpecificVector(line,vector)
			__printVector(vector)
'''
生成向量文件到C:/Users/rainto96/workspace/HeaderXtractor/vector.csv
classification: 文件名称 ，如address.txt
'''
def generateVectorFor(classification):
	__getPositive(classification)
	__getNegative(classification)
	

'''
测试
'''
#print __removeTag(r'<address> Pittsburgh, PA 15213 D-79110 Freiburg, Germany D-53117 Bonn, Germany Austin, TX 78712  </address>')
#getPositive('address.txt')
#getNegative('address.txt')