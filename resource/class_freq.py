# -*- coding: utf-8 -*- 
import re
import os

def wordCount():
	add=r'D:/涛Work/gitDomainPractice/HeaderXtractor/resource'
	#add=add.replace('\\','/')
	for file in os.listdir(add+r'/各类语料'):
		fout=open(add+r'/词频/'+file,'w')
		list = ''.join(open(add+r'/各类语料/'+file).readlines()).split(' ')
		st = set(list)
		list = [(term,str(list.count(term))) for term in st]
		list.sort(key=lambda d:int(d[1]),reverse=True)
		for one in list:
			ss=one[0]
			ss=ss.replace('\n','')
			if(len(ss)<1):
				continue
			fout.write(ss+' '+one[1]+'\n')
		fout.close()
def getTrainTestSet():
	add=r'C:/Users/rainto96/workspace/HeaderXtractor/resource'
	for file in os.listdir(add+r'/allClassification'):
		all=open(add+r'/allClassification/'+file).readlines()
		train=all[0:len(all)/2]
		test=all[len(all)/2:]
		w1=open(add+'/train/'+file,'w')
		w2=open(add+'/test/'+file,'w')
		for line in train:
			w1.write(line)
		for line in test:
			w2.write(line)
		w1.close()
		w2.close()
		
def getPostCode():
	add=r'C:/Users/rainto96/workspace/HeaderXtractor/resource'
	s=re.findall(r'[A-Z][.,]?[A-Z][.,]? [0-9]{5}', ''.join(open(add+'/train/address.txt').readlines()))
	w1=open(add+'/db/postcode.txt','w')
	w2=open(add+'/db/postcode_prefix.txt','w')
	prefix = []
	for line in s:
		w1.write(line+'\n')
		prefix.append(line.split(' ')[0].replace(',','').replace('.',''))
	for line in set(prefix):
		w2.write(line+'\n')
'''
main
'''	
getPostCode()