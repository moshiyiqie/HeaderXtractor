# -*- coding: utf-8 -*- 
import re
import os
import Config
os.chdir(Config.WORKSPACE)
sourceDir = r'./resource'

#加了个很快的缓存，几十倍的性能提升吧
file_cache={}
def __fileContain(path, x):
	if file_cache.has_key(path):
		return file_cache[path].count(x.lower()) > 0
	else:
		file_cache[path]=[line.strip().lower() for line in open(path).readlines()]
		return file_cache[path].count(x.lower()) > 0

def isPhone(x):
	return isdigit(x) and len(x)>=6
def isDegree(x):
	path = sourceDir+r'/db/degree.txt'#ok
	return __fileContain(path,x)
	
#-----------attribute in paper---------------
def isEmail(x):
	s=re.findall(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*',x)
	return len(s)>0
def isURL(x):
	s=re.findall(r'[a-zA-z]+://[^\s]*',x)
	return len(s)>0
def isSingleCap(x):
	s1=re.findall(r'[a-zA-Z]',x)
	s2=re.findall(r'[A-Z]',x)
	return len(s1)==1 and len(s2)==1
def isPostCode(x):
	path = sourceDir + r'/db/postcode_prefix.txt'
	return [line.strip() for line in open(path).readlines()].count(x) > 0
def isAbstract(x):
	return x.lower() == 'abstract'
def isPage(x):
	return len(x.strip()) - len('page') <= 4 and 'page' in x.lower()
def isKeyWord(x):
	return 'keyword' in x.strip().replace(' ','').lower()
def isIntro(x):
	return 'introduction' in x.strip().replace(' ','').lower()
def isPhone(x):
	xl = x.lower()
	return 'tel' == xl or 'fax' == xl or 'telephone' in xl or 'tel:' in xl or 'fax:' in xl or 'phone' in xl
def isMonth(x):
	path = sourceDir+r'/db/month.txt'#ok
	return __fileContain(path,x)
def isPrep(x):
	return 'at' in x.lower() or 'in' in x.lower() or 'of' in x.lower()
def isPubNum(x):
	path = sourceDir+r'/db/pubnum.txt'#ok
	return __fileContain(path,x)
def isNote(x):
	path = sourceDir+r'/db/note.txt'#ok
	return __fileContain(path,x)
def isAffi(x):
	path = sourceDir+r'/db/affi.txt'#ok
	return __fileContain(path,x)
def isAddr(x):
	path = sourceDir+r'/db/addr.txt'#ok
	return __fileContain(path,x)
def isCity(x):
	path = sourceDir+r'/db/cityname.txt'#ok
	return __fileContain(path,x)
def isState(x):
	path = sourceDir+r'/db/state.txt'#ok
	return __fileContain(path,x)
def isCountry(x):
	path = sourceDir+r'/db/country.txt'#ok
	return __fileContain(path,x)
def isMayName(x):
	path = sourceDir+r'/db/humanname.txt'#ok
	return __fileContain(path,x)

flist = [isEmail,isURL,isSingleCap,isPostCode,isAbstract,
			isPage,isKeyWord, isIntro, isPhone, isMonth, isPrep,
			isPubNum, isNote, isAffi, isAddr, isCity, 
			isState, isCountry, isMayName]
diclist = flist+[isDegree]
def updateWordSpecificVector(word,vector):
	for fun in flist:
		if not vector.has_key(fun.__name__):
			vector[fun.__name__]=0
		vector[fun.__name__] += int(fun(word))

if __name__ == '__main__':
	#line = 'Tel: +44 (0) 121 414 4791, Fax: +44 (0) 121 414 4281'
	#for word in line.split(' '):
	#	print word+' '+str(isPhone(word))
	'''
	测试

	vector={}
	updateWordSpecificVector('rainto@qq.com', vector)
	print vector

	print isPhone('tell')
	print isPhone('tEl')
	print isPhone('tel')
	print isPhone('telephonenum')
		
	print isMonth('jan')
	print isMonth('Jan')
	print isMonth('January')
	print isMonth('Januarys')
		
	print isKeyWord('key word')
	print isKeyWord('key words')
	print isKeyWord('keyword')
	print isKeyWord('keywords')
	print isKeyWord('key t word')

	print isAbstract('abStract')
	print isAbstract('abStracts')
	print isPostCode('WA')
	print isPostCode('wa')
	print isPostCode('KK')
	print isPostCode('AZ')
	print isEmail('rainto@gmail.com')
	print isURL('http://www.hao123.com')
	print isURL('wwwhao123com')
	print isSingleCap('E.')
	print isSingleCap('Esdf.')
	print isSingleCap('EDf.')
	'''