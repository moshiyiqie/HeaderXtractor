# -*- coding: utf-8 -*- 
import os
import Config
import sys
import StringManager
import re
import Author
os.chdir(Config.WORKSPACE)
#获得归属、归属编号、对应的行
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

#根据获取到的作者、作者编号、对应的行， 做作者名到作者编号的映射
def getDicForAuthor(authors, authorsIndex):
	idAuthors={}
	for i in range(len(authorsIndex)):
		idxList = authorsIndex[i].split(',')
		idxList = [int(x.strip()) for x in idxList if x != '' and x.isdigit()]
		idAuthors[authors[i]] = idxList
	return idAuthors

#根据获取到的归属、归属编号、对应的行， 做归属编号到归属的映射
def getDicForAffliations(affliations, affliationsIndex):
	idAffliations={}
	for i in range(len(affliationsIndex)):
		s = affliationsIndex[i].strip()
		if affliationsIndex[i].strip().isdigit():
			idx = int(affliationsIndex[i].strip())
			idAffliations[idx] = affliations[idx-1]
			
	return idAffliations