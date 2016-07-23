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
	open(toPath+'/'+os.path.split(pdfpath)[1], 'w').writelines(output)
	return title, dicSet, header, predictLabel

if __name__ == '__main__':
	path = 'D:/acm_paper/TAO-TEST/2_p106-vogelaere.pdf.pdf'
	#path = 'C:/ZONE/ceshiPDF2/P15-1021.pdf'
	title, dicSet, header, predictLabel=run(path, 'D:/acm_paper/TAO-TEST-HEAD')
	#for file in os.listdir('D:/acm_paper/TAO-TEST'):
	#	path = 'D:/acm_paper/TAO-TEST/'+file
	#	title, dicSet, header, predictLabel=run(path, 'D:/acm_paper/TAO-TEST-HEAD')