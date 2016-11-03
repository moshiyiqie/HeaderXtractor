# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
sys.path.append(r'./py_scikit')
import re
import Pdf

#将cora.tagged文件转为NER格式的数据
def transform2NERformat(inpath, outpath):
	fout = open(outpath,'w')
	for line in open(inpath).readlines():
		curLabel = ''
		for word in line.split():
			if len(re.findall(r'</?\w*>',word)) > 0:
				curLabel = word
				continue
			fout.write(word.strip() + ' ' + curLabel + '\n')
		fout.write('\n')
	fout.close()

#将 acmpaper 抽取出 reference文本
def transForm_paper2referenceText(pdfFolder, outPath):
	pdf = Pdf.Pdf()
	fout = open(outPath,'w')
	fout.close()
	with open(outPath,'a') as fout:
		cnt = 0
		for file in os.listdir(pdfFolder):
			if cnt % 10 == 0:
				print 'Processing %d th paper...'%(cnt)
			cnt += 1
			
			wholePath = os.path.join(pdfFolder, file)
			pdfContentList = pdf.getPdfTextContent(wholePath)
			pos = -1
			for i in range(len(pdfContentList)-1, -1,-1):
				if 'reference' in pdfContentList[i].lower():
					pos = i
					break
			
			if pos == -1: continue
			else:
				refList = pdfContentList[pos+1:]
				refList = [x for x in refList if not (x.strip().isdigit())]
				fout.writelines(refList)
			

#将 reference文本 送到parscit标注，获得 引用标注结果

#将 引用标注结果 转为rnn训练数据
def transformParscit_out2rnn_train_File(inpath, outpath):
	lines = open(inpath).readlines()
	out = []
	for line in lines:
		if line.strip() == '':
			out.append('\n')
		else:
			line = line.split()
			out.append(line[0] + '\t' +'<%s>'%(line[-1]) + '\n' )
	open(outpath,'w').writelines(out)
	
#用 rnn训练数据 训练RNN模型，cora数据评测RNN模型



if __name__ == '__main__':	
	#transform2NERformat('./CitXtractor/tagged_data/cora.tagged.txt', './CitXtractor/train_data/cora.train')
	#transForm_paper2referenceText('D:/acm_paper/10000paper-05-17', 'D:/10000papers_cit.txt')
	#transformParscit_out2rnn_train_File('D:/in.txt','D:/out2.txt')