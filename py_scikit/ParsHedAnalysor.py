# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import JudgeResult
#

#
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

#
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
			if line[0] == '#': continue #ParsCit»á×Ô¶¯ÂÔÈ¥#¿ªÍ·µÄÐÐ
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

#
#
#
#
def transformCrfFileFromParscit(crfFilePath, tagsFilePath, outputPath = './py_scikit/tmp/transformed.txt'):
	tags = open(tagsFilePath).readlines()
	tmp = []
	for i in range(len(tags)):
		x = tags[i]
		if len(x.strip())!=0: 
			x = [x.split()[0].strip(), x.split()[-1].strip()]
			x = ['|||'.join(x[0].replace('|||',' ').split()), x[1]]
			tags[i] = x
		else: tags[i] = ['','']
	


	crfFile = open(crfFilePath).readlines()
	tl = 0
	outputCrf = []
	for line in tags:
		if len(line[0].strip())==0:
			outputCrf.append('\n')
		else:
			if tl == len(crfFile):
				print 'Error: size not same!'
			curtxt = crfFile[tl].split()[0].strip()
			curtxt = '|||'.join(curtxt.replace('|||',' ').split())
			if line[0] != curtxt:
				print line[0]
				print crfFile[tl].split()[0].strip()
				print 'Error: not same!'
			outputCrf.append('\t'.join(crfFile[tl].split()[:-1]) + '\t' + line[1] + '\n')
			tl+=1
	open(outputPath,'w').writelines(outputCrf)
	#print tl
	#print len(crfFile)
	#assert(tl == len(crfFile))

if __name__ == '__main__':
	#analysisSelfData()
	#outputParscitResult()
	
	#transformCrfFileFromParscit('./py_scikit/tmp/ParsHed-test/crf_train_text_crftype',
	#	'./py_scikit/tmp/ParsHed-test/crf_train-pub.txt')