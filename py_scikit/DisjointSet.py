# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
class DisjointSet:
	par=[]
	def __init__(self, elementNum):
		self.par = [x for x in range(0,elementNum+1)]
		
	def find(self, id):
		if self.par[id] == id:
			return id
		else:
			res = self.find(self.par[id])
			self.par[id] = res
			return res
	def unite(self, id1, id2):
		id1 = self.find(id1)
		id2 = self.find(id2)
		if id1 == id2: return
		else: self.par[id1] = id2
