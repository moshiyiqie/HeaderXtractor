# -*- coding: utf-8 -*- 
import os
import Config
import sys
import PdfProcessor
os.chdir(Config.WORKSPACE)

#将嵌套的列表变为一维列表
def __flatList(nested_list, to):
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            for sub_item in flatList(item):
                to.append(sub_item)
        else:
            to.append(item)
def flatList(nested_list):
	to = []
	__flatList(nested_list,to)
	return to

def reArrangeByIdxList(olist, sortedIdxList):
	nlist = []
	for idx in sortedIdxList:
		nlist.append(olist[idx])
	return nlist

def mergeAllTextBelowOneFolder(folderPath,outputPath):
	output=[]
	for file in os.listdir(folderPath):
		lines = open(os.path.join(folderPath, file)).readlines()
		output += lines
		output.append('\n')
	open(outputPath,'w').writelines(output)

if __name__ == '__main__':
	mergeAllTextBelowOneFolder('./py_scikit/train_center/cleaned_line_cls','./py_scikit/train_center/cleaned_lines.txt')


