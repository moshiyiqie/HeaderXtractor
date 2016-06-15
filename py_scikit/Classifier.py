# -*- coding: utf-8 -*- 
import os
import Config
os.chdir(Config.WORKSPACE)
from sklearn.datasets import load_svmlight_file
import numpy as np
from sklearn.svm import SVC
from sklearn.svm import NuSVC
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
import Data
import random
#X_trian, y_train = load_svmlight_file('./resource/向量化后_带上下文信息_everyline.svmdata')
classification = ['abstract','address','affiliation','author','date','degree','email','intro','keyword','note','page','phone','pubnum','title','web']
def trainCSVC(X, y, ratio):
	limit = int(X.shape[0] * ratio)
	clf = SVC()
	clf.fit(X[:limit],y[:limit])
	#y_pred = clf.predict(X[limit:])
	#print classification_report(y[limit:], y_pred, target_names = classification)
	return clf
	#print confusion_matrix(y_train[-3000:], y_predict)
	#print y_train
def trainNuSVC(X, y, ratio):
	limit = int(X.shape[0] * ratio)
	clf = NuSVC()
	clf.fit(X[:limit],y[:limit])
	return clf
	
def trainLinearSVC(X, y, ratio):
	limit = int(X.shape[0] * ratio)
	clf = LinearSVC()
	clf.fit(X[:limit],y[:limit])
	return clf
def trainDT(X, y, ratio):
	limit = int(X.shape[0] * ratio)
	clf = tree.DecisionTreeClassifier()
	clf.fit(X[:limit],y[:limit])
	return clf
def trainRF(X, y, ratio):
	limit = int(X.shape[0] * ratio)
	clf = ExtraTreesClassifier()
	clf.fit(X[:limit],y[:limit])
	return clf
def trainAdaboost(X, y, ratio):
	limit = int(X.shape[0] * ratio)
	clf = AdaBoostClassifier(n_estimators = 500)
	clf.fit(X[:limit],y[:limit])
	return clf
def trainBagging(X, y, ratio):
	limit = int(X.shape[0] * ratio)
	clf = BaggingClassifier(n_estimators = 500)
	clf.fit(X[:limit],y[:limit])
	return clf
def randomSample(X,y):
	
	XX = X.toarray()
	yy = y.tolist()
	#print type(XX)
	ratio = random.uniform(0.99,1.0)
	sampleLen = int(len(XX) * ratio)
	idx = [i for i in range(len(XX))]
	random.shuffle(idx)
	idx = idx[:sampleLen]
	X_s = np.array([XX[i] for i in idx])
	y_s = np.array([yy[i] for i in idx])
	#print '采样长度:',sampleLen
	#print '采样:',X_s
	return X_s, y_s

def randomEqualSample(X,y):
	XX = X.toarray()
	yy = y.tolist()
	
	p_idx = []
	n_idx = []
	for i in range(len(y)):
		if y[i] == 1: p_idx.append(i)
		else: n_idx.append(i)
	
	ratio = random.uniform(0.8,1.0)
	sampleLen = int(len(p_idx) * ratio)
	
	random.shuffle(p_idx)
	random.shuffle(n_idx)
	X_s = np.array([XX[i] for i in p_idx[:sampleLen]] + [XX[i] for i in n_idx[:sampleLen]] )
	y_s = np.array([yy[i] for i in p_idx[:sampleLen]] + [yy[i] for i in n_idx[:sampleLen]] )
	#print '采样长度:',sampleLen,len(y_s)
	#print '采样:',X_s
	return X_s, y_s

def randomSampleRandomAlgorithmForWeakClf(X, y, ratio):
	limit = int(X.shape[0] * ratio)
	X_train = X[:limit]
	y_train = y[:limit]
	func=[trainLinearSVC,trainDT,trainRF]
	X_s, y_s = randomSample(X_train, y_train)
	clsidx = random.randint(0,len(func)-1)
	#print '用'+str(clsidx)+'算法' 
	
	return func[clsidx](X_s, y_s, 1)

if __name__ == '__main__':
	data = Data.Data()
	for cls in classification:
		data.transform2LibsvmStyleForOneClass('./pythonsrc/tmp/tmp.svmdata',cls)
		X, y = load_svmlight_file('./pythonsrc/tmp/tmp.svmdata')
		clf = trainRF(X,y,0.7)
		limit = int(len(y)*0.7)
		y_pred = clf.predict(X[limit:])
		print cls,'\t',classification_report(y[limit:], y_pred).split('\n')[-4]
	'''
	for cls in classification:
		data.transform2LibsvmStyleForOneClass('./pythonsrc/tmp/tmp.svmdata',cls)
		X, y = load_svmlight_file('./pythonsrc/tmp/tmp.svmdata')
		clf = trainCSVC(X,y,0.7)
		limit = int(len(y)*0.7)
		y_pred = clf.predict(X[limit:])
		print cls,'\t',classification_report(y[limit:], y_pred).split('\n')[-4]
	print '===================================='
	for cls in classification:
		data.transform2LibsvmStyleForOneClass('./pythonsrc/tmp/tmp.svmdata',cls)
		X, y = load_svmlight_file('./pythonsrc/tmp/tmp.svmdata')
		clf = trainLinearSVC(X,y,0.7)
		limit = int(len(y)*0.7)
		y_pred = clf.predict(X[limit:])
		print cls,'\t',classification_report(y[limit:], y_pred).split('\n')[-4]
	print '===================================='
	for cls in classification:
		data.transform2LibsvmStyleForOneClass('./pythonsrc/tmp/tmp.svmdata',cls)
		X, y = load_svmlight_file('./pythonsrc/tmp/tmp.svmdata')
		clf = trainDT(X,y,0.7)
		limit = int(len(y)*0.7)
		y_pred = clf.predict(X[limit:])
		print cls,'\t',classification_report(y[limit:], y_pred).split('\n')[-4]
	print '===================================='
	for cls in classification:
		data.transform2LibsvmStyleForOneClass('./pythonsrc/tmp/tmp.svmdata',cls)
		X, y = load_svmlight_file('./pythonsrc/tmp/tmp.svmdata')
		clf = trainAdaboost(X,y,0.7)
		limit = int(len(y)*0.7)
		y_pred = clf.predict(X[limit:])
		print cls,'\t',classification_report(y[limit:], y_pred).split('\n')[-4]
	print '===================================='
	for cls in classification:
		data.transform2LibsvmStyleForOneClass('./pythonsrc/tmp/tmp.svmdata',cls)
		X, y = load_svmlight_file('./pythonsrc/tmp/tmp.svmdata')
		clf = trainBagging(X,y,0.7)
		limit = int(len(y)*0.7)
		y_pred = clf.predict(X[limit:])
		print cls,'\t',classification_report(y[limit:], y_pred).split('\n')[-4]
	'''