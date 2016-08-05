# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
class DisjointSet:
	par=[]
	def __init__(self, elementNum):
		par = [x for x in range(0,elementNum+1)]
		
	def find(slef, id):
		if par[id] == id:
			return id
		else:
			return par[id]=self.find(par[id])
	def unite(self, id1, id2):
		id1 = self.find(id1)
		id2 = self.find(id2)
		if id1 == id2: return
		else: par[id1] = id2
