# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import PdfProcessor

###该类主要用于将抽取成功的样例pdf变为训练集不断地循环训练，负责改进分类器
def getPDFLineClassificationResult(pdfFolder, resultFolder):
	for file in os.listdir(pdfFolder):
		try:
			#if file != '165.pdf' and file != '167.pdf': continue
			print 'File:',file,'===================================='
			filepath = os.path.join(pdfFolder, file)
			header, fonts, sizes, ypos, xpos, charSizes, pdf, label = PdfProcessor.preProcedure(filepath)
			outputstr=['->'.join(x) + '\n' for x in zip(header, label)]
			open(os.path.join(resultFolder, file.replace('.pdf','.txt')), 'w').writelines(outputstr)
		except:
			print 'error'

if __name__ == '__main__':
	getPDFLineClassificationResult('D:/acm_paper/TAO-TEST', './py_scikit/train_center/line_cls_result/')
