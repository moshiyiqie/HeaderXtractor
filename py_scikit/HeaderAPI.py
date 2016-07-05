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
def run(pdfpath):
	if not os.path.exists(r'./RandomForestScikitModel'):
		Classifier.outputModel()
	title, authorInfo, header , predictLabel = PdfProcessor.run(pdfpath)
	dicSet = []
	print '[Title]:' + title
	print ''
	for author in authorInfo:
		print author.toString()
		dicSet.append(author.toDic())
	return title, dicSet, header, predictLabel

if __name__ == '__main__':
	#path = './test.pdf'
	path = 'C:/ZONE/ceshiPDF2/P15-1038.pdf'
	title, dicSet, header, predictLabel=run(path)
	#print header
	#print predictLabel