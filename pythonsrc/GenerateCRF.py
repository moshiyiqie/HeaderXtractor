# -*- coding: utf-8 -*- 
import re
import Config
import os
import LineSpecific
import GenerateVector
import WordSpecific
os.chdir(Config.WORKSPACE)

def getFeatureStr(line):
	line = line.strip()
	lineno = line.split('::line_number::')[1]
	text = line.split('::line_number::')[0]
	label = re.findall(r'<\w+>', text)[0]
	text = re.sub(r'</?\w+>','', text).strip()
	#if len(text) == 0: continue
	featureDic={}
	#print text,lineno,label
	LineSpecific.updateForCRF(text[:], featureDic)
	feature=''
	for key in featureDic:
		feature+=key + ':'
		if featureDic[key] >= 0.999:
			feature += 'YES '
		elif featureDic[key] >= 0.5:
			feature += 'HIGH '
		elif featureDic[key] <= 0.001:
			feature += 'NO '
		else:
			feature += 'MID '
	
	wordDic={}
	for word in text.split():
		WordSpecific.updateWordSpecificVector(word, wordDic)
	for key in wordDic:
		wordDic[key] = wordDic[key]*1.0/len(text.split())
		#feature += key + ':' + str(wordDic[key]*1.0/len(text.split())) + ' '
	for key in wordDic:
		feature+=key + ':'
		if wordDic[key] >= 0.999:
			feature += 'YES '
		elif wordDic[key] >= 0.5:
			feature += 'HIGH '
		elif wordDic[key] <= 0.001:
			feature += 'NO '
		else:
			feature += 'MID '
	return feature + 'lineno:' + str(lineno) + ' '

def generateTrainFile(path = './resource/tagged_headers_everyline.txt'):
	#pickedFeature = [dictWordNumPer, nonDictWordNumPer, cap1DicWordNumPer,
	#	cap1NonDicWordNumPer, digitNumPer, affiNumPer, addrNumPer, 
	#	dateNumPer, degreeNumPer, phoneNumPer, pubNumPer, noteNumPer,singleDigitNumPer]
	
	
	lines = open(path).readlines()
	fout = open('./py_scikit/tmp/crf_train-pub.txt','w')
	#textout = open('./py_scikit/tmp/crf_train_text.txt','w')#输出不带标签的文本
	paperno=0
	for line in lines:
		line = line.strip()
		lineno = line.split('::line_number::')[1]
		text = line.split('::line_number::')[0]
		if lineno == '0':
			print "Generating page:"+str(paperno)
			if paperno == 700:
				fout.close()
				fout = open('./py_scikit/tmp/crf_test-pub.txt','w')
				#textout = open('./py_scikit/tmp/crf_test_text.txt','w')
			#fout.write('\n')
			#textout.write('\n')
			paperno+=1
		label = re.findall(r'<\w+>', text)[0]
		text = re.sub(r'</?\w+>','', text).strip()
		if len(text) == 0: continue
		
		feature = getOneLineFeatureStr(text[:],True)
		
		fout.write(' '.join([text.replace(' ','|||'), feature, lineno, label]) + '\n')
		#textout.write(text + '\n')
		
	fout.close()
	#textout.close()

highFreqWordsCache=[]

def getCiFeature(line):
	global highFreqWordsCache
	if len(highFreqWordsCache) == 0:
		print '[Info: CRFFeature] Loading Keyword...'
		lines = open('./resource/keyword.txt').readlines()
		for fileline in lines:
			if len(fileline.strip())==0 : continue
			highFreqWordsCache.append(fileline.split(':::')[0].strip().lower())
			if len(highFreqWordsCache) >= 500:
				break
		highFreqWordsCache = set(highFreqWordsCache)
	feature = ''
	lowerLine = line.lower()
	for word in highFreqWordsCache:
		if word in lowerLine:
			feature += 'HAS_'+word+':YES '
		else:
			feature += 'HAS_'+word+':NO '
	return feature

