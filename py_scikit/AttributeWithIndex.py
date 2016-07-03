# -*- coding: utf-8 -*- 
import os
import Config
import sys
import StringManager
import re
import Author
os.chdir(Config.WORKSPACE)

#获得属性、属性编号、对应的行
def getAttributes(header, label, attributeKind, pdf):
	attributes=[]
	attributesIndex = []
	attributesLine = []
	for i in range(len(header)):
		if label[i] == '<'+attributeKind+'>':
			originLen = len(attributes)
			#if StringManager.hasDigit(header[i]):
			#	attributes += re.split(r'\d(?:,\d)*', re.sub(r'\d\d+','',header[i]))
			#	attributesIndex += re.findall(r'\d(?:,\d)*', re.sub(r'\d\d+','',header[i]))
			if pdf.hasIndex(i):
				attributesListTmp, attributesIndexTmp = pdf.handleIndex(i)
				attributes += attributesListTmp
				attributesIndex += attributesIndexTmp
			else:
				attributes.append(header[i])
			attributes = [x.strip() for x in attributes if x not in ['']]
			for j in range(len(attributes) - originLen):
				attributesLine.append(i)
			
	assert(len(attributes) == len(attributesLine))
	#print 'attribute and lineNo', attributes, attributesLine
	StringManager.clusterSameLine(attributes, attributesLine, pdf)
	print 'attributes, attributesIndex', attributes, attributesIndex
	return attributes, attributesIndex, attributesLine

#根据获取到的属性、属性编号、对应的行， 做属性编号到属性的映射
def getDicForAttributes(attributes, attributesIndex):
	if len(attributesIndex) ==0 : return {}
	attributesIndexTmp = [x[0] for x in attributesIndex]
	if attributesIndexTmp[0].strip().isdigit():
		idAttributes={}
		for i in range(len(attributesIndexTmp)):
			s = attributesIndexTmp[i].strip()
			if attributesIndexTmp[i].strip().isdigit():
				idx = int(attributesIndexTmp[i].strip())
				idAttributes[idx] = attributes[idx-1]
		return idAttributes
	else:
		idAttributes={}
		for i in range(len(attributesIndexTmp)):
			if i >= range(len(attributes)):
				break
			idAttributes[attributesIndexTmp[i]] = attributes[i]
		return idAttributes

def matchAuthorAttributes(author, idAuthor, idAttributes):
	attribute=''
	if idAuthor.has_key(author) and len(idAttributes) > 0: 
		for idx in idAuthor[author]:
			if idAttributes.has_key(idx):
				attribute += idAttributes[idx] + ' ||| '
		attribute = attribute[:-5]
	return attribute