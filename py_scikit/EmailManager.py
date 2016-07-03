# -*- coding: utf-8 -*- 
import os
import Config
import sys
import PdfProcessor
os.chdir(Config.WORKSPACE)
import re
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