# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import  xml.dom.minidom
def getHeader(pdfpath):
	os.system(Config.WORKSPACE+'/pdfminer/tools/pdf2txt.py -t xml %s > '%(pdfpath)+Config.WORKSPACE+'/py_scikit/tmp/pdf.xml')
	dom = xml.dom.minidom.parse('./py_scikit/tmp/pdf.xml')
	root = dom.documentElement
	linesXML = root.getElementsByTagName('textline')
	header = []
	fonts = []
	sizes = []
	print 'len:',len(linesXML)
	for lineXML in linesXML:
		texts = lineXML.getElementsByTagName('text')
		s=''
		for text in texts:
			s+=text.firstChild.data.encode('utf-8')
		font = texts[1].getAttribute('font')
		size = texts[1].getAttribute('size')
		header.append(s)
		fonts.append(font)
		sizes.append(size)
	return header, fonts, sizes
if __name__ == '__main__':
	header, fonts, sizes = getHeader('./test.pdf')