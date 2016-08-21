# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import StanfordNER

def fixForSameSizeSameLabel(header, fonts, sizes, label):
	newLabel = label[:]
	st = 0
	for i in range(1,len(label)-1):
		if fonts[i] == fonts[i-1] and sizes[i] == sizes[i-1] and (fonts[i] != fonts[i+1] or sizes[i] != sizes[i+1]) and newLabel[i] != newLabel[i-1] and newLabel[i]==newLabel[i+1]:
			newLabel[i] = newLabel[i-1]
	for i in range(1,len(label)-1):
		if fonts[i] == fonts[i+1] and sizes[i] == sizes[i+1] and (fonts[i] != fonts[i-1] or sizes[i] != sizes[i-1]) and newLabel[i] != newLabel[i+1] and newLabel[i]==newLabel[i-1]:
			newLabel[i] = newLabel[i+1]
	return newLabel
#有@符号，则直接认定为email
def fixForAt(header, label):
	newLabel = label[:]
	for i in range(len(label)):
		if '@' in header[i]:
			newLabel[i] = '<email>'
	return newLabel
#当没有作者时，将标题行下面的第一行作为作者
def fixForCheckIfNoAuthor(header, label):
	newLabel = label[:]
	noAuthor = True
	for i in range(len(label)):
		if label[i] == '<author>': noAuthor = False
	if noAuthor:
		st=-1
		for i in range(len(label)):
			if label[i] == '<title>': 
				st = i
				break
		if st == -1: return newLabel
		for i in range(st, len(label)):
			if label[i] == '<title>':
				continue
			else:
				newLabel[i] = '<author>'
				break
	return newLabel
#含有university和institute，直接判定为affiliation
def fixForContainUniversity(header, label):
	words = ['universit', 'university', 'univercity', 'universite', 'institute', 'departamen', 'lab']
	newLabel = label[:]
	if(len(header[i].split()) >= 10) return newLabel
	for i in range(len(label)):
		if any([(word in header[i].lower()) for word in words ]):
			newLabel[i] = '<affiliation>'
	return newLabel
	
def fixForDistantTitle(label):
	newLabel = label[:]
	titleNo=[]
	for i in range(0, len(label)):
		if label[i] == '<title>':
			titleNo.append(i)
	for i in range(1,len(titleNo)):
		if titleNo[i] - titleNo[i-1] > 1:
			newLabel[titleNo[i]] = '<unknow>'
	return newLabel
	
#当没有标题时，将作者行上面的第一行作为标题
def fixForCheckIfNoTitle(header, label):
	newLabel = label[:]
	noTitle = True
	for i in range(len(label)):
		if label[i] == '<title>': noTitle = False
	if noTitle:
		st=-1
		for i in range(len(label)):
			if label[i] == '<author>': 
				st = i
				break
		if st <= 0: return newLabel
		newLabel[st - 1] = '<title>'
	return newLabel
#一般来说title后面不可能是note，将title下一行的note修正为title
def fixForNoteAfterTitle(header, label):
	newLabel = label[:]
	for i in range(len(label) - 1):
		if label[i] == '<title>' and label[i+1] == '<note>':
			newLabel[i+1] = '<title>'
			break
	return newLabel

#利用stanford ner来进行机构、地址、作者的修正
def fixByStanfordNER(header, label):
	newLabel = label[:]
	for i in range(len(label)):
		res = StanfordNER.getNerResult(header[i])
		#if u'PERSON' in res.keys(): print 'FOUND person!!', header[i], label[i]
		if u'PERSON' in res.keys() and label[i] != '<author>'  and label[i] != '<title>' and label[i] != '<abstract>':
			print '[NER-person] ', header[i], label[i]
			newLabel[i] = '<author>'
		elif u'ORGANIZATION' in res.keys() and label[i] != '<affiliation>' and label[i] != '<abstract>' and label[i] != '<title>' and len(header[i]) <= 4:
			print '[NER-affiliation] ', header[i], label[i]
			newLabel[i] = '<affiliation>'
		#elif u'LOCATION' in res.keys() and label[i] != '<address>' and label[i] != '<abstract>'  and label[i] != '<title>':
		#	print '[NER-address] ', header[i], label[i]
		#	newLabel[i] = '<address>'
	return newLabel

