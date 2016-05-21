# -*- coding: utf-8 -*- 
import os
os.chdir(r'D:\涛Work\gitDomainPractice\HeaderXtractor')
import re
lines = open('./CRF++/train/result.txt').readlines()
dic={}
labelset = ['<web>', '<keyword>', '<author>', '<title>', '<abstract>', 
			'<pubnum>', '<date>', '<address>', '<email>', '<phone>', 
			'<page>', '<note>', '<affiliation>', '<degree>', '<intro>']
for label in labelset:
	for label2 in labelset:
		if not dic.has_key(label):
			dic[label] = {}
		if not dic[label].has_key(label2):
			dic[label][label2]=0

for line in lines:
	line = line.strip()
	if len(line) == 0: continue
	labels = re.findall(r'<\w+>', line)
	if not dic.has_key(labels[0]):
		dic[labels[0]]={}
	if not dic[labels[0]].has_key(labels[1]):
		dic[labels[0]][labels[1]]=0
	dic[labels[0]][labels[1]]+=1



fout = open('./out.csv','w')
fout.write(' ,')
for label in labelset: fout.write(label + ',')
fout.write('\n')
for label in labelset:
	fout.write(label + ',')
	for label2 in labelset:
		fout.write(str(dic[label][label2])+',')
	fout.write('\n')
fout.write('\n类别,准确率,召回率,F1值,样本个数')
for label in labelset:
	fout.write('\n')
	a2a = dic[label][label]
	b2a = sum( [dic[y][label] for y in labelset if y != label] )
	a2b = sum( [dic[label][y] for y in labelset if y != label] )
	b2b = sum( [dic[y][z] for y in labelset for z in labelset if y!=label or z!=label] ) - b2a
	if a2a+b2a == 0: precision = 0
	else:
		precision = a2a*1.0/(a2a+b2a)
	if a2a+a2b == 0: recall = 0
	else:
		recall=a2a*1.0/(a2a+a2b)
	if precision + recall == 0: f1=0
	else:
		f1=2*precision*recall/(precision + recall)
	fout.write(','.join([label, str(precision), str(recall), str(f1), str(a2a + a2b)]))
	
fout.close()