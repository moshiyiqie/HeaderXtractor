# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import PdfProcessor
import Classifier

#输入pdfpath 代表pdf文件路径（使用绝对路径）
#函数返回四个变量
#	title:文章标题
#	dicSet:包含作者信息的字典列表
#	header:PDF中抽取的头部部分原文
#	predictLabel:header对应的每行的算法预测的类别
def run(pdfpath, toPath):
	if not os.path.exists(r'./RandomForestScikitModel'):
		Classifier.outputModel()
	title, authorInfo, header , predictLabel = PdfProcessor.run(pdfpath)
	dicSet = []
	output = ''
	output += '[Title]:' + title + '\n\n'
	for author in authorInfo:
		output += author.toString() + '\n'
		dicSet.append(author.toDic())
	print output
	open(toPath+'/'+os.path.split(pdfpath)[1].replace('.pdf','.txt'), 'w').writelines(output)
	return title, dicSet, header, predictLabel
'''
if __name__ == '__main__':
	srcPath = sys.argv[1]
	resultFolderPath = sys.argv[2]
	#print 'sys.argv', sys.argv
	title, dicSet, header, predictLabel=run(srcPath, resultFolderPath)
	
'''
if __name__ == '__main__':
	#path = 'D:/acm_paper/TAO-TEST/3.pdf'
	#title, dicSet, header, predictLabel=run(path, 'D:/acm_paper/TAO-TEST-HEAD')
	
	path = 'D:/acm_paper/TAO-TEST/54.pdf'
	print '================'+os.path.split(path)[1]+'================='
	title, dicSet, header, predictLabel=run(path, 'D:/acm_paper/TAO-TEST-HEAD')

	#
	#for file in os.listdir('D:/acm_paper/TAO-TEST'):
	#	path = 'D:/acm_paper/TAO-TEST/'+file
	#	try:
	#		title, dicSet, header, predictLabel=run(path, 'D:/acm_paper/TAO-TEST-HEAD')
	#	except Exception,e:
	#		print '[Error]: File ',file
	#		continue
	#
