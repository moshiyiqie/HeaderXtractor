# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import PdfProcessor
sys.path.append(r'./pythonsrc')
import GenerateCRF
import codecs
import pickle
import Tools
###该类主要用于将抽取成功的样例pdf变为训练集不断地循环训练，负责改进分类器
def getPDFLineClassificationResult(pdfFolder, resultFolder):
	for file in os.listdir(pdfFolder):
		try:
			#if int(file[:file.find('.')])<=400:
			#	continue
			#if file != '165.pdf' and file != '167.pdf': continue
			print 'File:',file,'===================================='
			filepath = os.path.join(pdfFolder, file)
			outputPath = os.path.join(resultFolder, file.replace('.pdf','.txt'))
			if os.path.exists(outputPath):
				print 'File [%s] exists!'%(outputPath)
				continue
			header, fonts, sizes, ypos, xpos, charSizes, pdf, label = PdfProcessor.preProcedure(filepath)
			outputstr=['->'.join(x) + '\n' for x in zip(header, label)]
			open(outputPath, 'w').writelines(outputstr)
		except:
			print 'error'
###从标注的文件夹中获得每行header的label
def getLabelFromGoldFolder(header, goldfilepath):
	header2tag={}
	lines = open(goldfilepath).readlines()
	if len(lines)>0 and lines[0][:3] == codecs.BOM_UTF8:
		lines[0] = lines[0][3:]
	for line in lines:
		if len(line.strip())==0:
			continue
		ht = line.strip().split('->')
		if len(ht) < 2:
			print '[Cant Split -> Error]:', line
			return [], False
		header2tag[ht[0].strip()] = ht[1]
	label = []
	for i in range(len(header)):
		hd = header[i].strip()
		if not header2tag.has_key(hd):
			print '[No Tag Error]:', hd
			return [], False
		label.append(header2tag[hd])
	return label,True

###训练带富文本信息特征的行分类模型
def getModelForRichTextFeatureFolder(pdfFolder='D:/acm_paper/TAO-TEST', goldFolder='./py_scikit/train_center/cleaned_line_cls'):
	data = []
	number = 0
	for file in os.listdir(goldFolder):
		#if file != '562.txt' and file != '563.txt':
		#	continue
		print 'Generate ' + str(number) + ' files... filename: '+ file
		pdfpath = os.path.join(pdfFolder, file.replace('.txt','.pdf'))
		goldfilepath = os.path.join(goldFolder, file)
		header, fonts, sizes, ypos, xpos, charSizes, pdf = PdfProcessor.preProcedure(pdfpath, False)
		label,success = getLabelFromGoldFolder(header, goldfilepath)
		if success == False:
			print '[Tag False!]'
			continue
		data.append(file + GenerateCRF.generateCrfFileFromHeaderTextWithRichInfo(header, fonts, sizes, label, ypos))
		number += 1
		

	limit = int(len(data)*0.7)
	open('./py_scikit/tmp/ntrain-ok.txt','w').writelines('\n'.join(data[:limit]))
	open('./py_scikit/tmp/ntest-ok.txt','w').writelines('\n'.join(data[limit:]))

###选择一些特征，将其他未选择特征变为<other>
def pickFeatures(frompath, outpath):
	picked= ['<author>', '<title>', '<address>', '<email>', '<affiliation>']
	lines = open(frompath).readlines()
	result = []
	for line in lines:
		line = line.strip()
		if len(line) == 0:
			result.append('\n')
			continue
		line = line.split()
		tag = line[-1]
		if '<' in tag and '>' in tag:
			if not tag in picked:
				line[-1] = '<other>'
		else:
			print 'FAIL! Not A Tag!'
		result.append(' '.join(line) + '\n')
	open(outpath, 'w').writelines(result)

#对标注的数据抽取高频词
def extractHighFreqWord(goldFolder='./py_scikit/train_center/cleaned_line_cls'):
	cls = ['<author>', '<affiliation>', '<address>']
	wordFreq={}
	for file in os.listdir(goldFolder):
		goldfilepath = os.path.join(goldFolder, file)
		lines = open(goldfilepath).readlines()
		for line in lines:
			line = line.strip()
			if len(line) == 0:
				continue
			if any([x in line for x in cls]):
				text = line.split('->')[0].split()
				for word in text:
					if len(word)<=1: continue
					if not wordFreq.has_key(word):
						wordFreq[word]=0
					wordFreq[word]+=1
	wordList = []
	for word in wordFreq.keys():
		wordList.append([word, wordFreq[word]])
	wordList.sort(key = lambda x:x[1], reverse = True)
	wordList = [x[0]+' ::: '+str(x[1]) + '\n' for x in wordList]
	open('./py_scikit/tmp/wordfreq.txt','w').writelines(wordList)

#查看误将cls1分类到cls2的文件名
def lookWrongClassify(cls1, cls2,path = 'D:/CRF++/train/nmodel/result.txt'):
	lines = open(path).readlines()
	for line in lines:
		if len(line.strip()) == 0: continue
		if '.txt' in line[:8]:
			cur = line[:line.find('.txt')]
		l = line.split()
		origin = l[-2]
		judge = l[-1]
		if cls1 in origin and cls2 in judge:
			print 'Error in ', cur
			#print line[-50:]

#将tagged_headers_everyline分为训练集和测试集-针对tensorflow训练
def splitTrainSet():
	path = './resource/tagged_headers_everyline.txt'
	lines = open(path).readlines()
	nl = []
	tmp = []
	for line in lines:
		if line.strip().endswith('::line_number::0'):
			tmp.append('\n')
			nl.append(tmp)
			tmp = [line]
		else:
			tmp.append(line)
	if len(tmp)>0:
		tmp.append('\n')
		nl.append(tmp)

	print 'len(nl) = ',len(nl)
	open('./py_scikit/tmp/train.in','w').writelines(Tools.flatList(nl[:600]))
	open('./py_scikit/tmp/testa.in','w').writelines(Tools.flatList(nl[600:750]))
	open('./py_scikit/tmp/testb.in','w').writelines(Tools.flatList(nl[750:]))

if __name__ == '__main__':
	#getPDFLineClassificationResult('D:/acm_paper/TAO-TEST', './py_scikit/train_center/line_cls_result/')
	getPDFLineClassificationResult('D:/acm_paper/10000paper-05-17', './py_scikit/train_center/10000paper-05-17/')
	getPDFLineClassificationResult('D:/acm_paper/10000paper-99-04', './py_scikit/train_center/10000paper-99-04/')
	
	#getModelForRichTextFeatureFolder()
	#pickFeatures('./CRF++/train/nmodel/ntest.txt','./CRF++/train/nmodel/ntest2.txt')
	#extractHighFreqWord()
	#pickFeatures('D:/CRF++/ntest-ok.txt', 'D:/CRF++/ntest-ok-o.txt')
	#lookWrongClassify('address','author','D:/CRF++/result.txt')
	
	#getModelForRichTextFeatureFolder()
	
	#splitTrainSet()