# -*- coding: utf-8 -*- 
import os
import Config
os.chdir(Config.WORKSPACE)
import Data
from sklearn.datasets import load_svmlight_file
import Classifier
from sklearn.metrics import classification_report
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
X, y = load_svmlight_file('./resource/向量化后_带上下文信息_everyline.svmdata')

limit = int(y.shape[0]*0.7)
clf = Classifier.trainRF(X,y,0.7)
print sorted(clf.feature_importances_)


'''
for k_ in range(1,30):
	print k_,'\t',
	X_new = SelectKBest(chi2, k=k_).fit_transform(X, y)
	limit = int(y.shape[0]*0.7)
	clf = Classifier.trainRF(X_new,y,0.7)
	y_pred = clf.predict(X_new[limit:])
	print classification_report(y[limit:], y_pred, target_names = Classifier.classification).split('\n')[-2]
'''