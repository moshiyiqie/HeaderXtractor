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
	fout = open('./CRF++/train/crf_train.txt','w')
	paperno=0
	for line in lines:
		line = line.strip()
		lineno = line.split('::line_number::')[1]
		text = line.split('::line_number::')[0]
		if lineno == '0':
			print "Generating page:"+str(paperno)
			if paperno == 800:
				fout.close()
				fout = open('./CRF++/train/crf_test.txt','w')
			fout.write('\n')
			paperno+=1
		label = re.findall(r'<\w+>', text)[0]
		text = re.sub(r'</?\w+>','', text).strip()
		if len(text) == 0: continue
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
		
		fout.write(' '.join([text.replace(' ','|||'), feature, lineno, label]) + '\n')
		
	fout.close()
def generateTestFileFromHeaderText(header):
	#pickedFeature = [dictWordNumPer, nonDictWordNumPer, cap1DicWordNumPer,
	#	cap1NonDicWordNumPer, digitNumPer, affiNumPer, addrNumPer, 
	#	dateNumPer, degreeNumPer, phoneNumPer, pubNumPer, noteNumPer,singleDigitNumPer]
	
	fout = open('./CRF++/train/crf_test.txt','w')
	lineno=0
	for line in header:
		line = line.strip()
		text = line
		label = 'Unknown'
		if len(text) == 0: continue
		featureDic={}
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
		
		fout.write(' '.join(['ORIGIN', feature, str(lineno), label]) + '\n')
		lineno+=1
		
	fout.close()
if __name__ == '__main__':
	generateTrainFile()