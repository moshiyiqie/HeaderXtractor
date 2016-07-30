# -*- coding: utf-8 -*- 
import os
import Config
import sys
import PdfProcessor
os.chdir(Config.WORKSPACE)
import re
import StringManager
#获得email列表
def getEmails(header,label, affiliationsIndex, affiEmailMap, pdf):
	emailBlocks = getEmailBlocks(pdf,label)
	#print 'emailBlocks::',emailBlocks
	#print 'affiliationsIndex::',affiliationsIndex
	if len(emailBlocks) == len(affiliationsIndex):
		for i in range(len(affiliationsIndex)):
			#print 'handleOneEmailBlock(emailBlocks[i])', handleOneEmailBlock(emailBlocks[i])
			affiEmailMap[affiliationsIndex[i][0]] = handleOneEmailBlock(emailBlocks[i])
		#print 'affiEmailMap::',affiEmailMap
		return []
	else:
		emails=[]
		for emailBlock in emailBlocks:
			emails += handleOneEmailBlock(emailBlock)
		return [x for x in emails if '@' in x]

#获得email块列表
def getEmailBlocks(pdf,label):
	emailBlocks = []
	for i in range(len(pdf.header)):
		if label[i] == '<email>':
			blockList = StringManager.removeCharBetween(pdf.header[i], '{','}',' ').strip().split()
			emailBlocks += blockList
	return emailBlocks


#处理一个email块，返回解析得到的email
def handleOneEmailBlock(emailBlock):
	emails = []
	text = emailBlock
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
			elif ch == ',' or ch == '|':
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
	emails = [x for x in emails if x != '']
	return emails
	
	
#=============================================================================================================
#OLD FUNCTION!!获取Email，处理了{}这种情况
def OLDgetEmails(header, label):
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
					elif ch == ',' or ch == '|':
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
	emails = [x for x in emails if x != '']
	return emails