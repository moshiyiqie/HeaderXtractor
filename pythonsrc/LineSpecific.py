# -*- coding: utf-8 -*- 
import WordSpecific
import Config
import os
import re
os.chdir(Config.WORKSPACE)
def countDic(line,func):
	num=0
	for word in line.split(' '):
		num += int(func(word))
	return num, num*1.0 / senLen(line)
def inAnyDic(word):
	for func in WordSpecific.diclist:
		if func(word):
			return True
	return False
def senLen(line):
	return len(line.split(' '))

#--------------------attribute in paper----------------------------
def dictWordNumPer(line):
	num=0
	for word in line.split(' '):
		num += inAnyDic(word)
	return num*1.0/senLen(line)
def nonDictWordNumPer(line):
	return 1-dictWordNumPer(line)
def cap1DicWordNumPer(line):
	num=0
	all=1
	for word in line.split(' '):
		if len(word)>=1 and str.isupper(word[0]):
			all+=1
			num += inAnyDic(word)
	return num*1.0/all
def cap1NonDicWordNumPer(line):
	return 1-cap1DicWordNumPer(line)
def digitNumPer(line):
	num=0
	for word in line.split(' '):
		num += str.isdigit(word)
	return num*1.0/senLen(line)
def singleDigitNumPer(line):
	num=0
	all=0
	for word in line.split():
		for ch in word:
			all+=1
			if str.isdigit(ch):
				num+=1
	return num*1.0/(all+1)

def singleAlphaNumPer(line):
	num=0
	all=0
	for word in line.split():
		for ch in word:
			all+=1
			if str.isalpha(ch):
				num+=1
	return num*1.0/(all+1)

def affiNumPer(line):
	return countDic(line,WordSpecific.isAffi)[1]
def addrNumPer(line):
	return countDic(line,WordSpecific.isAddr)[1]
def dateNumPer(line):
	return countDic(line,WordSpecific.isMonth)[1]
def degreeNumPer(line):
	return countDic(line,WordSpecific.isDegree)[1]
def phoneNumPer(line):
	return countDic(line,WordSpecific.isPhone)[1]
def pubNumPer(line):
	return countDic(line,WordSpecific.isPubNum)[1]
def noteNumPer(line):
	return countDic(line,WordSpecific.isNote)[1]

#CRFneed
#->INITCAP
def cap1NumPer(line):
	num=0
	for word in line.split():
		if len(word)>=1 and str.isupper(word[0]):
			num += 1
	return num*1.0/len(line.split())
def capAllNumPer(line):
	num=0
	for word in line.split():
		if len(word)>=1 and str.isupper(word):
			num += 1
	return num*1.0/len(line.split())

def containDigit(line):
	for word in line.split():
		for ch in word:
			if str.isdigit(ch):
				return 1
	return 0
def allDigit(line):
	alphaNum=0
	digitNum=0
	for ch in line:
		if str.isalpha(ch): alphaNum += 1
		elif str.isdigit(ch): digitNum += 1
	return alphaNum == 0 and digitNum > 0
	#return str.isdigit(line.replace(' ',''))
def containDot(line):
	return '.' in line
def containDash(line):
	return '-' in line
def lonelyInitialPer(line):
	return len(re.findall(r'\w\.',line))*1.0/len(line.split())
def singleCharPer(line):
	num=0
	for word in line.split():
		if len(word)==1 and str.isalpha(word):
			num+=1
	return num*1.0/len(line.split())
def cap1Per(line):
	num=0
	for word in line.split():
		if len(word)==1 and str.isupper(word):
			num+=1
	return num*1.0/len(line.split())
def puncPer(line):
	num=0
	num += line.count('.')
	num += line.count(',')
	return num*1.0 / len(line.split())
def emailPer(line):
	return countDic(line,WordSpecific.isEmail)[1]
def urlPer(line):
	return countDic(line,WordSpecific.isURL)[1]
def authorPer(line):
	return countDic(line,WordSpecific.isMayName)[1]
def keywordPer(line):
	return countDic(line,WordSpecific.isKeyWord)[1]
def comaNum(line):
	return  line.count(',')
def shortPhrasePer(line):
	list = line.split(',')
	cnt = 0
	for ele in list:
		if len(ele.split()) <= 3:
			cnt+=1
	return cnt*1.0 / len(list)
