# -*- coding: utf-8 -*- 
from __future__ import print_function
import os
import Config
os.chdir(Config.WORKSPACE)
def showExcel():
	excelpath = r'./pythonsrc/tmp/excel.csv'
	path = r'./resource/j48_result'
	#path = r'./resource/MulLine_svm_result'
	#fout = open(excelpath,'w')
	
	fout = open(excelpath,'w')
	fout.write('类别,准确率,召回率,F值,样本数目\n'.decode('utf-8').encode('gbk'))
	for file in os.listdir(path):
		if not file.endswith('.txt'): continue
		s = open(path + '/' + file).readlines()
		s = [x.strip() for x in s]
		st=','.join([file[:file.find(".")],s[0],s[1],s[2],s[6]])
		fout.write(st+'\n')
	fout.close()
	os.system(Config.WORKSPACE+excelpath)
if __name__ == '__main__':
	showExcel()