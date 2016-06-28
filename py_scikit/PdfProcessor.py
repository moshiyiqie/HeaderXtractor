# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import re
sys.path.append(r'./pythonsrc')
import pickle
import GenerateCRF
import GenerateVectorMulLines_everyline
import Data
from sklearn.datasets import load_svmlight_file
import PdfMiner
import RuleEngine
import AffliManager
import StringManager
import Author
	
#获得PDF文件的头部
def getHeader(pdfpath):
	oscmd='java -jar ./py_scikit/PDFManager-openjdk.jar '+pdfpath
	pdfContent = os.popen(oscmd).readlines()
	header=[]
	lineNo=1
	for line in pdfContent:
		line = line.strip()
		line = line.replace('?','')#去掉不能识别的问号
		if len(line)==0: continue
		if lineNo>=2 and 'abstract' in line.lower(): break
		header.append(line)
		lineNo+=1
	return header
#获得PDF文件的头部、字体、大小
def getHeaderFontsSizesByPDFbox(pdfpath):
	oscmd='java -jar ./py_scikit/PDFManagerSizeFont-openjdk.jar '+pdfpath
	pdfContent = os.popen(oscmd).readlines()
	
	#open('./py_scikit/tmp/pdfContentDEBUG.txt','w').writelines(pdfContent)
	
	header=[]
	fonts = []
	sizes = []
	ypos = []
	lineNo=1
	for line in pdfContent:
		line = line.strip()
		line = line.replace('?','')#去掉不能识别的问号
		if len(line)==0: continue
		if lineNo>=2 and 'abstract' in line.lower(): break
		first = True
		content = ''
		for one in line.split():
			fontSizeWord = one.split('|||')
				
			if first:
				first = False
				fonts.append(fontSizeWord[0])
				sizes.append(float(fontSizeWord[1]))
				ypos.append(float(fontSizeWord[2]))
			content += fontSizeWord[3] + ' '
		header.append(content)
		lineNo+=1
	return header,fonts,sizes,ypos

def sortByYpos(header, fonts, sizes, ypos):
	length = len(ypos)
	for i in range(length):
		for j in range(i+1, length):
			if ypos[i] > ypos[j]:
				ypos[i], ypos[j] = ypos[j], ypos[i]
				header[i], header[j] = header[j], header[i]
				fonts[i], fonts[j] = fonts[j], fonts[i]
				sizes[i], sizes[j] = sizes[j], sizes[i]
	
#获取分类器对每行所属类别的判断-用CRF++
def getPredictLabelWithCRF(header):
	GenerateCRF.generateTestFileFromHeaderText(header)
	oscmd=Config.WORKSPACE+'/CRF++/crf_test -m ./CRF++/train/model ./CRF++/train/crf_test.txt'
	#os.popen(oscmd);
	result = os.popen(oscmd).readlines()
	label = [line.strip().split()[-1] for line in result if len(line.strip())>0]
	return label
#获取分类器对每行所属类别的判断-用Scikit
def getPredictLabelWithScikit(header):
	clfScikit = pickle.load(open(r'./RandomForestScikitModel'))
	#print 'header:',header
	headerVec = GenerateVectorMulLines_everyline.transformHeader2Vector(header[:])
	Data.transformVector2LibsvmStyle(headerVec,'./pythonsrc/tmp/tmp.svmdata')
	X, y = load_svmlight_file('./pythonsrc/tmp/tmp.svmdata')
	y_pred = clfScikit.predict(X)
	label = [ '<'+ Data.CLASSIFICATION[int(x)]+'>' for x in y_pred]
	return label


	
