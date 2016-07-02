# -*- coding: utf-8 -*- 
import os
import Config
import sys
import StringManager
import re
import Author
os.chdir(Config.WORKSPACE)

#获得地址、对应的行
def getAddress(header, label):
	address=[]
	addressLine = []
	for i in range(len(header)):
		if label[i] == '<address>':
			originLen = len(address)
			address.append(header[i])
			address = [x.strip() for x in address if x not in ['']]
			for j in range(len(address) - originLen):
				addressLine.append(i)
	assert(len(address) == len(addressLine))
	StringManager.clusterSameLine(address, addressLine)
	return address, addressLine
#获得地址、地址编号、对应的行
def getAddressWithIndex(header, label):
	address=[]
	addressIndex = []
	addressLine = []
	for i in range(len(header)):
		if label[i] == '<address>':
			print 'debug:',header[i]
			originLen = len(address)
			if StringManager.hasDigit(header[i]):
				address += re.split(r'\d(?:,\d)*', re.sub(r'\d\d+','',header[i]))
			else:
				address.append(header[i])
			address = [x.strip() for x in address if x not in ['']]
			for j in range(len(address) - originLen):
				addressLine.append(i)
			addressIndex += re.findall(r'\d(?:,\d)*', re.sub(r'\d\d+','',header[i]))
			addressIndex = [x.strip() for x in addressIndex if x not in ['']]
	assert(len(address) == len(addressLine))
	StringManager.clusterSameLine(address, addressLine)
	return address, addressIndex, addressLine

#为authorInfo更新每个作者的地址信息
def updateAddress(authors, address, authorInfo, authorsLine, addressLine):
	if len(authors) == len(address):#作者数目和收集到的归属数目相同
		for i in range(len(authors)):
			authorInfo[i].address = address[i]
	else:#数目不同，找离自己最近的
		for i in range(len(authors)):
			lineno = authorsLine[i]
			for j in range(len(address)):
				if addressLine[j] > lineno:
					authorInfo[i].address = address[j]
					break

#根据获取到的地址、地址编号、对应的行， 做地址编号到地址的映射
def getDicForAffliations(affliations, affliationsIndex):
	idAffliations={}
	for i in range(len(affliationsIndex)):
		s = affliationsIndex[i].strip()
		if affliationsIndex[i].strip().isdigit():
			idx = int(affliationsIndex[i].strip())
			idAffliations[idx] = affliations[idx-1]
	return idAffliations