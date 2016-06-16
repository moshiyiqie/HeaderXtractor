# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import PdfProcessor
import Classifier

#����pdfpath ����pdf�ļ�·����ʹ�þ���·����
#���������ĸ�����
#	title:���±���
#	dicSet:����������Ϣ���ֵ��б�
#	header:PDF�г�ȡ��ͷ������ԭ��
#	predictLabel:header��Ӧ��ÿ�е��㷨Ԥ������
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
	run('./test.pdf')