#获取作者、作者编号、对应的行
def getAuthors(header, label):
	authors = []
	authorsIndex = []
	authorsLine = []
	for i in range(len(header)):
		if label[i] == '<author>':
			tmpStr=[]
			originLen = len(authors)
			if StringManager.hasBigComma(header[i], tmpStr):
				authors += tmpStr[0].split('#')
			elif StringManager.hasDigit(header[i]):
				authors += re.split(r'\d(?:,\d)*', header[i])
			else:
				authors.append(header[i])
			authors = [x.strip() for x in authors if x not in ['']]
			for j in range(len(authors) - originLen):
				authorsLine.append(i)
			authorsIndex += re.findall(r'\d(?:,\d)*', header[i])
			authorsIndex = [x.strip() for x in authorsIndex if x not in ['']]
	
	assert(len(authors) == len(authorsLine))
	
	length = len(authors)
	i=0
	while i < length:
		if authors[i] == '':
			authors.pop(i)
			authorsLine.pop(i)
		i+=1
		length = len(authors)
	
	return authors, authorsIndex, authorsLine




#获得地址、地址编号、对应的行
def getAddress(header, label):
	address=[]
	addressLine = []
	for i in range(len(header)):
		if label[i] == '<address>':
			originLen = len(address)
			address.append(header[i])
			address = [x.strip() for x in address if x not in ['']]
			for j in range(len(address) - originLen):
				addressLine.append(i)
	assert(len(address) == len(addressLine))
	StringManager.clusterSameLine(address, addressLine)
	return address, addressLine
	
#处理有角标的PDF的作者-地址等匹配
def handleResultWithIndex(authors, idAuthor, authorsLine, idAffliations, emails, address, addressLine):
	authorInfo=[]
	for i in range(len(authors)):
		name = authors[i]
		if idAuthor.has_key(authors[i]): 
			affliation=''
			for idx in idAuthor[authors[i]]:
				affliation += idAffliations[idx] + ' ||| '
			affliation = affliation[:-5]
		if i < len(emails): 
			email = emails[i]
		authorInfo.append(Author.Author(name=name,affliation=affliation, email=email))
	
	updateAddress(authors, address, authorInfo, authorsLine, addressLine)
	
	return authorInfo

#处理没有角标的PDF的作者-地址等匹配
def handleResultWithoutIndex(authors, affliations, emails, authorsLine, affliationsLine, address,addressLine):
	authorInfo=[]
	for i in range(len(authors)):
		authorInfo.append(Author.Author(name = authors[i]))
	
	if len(authors) == len(affliations):#作者数目和收集到的归属数目相同
		for i in range(len(authors)):
			authorInfo[i].affliation = affliations[i]
	else:#数目不同，找离自己最近的
		for i in range(len(authors)):
			lineno = authorsLine[i]
			for j in range(len(affliations)):
				if affliationsLine[j] > lineno:
					authorInfo[i].affliation = affliations[j]
					break
	
	updateAddress(authors, address, authorInfo, authorsLine, addressLine)
	for i in range(len(emails)):
		authorInfo[i].email = emails[i]
	return authorInfo
	

#获取Email，处理了{}这种情况
def getEmails(header, label):
	emails = []
	for i in range(len(header)):
		if label[i] == '<email>':
			text = header[i].strip()
			tmp = []
			if '{' in text:
				between = False
				for ch in text:
					if ch == '{': 
						tmp.append(ch)
						between = True
					elif ch == '}':
						tmp.append(ch)
						between = False
					elif ch == ',':
						if between: tmp.append('#')
						else: tmp.append(',')
					elif between and ch == ' ':
						continue
					else: tmp.append(ch)
			elif ',' in text:
				for one in text.split(','):
					emails.append(one)
			else:
				emails.append(text)
			text = ''.join(tmp)
			text = re.sub(r' ,|, ',' ', text)
			list = text.split()
			for one in list:
				if '#' in one:
					at = one.index('@')
					line = one[:at]
					for pre in line.split('#'):
						emails.append((pre.strip() + one[at:]).strip().replace('{','').replace('}',''))
				else:
					emails.append(one.strip().replace('{','').replace('}',''))
	return emails
#处理title
def getTitle(header, label):
	title = ''
	for i in range(len(header)):
		if label[i] == '<title>':
			title += header[i].strip() + ' '
	return title.strip()
#为authorInfo更新每个作者的地址信息
def updateAddress(authors, address, authorInfo, authorsLine, addressLine):
	if len(authors) == len(address):#作者数目和收集到的归属数目相同
		for i in range(len(authors)):
			authorInfo[i].address = address[i]
	else:#数目不同，找离自己最近的
		for i in range(len(authors)):
			lineno = authorsLine[i]
			for j in range(len(address)):
				if addressLine[j] > lineno:
					authorInfo[i].address = address[j]
					break


