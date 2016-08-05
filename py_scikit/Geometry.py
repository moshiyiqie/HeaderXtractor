# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)

class Rectangle:
	l=0.0
	r=0.0
	u=0.0
	d=0.0
	def __init__(l=0,r=0,u=0,d=0):
		self.l = l
		self.r = r
		self.u = u
		self.d = d
	#判断线段l1,r1, l2,r2是否相交
	def __segmentIntersect(l1,r1,l2,r2):
		if r1 > r2:
			l1,l2,r1,r2 = l2,l1,r2,r1
		return l2 < r1
	#判断与另一矩形是否相交
	def isIntersect(rec):
		return segmentIntersect(self.l, self.r, rec.l, rec.r) and segmentIntersect(self.u, self.d, rec.u, rec.d)