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
	return newLabel
def fixForAt(header, label):
	newLabel = label[:]
	for i in range(len(label)):
		if '@' in header[i]:
			newLabel[i] = '<email>'
	return newLabel
def fixForContainUniversity(header, label):
	newLabel = label[:]
	for i in range(len(label)):
		if 'university' in header[i].lower() or 'univercity' in header[i].lower() or 'universite' in header[i].lower():
			newLabel[i] = '<affiliation>'
	return newLabel