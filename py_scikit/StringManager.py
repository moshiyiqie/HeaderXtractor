# -*- coding: utf-8 -*- 
import os
import Config
import sys
import PdfProcessor
os.chdir(Config.WORKSPACE)
import Pdf

#是否包含数字
def hasDigit(s):
	for ch in s:
		if str.isdigit(ch): return True
	return False
	
#是否有大逗号，指的是非角标编号中的逗号
def hasBigComma(s, tmpStr):
	has = False
	s = s.replace(' and ', ' , ')
	s = s.replace('*', '')
	tmp=''
	for word in s.split():
		for i in range(len(word)):
			if word[i]==',' and (i==0 or not str.isdigit(word[i-1]) ) and (i+1==len(word) or not str.isdigit(word[i+1])  ):
				word= word[:i] + '#' + word[i+1:]
				has = True
		tmp += word + ' '
	tmpStr.append(tmp)
	return has
	
#把本应该是同一行的归属聚集起来
def clusterSameLine(property, propertyLine, pdf):
	length = len(property)
	i=1
	while i<length:
		if i >= length: break
		if propertyLine[i] - 1 == propertyLine[i-1]:
			if not pdf.hasIndex(propertyLine[i]):
				property[i-1] += ' ' + property[i]
				#print 'pop '+str(i) + ' '+ property[i] + '  lineno:' + str(propertyLine[i])
				property.pop(i)
				propertyLine[i-1] = propertyLine[i]
				propertyLine.pop(i)
				i-=1
		length = len(property)
		i+=1
	assert(len(property) == len(propertyLine))