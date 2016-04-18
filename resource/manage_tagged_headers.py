import os
import re
fin = open(r'C:\Users\rainto96\workspace\HeaderXtractor\resource\tagged_headers.txt','r').readlines()
fin = [x.strip().replace('+L+','').replace('\n','') for x in fin]
pos=0

def getLinePosInfo():
	fout = open('C:/ZONE/out.txt','w')
	for line in open(r'C:\Users\rainto96\workspace\HeaderXtractor\resource\sparsed_tagged_header.txt').readlines():
		line = line.strip()
		if line == '<NEW_HEADER>': 
			pos=0
			continue
		fout.write(line.strip() + '::line_number::' + str(pos)+'\n')
		pos+=1
	fout.close()

def genToAllClassificationFolder():
	dic={}
	for line in open(r'C:\Users\rainto96\workspace\HeaderXtractor\resource\sparsed_tagged_header_with_line_number.txt').readlines():
		line=line.strip()
		filename = re.findall(r'<\w+>', line)[0][1:-1]+'.txt'
		if not dic.has_key(filename): dic[filename]=[]
		dic[filename].append(line)
	for filename in dic:
		fout = open(r'C:/Users/rainto96/workspace/HeaderXtractor/resource/allClassification/'+filename,'w')
		for line in dic[filename]:
			fout.write(line+'\n')
		fout.close()

def getSparsedTaggedHeader():
	fout=open('C:/ZONE/out.txt','w')
	for element in re.findall(r'<\w*>.*?</\w*>', ''.join(fin)):
		if '<NEW_HEADER>' in element:
			element = element[len('<NEW_HEADER>'):]
			fout.write('<NEW_HEADER>'+'\n')
		fout.write(element+'\n')

genToAllClassificationFolder()