def run(pdfpath = 'C:/ZONE/test5.pdf'):
	#获取Header
	#pdfpath = 'C:/ZONE/ceshiPDF/P15-1008.pdf'
	header, fonts, sizes, ypos = getHeaderFontsSizesByPDFbox(pdfpath)
	
	#header = getHeader(pdfpath)
	assert(len(header) == len(fonts))
	assert(len(fonts) == len(sizes))
	assert(len(sizes) == len(ypos))
	
	#根据ypos排序
	sortByYpos(header, fonts, sizes, ypos)
	
	#获取预测结果
	#label = getPredictLabelWithScikit(header)
	label = getPredictLabelWithCRF(header)
	print header
	print label
	
	#header长度和预测的每行结果的长度必须相同
	assert(len(header) == len(label))
	
	#规则修正
	label = RuleEngine.fixForSameSizeSameLabel(fonts, sizes, label)
	label = RuleEngine.fixForAt(header, label)
	
	#处理作者
	authors, authorsIndex, authorsLine = getAuthors(header, label)
	idAuthor = AffliManager.getDicForAuthor(authors, authorsIndex)
	print 'authors', authors
	
	#处理机构
	affliations, affliationsIndex, affliationsLine  = AffliManager.getAffliations(header, label)
	idAffliations = AffliManager.getDicForAffliations(affliations, affliationsIndex)
	
	#处理地址
	address, addressLine  = getAddress(header, label)
	
	#处理Email
	emails = getEmails(header, label)
	
	#处理title
	title = getTitle(header, label)
	#输出
	authorInfo = []
	if len(idAuthor) != 0:
		authorInfo = handleResultWithIndex(authors, idAuthor, authorsLine, idAffliations, emails, address, addressLine)#针对有角标的pdf输出
	else:
		authorInfo = handleResultWithoutIndex(authors, affliations, emails, authorsLine, affliationsLine, address,addressLine)#针对无角标的pdf输出
	
	return title, authorInfo, header, label
	for author in authorInfo:
		print author.toString()
	
if __name__ == '__main__':
	#vec = pickle.load(open(r'./resource/xlhh.pickle'))
	#for key in vec[0]:
	#	print key
	#print '==================================='
	run()
	
	#s = 'Huy Hoang Nhat Do1,2 Muthu Kumar Chandrasekaran2 Philip S. Cho2'
	#print re.findall(r'\d(?:,\d)*', s)
	#print re.split(r'\d(?:,\d)*', s)
	
	

	
	
	
'''
def hasBigComma(s):
	has = False
	for word in s.split():
		if word.lower()=='and':
			word = '#'
			continue
		for i in range(len(word)):
			if word[i]==',' and (i==0 or not str.isdigit(word[i-1]) ) and (i+1==len(word) or not str.isdigit(word[i+1])  ):
				word= word[:i] + '#' + word[i+1:]
				has = True
	return has

	
	
header = []
header.append('  Protocols for Collecting Responses  ')
header.append(' in Multi-hop Radio Networks   ')
header.append('  Chungki Lee James E. Burns  ')
header.append(' Mostafa H. Ammar   ')
header.append('  GIT-CC-92/28   ')
header.append('  June 1992   ')
header.append('  Abstract  ')
header.append(' The problem of collecting responses in multi-hop radio networks is considered. A given node, called the source, is to collect a specified number of  ')
header.append(' responses from nodes in a radio network. The problem arises in several  ')
header.append(' applications of distributed systems. A deterministic and a randomized protocol for the problem are presented. The two protocols are analyzed and  ')
header.append(' their performance is compared. Conclusions are drawn about the suitability  ')
header.append(' of our protocols in various network environments.   ')
header.append('  College of Computing  ')
header.append(' Georgia Institute of Technology   ')
header.append('  Atlanta, Georgia 30332-0280   ')
header.append('  +PAGE+  ')
'''