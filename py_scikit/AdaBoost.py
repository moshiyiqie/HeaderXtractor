# coding: UTF-8
import sys
import Classifier
import numpy as np
import scipy as sp
from sklearn.metrics import classification_report
from sklearn.datasets import load_svmlight_file
import Data
import os
import Config
os.chdir(Config.WORKSPACE)
sys.stdout = open('./pythonsrc/tmp/labout.txt','w')
class AdaBoost:
	def __init__(self,X,y,ratio):
		len = int(ratio*X.shape[0])
		self.X = X[:len]
		self.y = y[:len]
		self.X_testT = X[len:]
		self.y_testT = y[len:]
		
		self.X_test = X[len:]
		self.y_test = y[len:]
		
		#self.X_test = X[:len]
		#self.y_test = y[:len]
		
		self.sums=np.zeros(self.y_test.shape)
		self.W=np.ones((self.X_test.shape[0],1)).flatten(1)/self.X_test.shape[0]
		
		self.M = 20
		self.G={}
		for i in range(0,self.M):
			self.G[i] = Classifier.randomSampleRandomAlgorithmForWeakClf(self.X, self.y, 0.75)
		#print self.W
	def sign(self,mat):
		eps = 0.0000000001
		res = np.zeros(mat.shape)
		for i in range(mat.shape[0]):
			if mat[i] > eps: res[i] = 1
			elif mat[i] < -eps: res[i] = -1
			else: res[i] = 0
		return res
	def train(self):
		self.alpha={}#分类器权重
		for i in range(self.M):#循环计算每个分类器的权重
			#print '正在处理第%d个分类器'%(i)
			sg = self.G[i].predict(self.X_test).transpose()#输出训练器的判断结果
			print 'W sum',sum([x for x in self.W])
			np.array(sorted(self.W, reverse = True)).tofile('./pythonsrc/tmp/W'+str(i)+'.npdata', '\t' )
			print 'sg,',sg
			print 'self.y_test,',self.y_test
			e = sum([self.W[j] for j in range(sg.shape[0]) if sg[j] != self.y_test[j] ])#计算误差率
			if e > 0.5:
				#print '误差率过大，作废'
				continue
			print 'e value:',e
			self.alpha[i] = 1.0/2*np.log((1-e)/(e+0.0000001))*(i+1)#计算分类器权重
			Z = self.W * np.exp(-self.alpha[i] * self.y_test * np.array(sg))
			self.W=(Z/Z.sum()).flatten(1)
			if self.updateSumGetErrorNum(i)==0:
				#print i+1," weak classifier is enough to  make the error to 0"
				break
			self.printFinalResult()
		self.testOnTestSet(self.X_testT, self.y_testT)
	def updateSumGetErrorNum(self,t):#计算分类错误的个数
		#print 'alpha ',self.alpha[t]
		self.sums=self.sums+self.G[t].predict(self.X_test).flatten(1)*self.alpha[t]
		pre_y=self.sign(self.sums)
		t = sum([pre_y[i] != self.y[i] for i in range(pre_y.shape[0]) ])
		print 'sum:',self.sums
		print '错误数:',t
		return t
	def printFinalResult(self):
		pre_y=self.sign(self.sums)
		print classification_report(self.y_test, pre_y)
	def testOnTestSet(self, X_testT, y_testT):
		Sum = np.zeros(y_testT.shape)
		for i in range(self.M):
			if not self.alpha.has_key(i): continue
			#print 'i:',i
			Sum = Sum + self.G[i].predict(X_testT) * self.alpha[i]
		pre_y=self.sign(Sum)
		print classification_report(y_testT, pre_y).split('\n')[-4]
	
if __name__ == '__main__':
	data = Data.Data()
	data.transform2LibsvmStyleForOneClass('./pythonsrc/tmp/tmp.svmdata','keyword')
	X, y = load_svmlight_file('./pythonsrc/tmp/tmp.svmdata')
	adaBoost = AdaBoost(X,y,0.7)
	adaBoost.train()
	'''
	classification = ['abstract','address','affiliation','author','date','degree','email','intro','keyword','note','page','phone','pubnum','title','web']
	data = Data.Data()
	for cls in classification:
		print cls,'\t',
		data.transform2LibsvmStyleForOneClass('./pythonsrc/tmp/tmp.svmdata',cls)
		X, y = load_svmlight_file('./pythonsrc/tmp/tmp.svmdata')
		adaBoost = AdaBoost(X,y,0.7)
		adaBoost.train()
	'''
	#adaBoost.train()
	#adaBoost.printFinalResult()