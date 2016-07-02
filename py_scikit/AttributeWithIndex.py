# -*- coding: utf-8 -*- 
import os
import Config
import sys
import StringManager
import re
import Author
os.chdir(Config.WORKSPACE)

#获得属性、属性编号、对应的行
def getAttributes(header, label, attributeKind):
	attributes=[]
	attributesIndex = []
	attributesLine = []
	for i in range(len(header)):
		if label[i] == '<'+attributeKind+'>':
			print 'debug:',header[i]
			originLen = len(attributes)
			if PdfManager.hasIndex(i):
				#attributes += re.split(r'\d(?:,\d)*', header[i])
				#attributes += re.split(r'\d(?:,\d)*', re.sub(r'\d\d+','',header[i]))
			else:
				attributes.append(header[i])
			attributes = [x.strip() for x in attributes if x not in ['']]
			for j in range(len(attributes) - originLen):
				attributesLine.append(i)
			#attributesIndex += re.findall(r'\d(?:,\d)*', header[i])
			attributesIndex += re.findall(r'\d(?:,\d)*', re.sub(r'\d\d+','',header[i]))
			attributesIndex = [x.strip() for x in attributesIndex if x not in ['']]
	assert(len(attributes) == len(attributesLine))
	#print 'attribute and lineNo', attributes, attributesLine
	StringManager.clusterSameLine(attributes, attributesLine)
	return attributes, attributesIndex, attributesLine

#根据获取到的属性、属性编号、对应的行， 做属性编号到属性的映射
def getDicForAttributes(attributes, attributesIndex):
	idAttributes={}
	for i in range(len(attributesIndex)):
		s = attributesIndex[i].strip()
		if attributesIndex[i].strip().isdigit():
			idx = int(attributesIndex[i].strip())
			idAttributes[idx] = attributes[idx-1]
	return idAttributes

def matchAuthorAttributes(author, idAuthor, idAttributes):
	attribute=''
	if idAuthor.has_key(author) and len(idAttributes) > 0: 
		for idx in idAuthor[author]:
			attribute += idAttributes[idx] + ' ||| '
		attribute = attribute[:-5]
	return attribute