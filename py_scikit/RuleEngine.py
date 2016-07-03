# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
def fixForSameSizeSameLabel(fonts, sizes, label):
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
	newLabel = label[:]
	for i in range(len(label)):
		if 'university' in header[i].lower() or 'univercity' in header[i].lower() or 'universite' in header[i].lower() or 'institute' in header[i].lower():
			newLabel[i] = '<affiliation>'
	return newLabel