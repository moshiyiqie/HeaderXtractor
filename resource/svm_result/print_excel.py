# -*- coding: utf-8 -*- 
from __future__ import print_function
import os
path = r'C:/Users/rainto96/workspace/HeaderXtractor/resource/svm_result'
for file in os.listdir(path):
	if not file.endswith('.txt'): continue
	s = open(path + '/' + file).readlines()
	s = [x.strip() for x in s]
	print(file.replace('.txt_svm.txt',''),s[0],s[1],s[2],s[6], end='')
	print('\n')