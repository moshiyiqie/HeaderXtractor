# -*- coding: utf-8 -*- 
import os
import re
#�����ǽ�+L+ȥ������һ����Ǻϲ�Ϊһ�У�����+L+�ǻ��У�һ��һ�����
def getEveryLineFromTaggedHeaders():
	f = open(r'D:\��work\gitDomainPractice\HeaderXtractor\resource\tagged_headers.txt')
	fout = open(r'D:/everyline.txt','w')
	s = f.readlines()
	label=''
	lineno=0
	for line in s:
		line = line.strip()
		if len(line) == 0: continue
		if 'NEW_HEADER>' in line:
			#fout.write(line+'\n')
			lineno=0
			continue
		line = line.replace('+L+','')
		l = re.findall(r'<\w*>',line)
		if len(l) > 0:
			label = l[0][1:-1]
		line = re.sub(r'</?\w*>','',line)
		line = '<'+label+'> '+ line + ' </'+label+'>'
		fout.write(line+'::line_number::'+str(lineno)+'\n')
		lineno+=1
	fout.close()