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
import StringManager
import Author
import AddressManager
import AttributeWithIndex
import Pdf
import EmailManager
import BlockManager
import Tools
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
	
#处理有角标的PDF的作者-地址等匹配
def handleResultWithIndex(authors, idAuthor, idAffliations, idAddress,  emails, affiEmailMap):
	qMap = {}
	if len(affiEmailMap)!=0:
		for idtf in idAffliations.keys():
			qMap[idtf] = affiEmailMap[idtf]
	
	authorInfo=[]
	email=''
	for i in range(len(authors)):
		name = authors[i]
		affliation = AttributeWithIndex.matchAuthorAttributes(authors[i], idAuthor, idAffliations)
		addr = AttributeWithIndex.matchAuthorAttributes(authors[i], idAuthor, idAddress)
		if len(emails) !=0:
			if i < len(emails): 
				email = emails[i]
		elif len(affiEmailMap)!=0:
			idtf = idAuthor[name][0]
			email = ''
			if len(qMap[idtf])!=0:
				email = qMap[idtf][0]
				qMap[idtf].pop(0)
		authorInfo.append(Author.Author(name=name,affliation=affliation, email=email, address = addr))
	#AddressManager.updateAddress(authors, address, authorInfo, authorsLine, addressLine)
	
	return authorInfo

#处理没有角标的PDF的作者-地址等匹配
#!!!已被BlockManager.matchInBlocks()代替
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
	
	AddressManager.updateAddress(authors, address, authorInfo, authorsLine, addressLine)
	for i in range(min(len(authorInfo),len(emails))):
		authorInfo[i].email = emails[i]
	return authorInfo
	


#处理title
def getTitle(header, label):
	title = ''
	for i in range(len(header)):
		if label[i] == '<title>':
			title += header[i].strip() + ' '
	return title.strip()



def run(pdfpath = 'C:/ZONE/test5.pdf'):
	#获取Header
	#pdfpath = 'C:/ZONE/ceshiPDF/P15-1008.pdf'
	pdf = Pdf.Pdf()
	pdf.loadPdfByPDFbox(pdfpath)
	
	##根据排序,包含分列
	#pdf.sortByYpos()
	header, fonts, sizes, ypos, xpos, charSizes = pdf.header, pdf.fonts, pdf.sizes, pdf.ypos, pdf.xpos, pdf.charSizes
	sortedIdxList = BlockManager.BlockUnionProcess(header, charSizes, ypos, xpos)
	header = Tools.reArrangeByIdxList(header, sortedIdxList)
	fonts = Tools.reArrangeByIdxList(fonts, sortedIdxList)
	sizes = Tools.reArrangeByIdxList(sizes, sortedIdxList)
	ypos = Tools.reArrangeByIdxList(ypos, sortedIdxList)
	xpos = Tools.reArrangeByIdxList(xpos, sortedIdxList)
	charSizes = Tools.reArrangeByIdxList(charSizes, sortedIdxList)
	
	
	#获取预测结果
	#label = getPredictLabelWithScikit(header)
	label = getPredictLabelWithCRF(header)
	print '[Before Rule]',zip(header, label)
	
	#header长度和预测的每行结果的长度必须相同
	assert(len(header) == len(label))
	
	#规则修正
	label = RuleEngine.fixForAt(header, label)
	label = RuleEngine.fixByStanfordNER(header, label)#利用stanford ner来进行机构、地址、作者的修正
	label = RuleEngine.fixForContainUniversity(header, label)
	label = RuleEngine.fixForCheckIfNoAuthor(header, label)
	label = RuleEngine.fixForCheckIfNoTitle(header, label)
	label = RuleEngine.fixForNoteAfterTitle(header, label)
	label = RuleEngine.fixForDistantTitle(label)
	label = RuleEngine.fixForSameSizeSameLabel(header, fonts, sizes, label)
	
	
	
	print '[After Rule]',zip(header, label)
	
	#处理作者
	authors, authorsIndex, authorsLine = Author.getAuthors(header, label, xpos, pdf)
	idAuthor = Author.getDicForAuthor(authors, authorsIndex)
	#print 'authors,idAuthor', authors,idAuthor
	
	#处理机构
	affliations, affliationsIndex, affliationsLine  = AttributeWithIndex.getAttributes(header, label, 'affiliation', pdf)
	idAffliations = AttributeWithIndex.getDicForAttributes(affliations, affliationsIndex)
	#print 'affliations, affliationsIndex', affliations, affliationsIndex
	#print 'affliations, idAffliations', affliations, idAffliations
	
	#处理地址
	address, addressIndex, addressLine  = AttributeWithIndex.getAttributes(header, label, 'address', pdf)
	idAddress = AttributeWithIndex.getDicForAttributes(address, addressIndex)
	
	#处理Email
	affiEmailMap = {}
	emails = EmailManager.getEmails(header, label,affliationsIndex, affiEmailMap, pdf)
	
	#处理title
	title = getTitle(header, label)
	
	#输出
	authorInfo = []
	if len(idAuthor) != 0:
		authorInfo = handleResultWithIndex(authors, idAuthor, idAffliations, idAddress,  emails, affiEmailMap)#针对有角标的pdf输出
	else:
		#authorInfo = handleResultWithoutIndex(authors, affliations, emails, authorsLine, affliationsLine, address,addressLine)#针对无角标的pdf输出
		authorInfo = BlockManager.matchInBlocks(label)
	
	return title, authorInfo, header, label
	#for author in authorInfo:
	#	print author.toString()
	
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