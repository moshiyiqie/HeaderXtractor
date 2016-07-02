# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import re
import StringManager
#������
class Author:
	name=''
	address=''
	affliation=''
	email=''
	def __init__(self, name='', address='', affliation='', email=''):
		self.name = name
		self.address = address
		self.affliation = affliation
		self.email = email
	def toString(self):
		outStr = ''
		if len(self.name)>0: outStr += '[Author name]:' + self.name + '\n'
		if len(self.address)>0: outStr += '[Address]:' + self.address + '\n'
		if len(self.affliation)>0: outStr += '[Affliation]:' + self.affliation + '\n'
		if len(self.email)>0: outStr += '[Email]:' + self.email + '\n'
		return outStr
	def toDic(self):
		dic={}
		dic['name'] = self.name
		dic['address'] = self.address
		dic['affliation'] = self.affliation
		dic['email'] = self.email
		return dic

def splitByBigSpace(line, xpos):
	words = line.strip().split()
	averageDist = 0
	for i in range(1,len(words)):
		averageDist += xpos[i][0] - xpos[i-1][1]
	averageDist /= len(words) - 1
	
	authors = []
	one = words[0]
	for i in range(1,len(words)):
		if xpos[i][0] - xpos[i-1][1] > averageDist:
			authors.append(one)
			one = words[i]
		else:
			one += ' ' + words[i]
	if one != '':
		authors.append(one)
	#print 'in splitByBigSpace():', authors, averageDist, xpos
	return authors

#��ȡ���ߡ����߱�š���Ӧ����
def getAuthors(header, label, xpos):
	authors = []
	authorsIndex = []
	authorsLine = []
	for i in range(len(header)):
		if label[i] == '<author>':
			tmpStr=[]
			originLen = len(authors)
			if StringManager.hasBigComma(header[i], tmpStr):
				authors += tmpStr[0].split('#')
			elif StringManager.hasDigit(header[i]):
				authors += re.split(r'\d(?:,\d)*', header[i])
			elif len(header[i].strip().split()) >= 4:
				authors += splitByBigSpace(header[i], xpos[i])
			else:
				authors.append(header[i])
			authors = [x.strip() for x in authors if x not in ['']]
			for j in range(len(authors) - originLen):
				authorsLine.append(i)
			authorsIndex += re.findall(r'\d(?:,\d)*', header[i])
			authorsIndex = [x.strip() for x in authorsIndex if x not in ['']]
	
	assert(len(authors) == len(authorsLine))
	
	length = len(authors)
	i=0
	while i < length:
		if authors[i] == '':
			authors.pop(i)
			authorsLine.pop(i)
		i+=1
		length = len(authors)
	
	return authors, authorsIndex, authorsLine
	
#���ݻ�ȡ�������ߡ����߱�š���Ӧ���У� �������������߱�ŵ�ӳ��
def getDicForAuthor(authors, authorsIndex):
	idAuthors={}
	for i in range(len(authorsIndex)):
		idxList = authorsIndex[i].split(',')
		idxList = [int(x.strip()) for x in idxList if x != '' and x.isdigit()]
		idAuthors[authors[i]] = idxList
	return idAuthors