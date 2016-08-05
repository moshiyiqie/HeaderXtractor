# -*- coding: utf-8 -*- 
import os
import Config
os.chdir(Config.WORKSPACE)
import Classifier
from sklearn.datasets import load_svmlight_file
from sklearn.decomposition import PCA 
from sklearn.feature_selection import VarianceThreshold
def PCA_func():
	X, y = load_svmlight_file('./resource/向量化后_带上下文信息_everyline.svmdata')
	print Classifier.trainTestReportRF(X.toarray(),y,0.70)
	for ite in range(1,31):
		print 'ite:'+str(ite)+'\t',
		pca = PCA(n_components=ite)
		newX = pca.fit_transform(X.toarray())
		Classifier.trainTestReportRF(newX,y,0.70)
