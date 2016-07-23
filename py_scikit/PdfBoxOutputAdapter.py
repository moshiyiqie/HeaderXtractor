# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
#将pdfbox输出结果从行表示换为词表示
#将一行的富文本信息转换为以词为单位的富文本信息
def manageLine(line):
	nline = line.split('|||')
	content = nline[4]
	chSizes = [x for x in nline[6].split(',') if x != '']
	chXpos = [x for x in nline[7].split(',') if x != '']
	#print 'len(content)',len(content)
	#print 'len(chSizes)',len(chSizes)
	#print 'len(chXpos)',len(chXpos)
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
			#print 'here!!!'
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

#将一行的富文本信息转换为以词为单位的富文本信息
def adapt2WordExpression(pdfcontent):
	#没有空格情况不处理
	hasSpace = False
	for line in pdfcontent:
		line = line.strip()
		if ' ' in line.split('|||')[4]:
			hasSpace = True
			break
	if hasSpace == False:
		return pdfcontent
	
	#处理内容含空格的情况，相当于分词
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