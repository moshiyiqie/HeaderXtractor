# -*- coding: utf-8 -*- 
import os
import Config
import sys
import StringManager
import re
import Author
os.chdir(Config.WORKSPACE)

#��õ�ַ����Ӧ����
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

#ΪauthorInfo����ÿ�����ߵĵ�ַ��Ϣ
def updateAddress(authors, address, authorInfo, authorsLine, addressLine):
	if len(authors) == len(address):#������Ŀ���ռ����Ĺ�����Ŀ��ͬ
		for i in range(len(authors)):
			authorInfo[i].address = address[i]
	else:#��Ŀ��ͬ�������Լ������
		for i in range(len(authors)):
			lineno = authorsLine[i]
			for j in range(len(address)):
				if addressLine[j] > lineno:
					authorInfo[i].address = address[j]
					break