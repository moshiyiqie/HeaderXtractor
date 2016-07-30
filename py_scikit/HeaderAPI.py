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

if __name__ == '__main__':
	#path = 'D:/acm_paper/TAO-TEST/3.pdf'
	#title, dicSet, header, predictLabel=run(path, 'D:/acm_paper/TAO-TEST-HEAD')
	
	path = 'D:/acm_paper/TAO-TEST-1/14.pdf'
	print '================'+os.path.split(path)[1]+'================='
	title, dicSet, header, predictLabel=run(path, 'D:/acm_paper/TAO-TEST-HEAD')
	'''
	for file in os.listdir('D:/acm_paper/TAO-TEST'):
		path = 'D:/acm_paper/TAO-TEST/'+file
		try:
			title, dicSet, header, predictLabel=run(path, 'D:/acm_paper/TAO-TEST-HEAD')
		except Exception,e:
			print '[Error]: File ',file
			continue
	'''