#数字字符是否多于等于7个
def digitMore7(line):
	digitNum=0
	for ch in line:
		if str.isdigit(ch):
			digitNum += 1
	return digitNum >= 7
#连续数字字符是否多于等于3个
def digitMore3(line):
	digitNum=0
	for ch in line:
		if str.isdigit(ch):
			digitNum += 1
			if digitNum >= 3: return True
		else:
			digitNum = 0
	return False
#是否有{或者}括号
def containLR(line):
	return '{' in line or '}' in line

#是否包含at
def containAt(line):
	return '@' in line
	

#CRFneed
	
	
#flist = [dictWordNumPer, nonDictWordNumPer, cap1DicWordNumPer,
#		cap1NonDicWordNumPer, digitNumPer, affiNumPer, addrNumPer, 
#		dateNumPer, degreeNumPer, phoneNumPer, pubNumPer, noteNumPer,singleDigitNumPer,
#		cap1NumPer, capAllNumPer, comaNum, shortPhrasePer]
flist = [dictWordNumPer, nonDictWordNumPer, cap1DicWordNumPer,
		cap1NonDicWordNumPer, digitNumPer, affiNumPer, addrNumPer, 
		dateNumPer, degreeNumPer, phoneNumPer, pubNumPer, noteNumPer,singleDigitNumPer]
def updateLineSpecificVector(line,vector):
	for fun in flist:
		if not vector.has_key(fun.__name__):
			vector[fun.__name__]=0
		vector[fun.__name__] += float(fun(line))

#CRF的特征选择
pickedFeature_CRF = [cap1NumPer, capAllNumPer, containDigit, allDigit, phoneNumPer, 
					containDot, containDash, lonelyInitialPer, singleCharPer,
					cap1Per, puncPer, emailPer, urlPer, authorPer, dateNumPer, noteNumPer, affiNumPer,keywordPer, shortPhrasePer, singleDigitNumPer, singleAlphaNumPer,
					digitMore7, digitMore3, containLR, containAt]
def updateForCRF(line,vector):
	for fun in pickedFeature_CRF:
		if not vector.has_key(fun.__name__):
			vector[fun.__name__]=0
		vector[fun.__name__] += float(fun(line))
if __name__ == '__main__':
	#print digitMore3('223425')
	#print digitMore3('22acds33s2 24')
	#print digitMore3('222acds33s2 24')
	#print digitMore3('22acds332s2 24')

	#print containAt('sdfsdf@fsd@f.sdf')
	#print containAt('sdfsdf@fsdf.sdf')
	#print containAt('sdfsdf#fsdf.sdf')
	
	#print containLR('{abc}')
	#print containLR('{sss')
	#print containLR('998a}')
	#print containLR('998a')
	
	#print allDigit(' 132-5957-9999')
	#print allDigit(' 132-5957-9999a')

	#print capAllNumPer('in Multi-hop Radio Networks')
	#print comaNum('good,henhao,haha')
	'''
	测试
	#test for CRFfunction BEGIN
	#print cap1NumPer('A good N nice')
	#print capAllNumPer('ABS good HERE')
	#print containDigit('3 here')
	#print containDigit('what here')
	#print allDigit('132 443 43')
	#print phoneNumPer('tel: 1932')
	#print containDot('here.f')
	#print containDot('heresf')
	#print containDash('here-f')
	#print containDash('heref')
	#print lonelyInitialPer('E.Liu E. Yang Here')
	#print singleCharPer('A sdfs B sdf b')
	#print cap1Per('A sdf B sdf b')
	#print puncPer(', here . good .')
	#print emailPer('lrt 4504951@dd.ss gd')
	#print authorPer('Mary dsfsfa good jack')
	#test for CRFfunction END
	
	vector={}
	updateLineSpecificVector('alaska dr 13269579910 lab Mary mary',vector)
	print vector
	print '-----------------------------------'
	print cap1DicWordNumPer('Mary mary sdfsd Ssdfs')
	print digitNumPer('12321 good 3s')
	print dictWordNumPer('rainto@dd.com ALASKA mary sdfsadfa alalala')
	print countDic('rainto@dd.com gsdf dsfasd@dfsa.cs',WordSpecific.isEmail)
	'''