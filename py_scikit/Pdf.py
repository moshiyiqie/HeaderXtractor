# -*- coding: utf-8 -*- 
import os
import Config
import sys
import StringManager
import re
import Author
os.chdir(Config.WORKSPACE)
import Tools
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
	#获得PDF文件的头部、字体、大小
	def loadPdfByPDFbox(self,pdfpath):
		pdfboxOutputPath = './py_scikit/tmp/pdfboxResult.txt'
		oscmd='java -Dfile.encoding=utf-8 -jar ./py_scikit/PDFManagerSizeFont-openjdk.jar ' + pdfpath + ' ' + pdfboxOutputPath
		os.system(oscmd)
		#pdfContent = os.popen(oscmd).readlines()
		pdfContent = open(pdfboxOutputPath).readlines()
		#open('./py_scikit/tmp/pdfContentDEBUG.txt','w').writelines(pdfContent)
		lineNo=1
		for line in pdfContent:
			line = line.strip()
			#line = line.replace('?','')#去掉不能识别的问号
			if len(line)==0: continue
			if lineNo>=2 and 'abstract' in line.lower(): break
			first = True
			content = ''
			for one in line.split():
				fontSizeWord = one.split('|||')
					
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
		
	#根据每一行的y坐标进行排序
	def sortByYpos(self):
		length = len(self.ypos)
		for i in range(length):
			for j in range(i+1, length):
				if self.ypos[i] > self.ypos[j]:
					self.ypos[i], self.ypos[j] = self.ypos[j], self.ypos[i]
					self.header[i], self.header[j] = self.header[j], self.header[i]
					self.fonts[i], self.fonts[j] = self.fonts[j], self.fonts[i]
					self.sizes[i], self.sizes[j] = self.sizes[j], self.sizes[i]
					self.xpos[i], self.xpos[j] = self.xpos[j], self.xpos[i]
					self.charSizes[i], self.charSizes[j] = self.charSizes[j], self.charSizes[i]
	
	#得到lineNo行的平均字体大小
	def getAverageCharSizeForLine(self,lineNo):
		i = lineNo
		averageCharSize = 0.0
		charNum = 0
		for word in self.charSizes[lineNo]:
			for sz in word:
				averageCharSize += sz
				charNum += 1
		averageCharSize /= charNum
		return averageCharSize
		
	#是否含有角标
	def hasIndex(self, lineNo):
		lineCharSizes = self.charSizes[lineNo]
		averageCharSize = self.getAverageCharSizeForLine(lineNo)
		wordList = uni(self.header[lineNo]).strip().split()
		assert(len(wordList) == len(lineCharSizes))
		for i in range(len(wordList)):
			if len(wordList[i]) != len(lineCharSizes[i]):
				open('./py_scikit/tmp/debug.txt','w').writelines(' '.join(['wordList[i], lineCharSizes[i]', str(len(wordList[i])), str(len(lineCharSizes[i])), utf8(wordList[i])]))
			assert(len(list(wordList[i])) == len(lineCharSizes[i]))
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
