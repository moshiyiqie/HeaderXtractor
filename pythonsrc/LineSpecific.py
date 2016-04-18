# -*- coding: utf-8 -*- 
import WordSpecific
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

	
	
flist = [dictWordNumPer, nonDictWordNumPer, cap1DicWordNumPer,
		cap1NonDicWordNumPer, digitNumPer, affiNumPer, addrNumPer, 
		dateNumPer, degreeNumPer, phoneNumPer, pubNumPer, noteNumPer,singleDigitNumPer]
def updateLineSpecificVector(line,vector):
	for fun in flist:
		if not vector.has_key(fun.__name__):
			vector[fun.__name__]=0
		vector[fun.__name__] += float(fun(line))

if __name__ == '__main__':
	'''
	≤‚ ‘

	vector={}
	updateLineSpecificVector('alaska dr 13269579910 lab Mary mary',vector)
	print vector
	print '-----------------------------------'
	print cap1DicWordNumPer('Mary mary sdfsd Ssdfs')
	print digitNumPer('12321 good 3s')
	print dictWordNumPer('rainto@dd.com ALASKA mary sdfsadfa alalala')
	print countDic('rainto@dd.com gsdf dsfasd@dfsa.cs',WordSpecific.isEmail)
	'''