# -*- coding: utf-8 -*- 
import os
import Config
import sys
import StringManager
import re
import Author
import PdfBoxOutputAdapter
os.chdir(Config.WORKSPACE)
import Tools
import copy
def uni(s):
		return unicode(s,'utf-8')
def utf8(s):
	return s.encode('utf-8')
	
class Pdf:
	header=[]
	fonts=[]
	sizes=[]
	ypos=[]
	xpos=[]
	charSizes=[]
	def __init__(self):
		self.header=[]
		self.fonts=[]
		self.sizes=[]
		self.ypos=[]
		self.xpos=[]
		self.charSizes=[]
	#获得PDF文件的头部、字体、大小
	def loadPdfByPDFbox(self,pdfpath):
		pdfboxOutputPath = './py_scikit/tmp/pdfboxResult.txt'
		oscmd='java -Dfile.encoding=utf-8 -jar ./py_scikit/PDFManagerSizeFont-openjdk.jar ' + pdfpath + ' ' + pdfboxOutputPath
		os.system(oscmd)
		#pdfContent = os.popen(oscmd).readlines()
		pdfContent = open(pdfboxOutputPath).readlines()
		open('./py_scikit/tmp/pdfContentDEBUGbeforeAdapter.txt','w').writelines(pdfContent)
		pdfContent = PdfBoxOutputAdapter.adapt2WordExpression(pdfContent)
		open('./py_scikit/tmp/pdfContentDEBUG.txt','w').writelines(pdfContent)
		lineNo=1
		
		#====================pdfContent 格式====================
		#fonts sizes ypos xpos content xpos charSizes	charXpos
		#0	   1 	 2 	  3    4       5    6			7
		for line in pdfContent:
			#print 'line:', line
			line = line.strip()
			line = line.replace('*','')#去掉*号，不认为*号是角标
			if len(line)==0: continue
			if (lineNo>=2 and ('abstract' in line.lower() or 'introduction' in line.lower())) or lineNo>=35: break
			first = True
			content = ''
			
			for one in line.split():
				#print 'one',one
				fontSizeWord = one.split('|||')
				#print 'fontSizeWord',fontSizeWord
					
				if first:
					first = False
					self.fonts.append(fontSizeWord[0])
					self.sizes.append(float(fontSizeWord[1]))
					self.ypos.append(float(fontSizeWord[2]))
					self.xpos.append([])
					self.charSizes.append([])
				self.xpos[-1].append([float(fontSizeWord[3]), float(fontSizeWord[5])])
				self.charSizes[-1].append([float(x) for x in fontSizeWord[6].split(',') if x != ''])
				content += fontSizeWord[4] + ' '
			self.header.append(content)
			lineNo+=1
		assert(len(self.header) == len(self.fonts))
		assert(len(self.fonts) == len(self.sizes))
		assert(len(self.sizes) == len(self.ypos))
	
	def swapAllDataIJ(self,i, j):
		self.ypos[i], self.ypos[j] = self.ypos[j], self.ypos[i]
		self.header[i], self.header[j] = self.header[j], self.header[i]
		self.fonts[i], self.fonts[j] = self.fonts[j], self.fonts[i]
		self.sizes[i], self.sizes[j] = self.sizes[j], self.sizes[i]
		self.xpos[i], self.xpos[j] = self.xpos[j], self.xpos[i]
		self.charSizes[i], self.charSizes[j] = self.charSizes[j], self.charSizes[i]
	
	#根据每一行的y坐标进行排序
	def sortByYpos(self):
		LINE_BETWEEN = 5.0 #行间距
		
		length = len(self.ypos)
		for i in range(length):
			for j in range(i+1, length):
				if self.ypos[i] - LINE_BETWEEN >= self.ypos[j]:
					self.swapAllDataIJ(i,j)
				elif abs(self.ypos[i] - self.ypos[j]) <= LINE_BETWEEN:
					if self.xpos[i] > self.xpos[j]:
						self.swapAllDataIJ(i,j)
		
		#print 'YPOS::', self.ypos
		#print 'Header::', self.header
		lineVec=[[0]]
		for i in range(1, length):
			if abs(self.ypos[i] - self.ypos[i-1]) < LINE_BETWEEN:
				lineVec[-1].append(i)
				j = len(lineVec[-1]) - 1
				while j >=1 and self.xpos[lineVec[-1][j]][0] < self.xpos[lineVec[-1][j-1]][0]:
					lineVec[-1][j], lineVec[-1][j-1] = lineVec[-1][j-1], lineVec[-1][j]
					j -= 1
			else:
				lineVec.append([i])
		#print 'lineVec::',lineVec
		verVec = []
		for i in range(len(lineVec)):
			for j in range(len(lineVec[i])):
				if len(verVec) - 1 < j:
					verVec.append([lineVec[i][j]])
				else: 
					verVec[j].append(lineVec[i][j])
		#print 'verVec::', verVec
		#将数组变为排出的顺序
		finalSeq = []
		for col in verVec:
			for No in col:
				finalSeq.append(No)
		
		header=copy.deepcopy(self.header)
		fonts=copy.deepcopy(self.fonts)
		sizes=copy.deepcopy(self.sizes)
		ypos=copy.deepcopy(self.ypos)
		xpos=copy.deepcopy(self.xpos)
		charSizes=copy.deepcopy(self.charSizes)
		
		i=0
		for No in finalSeq:
			header[i] = self.header[No]
			fonts[i] = self.fonts[No]
			sizes[i] = self.sizes[No]
			ypos[i] = self.ypos[No]
			xpos[i] = self.xpos[No]
			charSizes[i] = self.charSizes[No]
			i+=1
		
		
		self.header=header
		self.fonts=fonts
		self.sizes=sizes
		self.ypos=ypos
		self.xpos=xpos
		self.charSizes=charSizes
		
		
	#得到lineNo行的平均字体大小
	def getAverageCharSizeForLine(self,lineNo):
		i = lineNo
		averageCharSize = 0.0
		charNum = 0
		for word in self.charSizes[lineNo]:
			for sz in word:
				#print self.header[lineNo]
				#print 'sz',sz
				averageCharSize += sz
				charNum += 1
		averageCharSize /= charNum
		return averageCharSize
		
	#是否含有角标
	def hasIndex(self, lineNo):
		#print self.header[lineNo]
		lineCharSizes = self.charSizes[lineNo]
		averageCharSize = self.getAverageCharSizeForLine(lineNo)
		wordList = uni(self.header[lineNo]).strip().split()
		assert(len(wordList) == len(lineCharSizes))
		for i in range(len(wordList)):
			if len(wordList[i]) != len(lineCharSizes[i]):
				open('./py_scikit/tmp/debug.txt','w').writelines(' '.join(['wordList[i], lineCharSizes[i]', str(len(wordList[i])), str(len(lineCharSizes[i])), utf8(wordList[i])]))
			#print 'wordList[i]', wordList[i]
			#print 'list(wordList[i])', list(wordList[i])
			#print 'lineCharSizes[i]', lineCharSizes[i]

			#assert(len(list(wordList[i])) == len(lineCharSizes[i]))
			while len(lineCharSizes[i]) < len(list(wordList[i])):#对assert的修补
				lineCharSizes[i].append(lineCharSizes[-1])#对assert的修补


			for j in range(len(wordList[i])):
				if lineCharSizes[i][j] < averageCharSize:
					return True
		return False
		
	#对lineNo行，如果有角标，将角标抽出并根据角标做split划分
	def handleIndex(self, lineNo):
		lineCharSizes = self.charSizes[lineNo]
		attributesList=[]
		attributesIndex=[]
		line = []
		tmpIndex = ''
		
		averageCharSize = self.getAverageCharSizeForLine(lineNo)
		wordList = uni(self.header[lineNo]).strip().split()
		assert(len(wordList) == len(lineCharSizes))
		
		for i in range(len(wordList)):
			assert(len(wordList[i]) == len(lineCharSizes[i]))
			for j in range(len(wordList[i])):
				if lineCharSizes[i][j] < averageCharSize:
					line.append('#')
					tmpIndex += wordList[i][j] + u','
				else:
					line.append(wordList[i][j])
					if tmpIndex != '': 
						tmpIndex = tmpIndex.replace(u'(','').replace(u')','').replace('{','').replace('}','').replace(u'*','').replace(u'\u2217','')
						attributesIndex.append(Tools.flatList([x for x in tmpIndex.split(u',') if x != u'']))
					tmpIndex=''
			line.append(' ')
		attributesList = [x for x in ''.join(line).split('#') if x != '']
		if tmpIndex != '': 
			tmpIndex = tmpIndex.replace(u'(','').replace(u')','').replace('{','').replace('}','').replace(u'*','').replace(u'\u2217','')
			attributesIndex.append(Tools.flatList([x for x in tmpIndex.split(u',') if x != u'']))
		#print '.join(line)', ''.join(line)
		#print 'attributesList,attributesIndex', attributesList, attributesIndex
		attributesList = [utf8(x) for x in attributesList]
		for i in range(len(attributesIndex)):
			for j in range(len(attributesIndex[i])):
				attributesIndex[i][j] = utf8(attributesIndex[i][j])
		return attributesList, attributesIndex
	
	#第lineNo行是否有明显的大空格
	def hasObviousBigSpace(self,lineNo):
		words = self.header[lineNo].strip().split()
		if len(words) == 1:
			return False
		
		averageDist = 0
		for i in range(1,len(words)):
			averageDist += self.xpos[lineNo][i][0] - self.xpos[lineNo][i-1][1]
		averageDist /= len(words) - 1
		
		for i in range(1,len(words)):
			if self.xpos[lineNo][i][0] - self.xpos[lineNo][i-1][1] > averageDist*5:
				return True
		return False
	
	#第lineNo行用明显的大空格分列
	def splitByObviousBigSpace(self,lineNo):
		words = self.header[lineNo].strip().split()
		if len(words) == 1:
			return words
		averageDist = 0
		for i in range(1,len(words)):
			averageDist += self.xpos[lineNo][i][0] - self.xpos[lineNo][i-1][1]
		averageDist /= len(words) - 1
		list = []
		one = words[0]
		for i in range(1,len(words)):
			if self.xpos[lineNo][i][0] - self.xpos[lineNo][i-1][1] > averageDist*5:
				list.append(one)
				one = words[i]
			else:
				one += ' ' + words[i]
		if one != '':
			list.append(one)
		return list