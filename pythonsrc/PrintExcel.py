# -*- coding: utf-8 -*- 
from __future__ import print_function
import os
def showExcel():
	#path = r'C:/Users/rainto96/workspace/HeaderXtractor/resource/svm_result'
	#fout = open(r'C:/Users/rainto96/workspace/HeaderXtractor/resource/svm_result/excel.csv','w')
	excelpath = r'C:/Users/rainto96/workspace/HeaderXtractor/pythonsrc/tmp/excel.csv'
	path = r'C:/Users/rainto96/workspace/HeaderXtractor/resource/MulLine_svm_result'
	fout = open(excelpath,'w')
	fout.write('类别,准确率,召回率,F值,样本数目\n'.decode('utf-8').encode('gbk'))
	for file in os.listdir(path):
		if not file.endswith('.txt'): continue
		s = open(path + '/' + file).readlines()
		s = [x.strip() for x in s]
		st=','.join([file.replace('.txt_svm.txt',''),s[0],s[1],s[2],s[6]])
		fout.write(st+'\n')
	fout.close()
	os.system(excelpath)
if __name__ == '__main__':
	showExcel()