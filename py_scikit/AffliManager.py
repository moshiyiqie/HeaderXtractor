# -*- coding: utf-8 -*- 
import os
import Config
import sys
import StringManager
import re
import Author
os.chdir(Config.WORKSPACE)
#��ù�����������š���Ӧ����
def getAffliations(header, label):
	affliations=[]
	affliationsIndex = []
	affliationsLine = []
	for i in range(len(header)):
		if label[i] == '<affiliation>':
			print 'debug:',header[i]
			originLen = len(affliations)
			if StringManager.hasDigit(header[i]):
				#affliations += re.split(r'\d(?:,\d)*', header[i])
				affliations += re.split(r'\d(?:,\d)*', re.sub(r'\d\d+','',header[i]))
			else:
				affliations.append(header[i])
			affliations = [x.strip() for x in affliations if x not in ['']]
			for j in range(len(affliations) - originLen):
				affliationsLine.append(i)
			#affliationsIndex += re.findall(r'\d(?:,\d)*', header[i])
			affliationsIndex += re.findall(r'\d(?:,\d)*', re.sub(r'\d\d+','',header[i]))
			affliationsIndex = [x.strip() for x in affliationsIndex if x not in ['']]
	assert(len(affliations) == len(affliationsLine))
	#print 'affliation and lineNo', affliations, affliationsLine
	StringManager.clusterSameLine(affliations, affliationsLine)
	return affliations, affliationsIndex, affliationsLine



#���ݻ�ȡ���Ĺ�����������š���Ӧ���У� ��������ŵ�������ӳ��
def getDicForAffliations(affliations, affliationsIndex):
	idAffliations={}
	for i in range(len(affliationsIndex)):
		s = affliationsIndex[i].strip()
		if affliationsIndex[i].strip().isdigit():
			idx = int(affliationsIndex[i].strip())
			idAffliations[idx] = affliations[idx-1]
	return idAffliations