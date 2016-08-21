# -*- coding: utf-8 -*- 
import os
import Config
os.chdir(Config.WORKSPACE)
import sys
sys.path.append(r'./py_scikit')
import HeaderAPI

def callExtractTool(toolPath, src, distFolder):
	cmd = 'python '+ toolPath + ' ' + src + ' ' + distFolder
	print cmd
	os.system(cmd)

#给出pdf文件夹路径和对应答案文件夹路径，以及要抽取的pdf标号列表，增加抽取正确的文件到指定文件夹
def addCorrectInstance(pdfFolder, goldFolder, fileList):
	for file in fileList:
		filename = file.strip()
		if not filename.endswith('.pdf'):
			filename += '.pdf'
		filePath = os.path.join(pdfFolder, filename)
		print filePath
		#HeaderAPI.run(filePath, goldFolder)
		callExtractTool('./py_scikit/HeaderAPI.py', filePath, goldFolder)

#给出pdf文件夹路径和对应的答案文件夹路径，输出抽取效果
def checkExtractStatus(pdfFolder, goldFolder):
	fileNum = len(os.listdir(goldFolder))
	correctNum = 0
	errorList = []
	for file in os.listdir(goldFolder):
		pdfFile = file.replace('.txt', '.pdf')
		pdfFilePath = os.path.join(pdfFolder, pdfFile)
		#HeaderAPI.run(pdfFilePath, './py_scikit/tmp/extract_result')
		callExtractTool('./py_scikit/HeaderAPI.py', pdfFilePath, './py_scikit/tmp/extract_result')
		outputContent = open('./py_scikit/tmp/extract_result/' + file).readlines()
		goldContent = open(os.path.join(goldFolder, file)).readlines()
		if goldContent == outputContent:
			correctNum += 1
		else:
			errorList.append([pdfFile, outputContent])
	print 'Correct: ', correctNum, '/', fileNum, ' -> ', correctNum*1.0/fileNum
	print '======================================================='
	print 'Error:'
	print errorList
	
if __name__ == '__main__':
	list = [x for x in open('./AutoCheck/right_pdf_id.txt').readlines()][10:]
	addCorrectInstance('D:/acm_paper/TAO-TEST/','./AutoCheck/gold',list)