#输入一行头部文本，输出该行crf++格式的特征
def getOneLineFeatureStr(line, addCiFeature=False):

	text = line
	featureDic={}
	LineSpecific.updateForCRF(text[:], featureDic)
	feature = ''
	if addCiFeature==True: 
		feature += getCiFeature(line)#添加关键词特征
	for key in featureDic:
		feature += key + ':'
		if featureDic[key] >= 0.999:
			feature += 'YES '
		elif featureDic[key] >= 0.5:
			feature += 'HIGH '
		elif featureDic[key] <= 0.001:
			feature += 'NO '
		else:
			feature += 'MID '
	
	notBoxFeature={}
	LineSpecific.updateLineSpecificVectorNotBox(text[:], notBoxFeature)
	for key in notBoxFeature:
		feature += key + ':' + notBoxFeature[key] + ' '


	wordDic={}
	#for word in text.split():
	WordSpecific.updateWordSpecificVectorOneLine(text[:], wordDic)
	for key in wordDic:
		wordDic[key] = wordDic[key]*1.0/len(text.split())
		#feature += key + ':' + str(wordDic[key]*1.0/len(text.split())) + ' '
	for key in wordDic:
		feature+=key + ':'
		if wordDic[key] >= 0.999:
			feature += 'YES '
		elif wordDic[key] >= 0.5:
			feature += 'HIGH '
		elif wordDic[key] <= 0.001:
			feature += 'NO '
		else:
			feature += 'MID '
	#if  len([i for i, ltr in enumerate(feature) if ltr == ':']) != 148:
		#print '[Feature Size Error]:', line
	return feature

#对于输入的头部生成crf测试文件-不带富文本信息
def generateTestFileFromHeaderText(header, addCiFeature):
	#pickedFeature = [dictWordNumPer, nonDictWordNumPer, cap1DicWordNumPer,
	#	cap1NonDicWordNumPer, digitNumPer, affiNumPer, addrNumPer, 
	#	dateNumPer, degreeNumPer, phoneNumPer, pubNumPer, noteNumPer,singleDigitNumPer]
	
	fout = open('./CRF++/train/crf_test.txt','w')
	lineno=0
	label = 'Unknown'
	for line in header:
		line = line.strip()
		if len(line) == 0: continue
		feature = getOneLineFeatureStr(line[:], addCiFeature)
		fout.write(' '.join(['ORIGIN', feature, str(lineno), label]) + '\n')
		lineno+=1
		
	fout.close()
#对于输入的头部生成crf训练格式的数据-带富文本信息
def generateCrfFileFromHeaderTextWithRichInfo(header, fonts, sizes, label, ypos):
	yPosListTmp = [float(x) for x in ypos]
	yPosListTmp.sort()
	yPosList = []
	for i in range(len(yPosListTmp)):
		if len(yPosList) > 0 and abs(float(yPosListTmp[i]) - float(yPosList[-1]))<=1:
			continue
		else:
			yPosList.append(yPosListTmp[i])

	fonts_lineno=['' for i in range(len(yPosList))]#和fonts，sizes不同的是，这里的下标是视觉的行，而fonts中的下标是前面分块排序后的输出顺序，其不一定代表视觉上的行
	sizes_lineno=['' for i in range(len(yPosList))]

	data = ''
	for i in range(len(header)):
		line = header[i].strip()
		if len(line) == 0: continue
		feature = getOneLineFeatureStr(line[:])#字、词特征
		lineno = 0
		for j in range(len(yPosList)):
			if abs(ypos[i] - yPosList[j]) < 1:
				lineno = j
				break

		fontDiff = 'NO'
		if lineno == 0:
			fontDiff = 'FIR'
		elif lineno>=1 and fonts[i] != fonts_lineno[lineno-1]:
			fontDiff = 'YES'

		szDiff = 'NO'
		if lineno == 0:
			szDiff = 'FIR'
		elif lineno>=1 and sizes[i] != sizes_lineno[lineno-1]:
			szDiff = 'YES'

		fonts_lineno[lineno] = fonts[i]
		sizes_lineno[lineno] = sizes[i]
		data += ' '.join([line.replace(' ','|||'), feature, str(lineno),fontDiff,szDiff,label[i]]) + '\n'
	return data

if __name__ == '__main__':
	generateTrainFile()