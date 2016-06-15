# -*- coding: utf-8 -*- 
import os
import Config
os.chdir(Config.WORKSPACE)
import pickle
class Data:
	vecList = []
	def __init__(self):
		vecList=[]
	def transform2LibsvmStyle(self, path):
		fout = open(path, 'w')
		classification=['abstract','address','affiliation','author','date','degree','email','intro','keyword','note','page','phone','pubnum','title','web']
		if len(self.vecList) == 0:
			#print 'Loading vecList...'
			self.vecList = pickle.load(open(r'./resource/��������_����������Ϣ_everyline.pickle'))
			#print 'Load Complete!'
		toidx={}
		idx = 0
		for vector in self.vecList:
			for key in vector:
				if key.startswith("z_") or key == 'classification' or key.startswith('pre') or key.startswith('next'): continue
				toidx[key] = idx
				idx+=1
			break
		for vector in self.vecList:
			s=str(classification.index(vector['classification']))
			for key in vector:
				if toidx.has_key(key):
					s += ' ' + str(toidx[key])+ ':' + str(vector[key])
			fout.write(s + '\n')
		fout.close()
	def transform2LibsvmStyleForOneClass(self, path, cls):
		fout = open(path, 'w')
		if len(self.vecList) == 0:
			#print 'Loading vecList...'
			self.vecList = pickle.load(open(r'./resource/��������_����������Ϣ_everyline.pickle'))
			#print 'Load Complete!'
		toidx={}
		idx = 0
		for vector in self.vecList:
			for key in vector:
				if key.startswith("z_") or key == 'classification' or key.startswith('pre') or key.startswith('next'): continue
				toidx[key] = idx
				idx+=1
			break
		for vector in self.vecList:
			s=''
			if vector['classification'] == cls: s = '1'
			else: s = '-1'
			for key in vector:
				if toidx.has_key(key):
					s += ' ' + str(toidx[key])+ ':' + str(vector[key])
			fout.write(s + '\n')
		fout.close()
if __name__ == '__main__':
	transform2LibsvmStyle('./resource/��������_����������Ϣ_everyline.svmdata')