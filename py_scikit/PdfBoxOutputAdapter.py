# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
#��pdfbox���������б�ʾ��Ϊ�ʱ�ʾ
#��һ�еĸ��ı���Ϣת��Ϊ�Դ�Ϊ��λ�ĸ��ı���Ϣ
def manageLine(line):
	nline = line.split('|||')
	#print 'nline', nline
	content = nline[4]
	if content.strip() == '':
		return ''
	chSizes = [x for x in nline[6].split(',') if x != '']
	chXpos = [x for x in nline[7].split(',') if x != '']
	if len(content) > len(chSizes) or len(content) > len(chXpos): return ''
	
	while len(content) < len(chSizes): chSizes.pop()
	while len(content) < len(chXpos): chXpos.pop()
	
	que=[]
	
	chque=[]
	szque=[]
	xposque=[]
	for i in range(len(content)):
		if content[i] != ' ':
			chque.append(content[i])
			szque.append(chSizes[i])
			xposque.append(chXpos[i])
		else:
			if len(xposque) > 0:
				block4 = ''.join(chque)
				block6 = ','.join(szque)
				que.append('|||'.join(nline[0:3] + [xposque[0], block4, xposque[-1], block6] ) )
			chque=[]
			szque=[]
			xposque=[]
	if len(chque) != 0:
		assert(len(chque) == len(szque) and len(szque) == len(xposque) )
		block4 = ''.join(chque)
		block6 = ','.join(szque)
		que.append('|||'.join(nline[0:3] + [xposque[0], block4, xposque[-1], block6] ) )
		chque=[]
		szque=[]
		xposque=[]
	return ' '.join(que)

#��һ�еĸ��ı���Ϣת��Ϊ�Դ�Ϊ��λ�ĸ��ı���Ϣ
def adapt2WordExpression(pdfcontent):
	#û�пո����������
	hasSpace = False
	for line in pdfcontent:
		line = line.strip()
		if not '|||' in line:
			continue
		if ' ' in line.split('|||')[4]:
			hasSpace = True
			break
	if hasSpace == False:
		return pdfcontent
	
	#�������ݺ��ո��������൱�ڷִ�
	nContent=[]
	for line in pdfcontent:
		line = line.strip()
		if not '|||' in line:
			continue
		nline = manageLine(line)
		#print '[nline]', nline
		if nline != '': 
			nContent.append(nline + '\n')
	return nContent

if __name__ == '__main__':
	pdfcontent = open('./py_scikit/tmp/pdfContentDEBUG.txt').readlines()
	open('./py_scikit/tmp/outputadapt.txt','w').writelines(adapt2WordExpression(pdfcontent))