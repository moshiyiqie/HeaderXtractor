# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import JudgeResult
##该类主要是分析ParsHed的头部预测结果性能

#生成测试文本（去除标注标签）
def analysisSelfData():
	goldpath='./py_scikit/train_center/cleaned_line_cls'
	text = []
	tag = []
	for file in os.listdir(goldpath):
		filepath = os.path.join(goldpath, file)
		lines = open(filepath).readlines()
		for line in lines:
			line = line.strip()
			if len(line)==0: continue
			l = line.split('->')
			text.append(l[0].strip() + '\n')
			tag.append(l[1].strip()[1:-1])
		text.append('\n')
	open('./py_scikit/tmp/testtext.txt','w').writelines(text)

#抓出Parscit的结果标签
def outputParscitResult():
	crfoutpath = './py_scikit/tmp/crfout'
	goldpath='./py_scikit/train_center/cleaned_line_cls'
	
	lines = open(crfoutpath).readlines()
	tags = []
	text1 = []
	for line in lines:
		line = line.strip()
		if len(line) == 0: continue
		if line[0] == '#': continue
		l = line.split()
		text1.append(l[0].strip().replace('|||',' '))
		tag = '<' + l[-1][:l[-1].find('/')] + '>'
		tags.append(tag)
	
	out=[]
	for file in os.listdir(goldpath):
		filepath = os.path.join(goldpath, file)
		lines = open(filepath).readlines()
		for line in lines:
			line = line.strip()
			if len(line)==0: continue
			if line[0] == '#': continue #ParsCit会自动略去#开头的行
			l = line.split('->')
			out.append([l[0].strip(), l[1].strip()])
	
	for i in range(len(out)):
		if out[i][0] != text1[i]:
			print 'NOT SAME ERROR!!'
			print out[i][0]
			print text1[i]
			print i
			return 
	
	assert(len(out) == len(tags))
	
	for i in range(len(out)):
		out[i].append(tags[i])
		out[i] = ' '.join(out[i]) + '\n'
	
	resultPath = './py_scikit/tmp/parcit-result.txt'
	open(resultPath,'w').writelines(out)
	JudgeResult.judgeAndOutputCSV(resultPath, Config.PYTMP + '/out.csv')
if __name__ == '__main__':
	#analysisSelfData()
	outputParscitResult()