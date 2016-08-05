# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
import DisjointSet
import Geometry
import Tools
import copy
import GraphicManager

BLOCK_HEIGHT_RATIO = 0.7
class Block:
	header=''
	l=0.0
	r=0.0
	u=0.0
	d=0.0
	rectangle = Geometry.Rectangle()
	originIdx = 0
	def __init__(self, headerContent, xposList,sizesList,ypos,originIdx):
		self.header = headerContent
		self.l = xposList[0][0] - sizesList[0][0]
		self.r = xposList[-1][-1] + sizesList[-1][-1]
		averageSz = sum([float(x) for x in Tools.flatList(sizesList)])*1.0 / len(Tools.flatList(sizesList))
		self.u = ypos - averageSz * BLOCK_HEIGHT_RATIO
		self.d = ypos + averageSz * BLOCK_HEIGHT_RATIO
		self.rectangle = Geometry.Rectangle(self.l, self.r, self.u, self.d)
		self.originIdx = originIdx

#合并相交的词块矩形
def unionBlockByRectangleIntersect(dsu, blockList):
	for i in range(len(blockList)):
		for j in range(i+1,len(blockList)):
			#if i == 0 and j == 1:
			#	print 'i::',blockList[i].rectangle.__dict__
			#	print 'j::',blockList[j].rectangle.__dict__
			#	print 'res::',blockList[i].rectangle.isIntersect(blockList[j].rectangle)
			if blockList[i].rectangle.isIntersect(blockList[j].rectangle):
				dsu.unite(i,j)
#将合并后的块按块平均高度排序后输出块列表
def getBlockSetList(dsu, blockList):
	blockSet = {}
	for i in range(len(blockList)):
		setId = dsu.find(i)
		if not blockSet.has_key(setId):
			blockSet[setId] = [[],0]
		blockSet[setId][0].append(blockList[i])
		blockSet[setId][1] += (blockList[i].u + blockList[i].d)/2.0
	blockSetList = []
	for key in blockSet.keys():
		blockSet[key][1] /= len(blockSet[key][0])
		blockSetList.append(copy.deepcopy(blockSet[key]))
		#print '===================='
		#for blk in blockSet[key][0]:
		#	print blk.__dict__
		#print '===================='
	blockSetList.sort(key = lambda x:x[1])
	return [x[0] for x in blockSetList]#仅取块集合

#该函数利用并查集通过词框合并得到一个个块，最后排序输出给分类器进行分类，排序规则如下
#计算块集合的平均高度y，首先输出平均高度y较小的块，块内按y从小到大
def BlockUnionProcess(header, charSizes, ypos, xpos):
	dsu = DisjointSet.DisjointSet(len(header))
	blockList = []
	for i in range(len(header)):
		blockList.append( Block(header[i], xpos[i], charSizes[i], ypos[i], i) )
	unionBlockByRectangleIntersect(dsu, blockList)
	blockSetList = getBlockSetList(dsu, blockList)
	for i in range(len(blockSetList)):
		blockSetList[i].sort(key = lambda x: (x.u+x.d)/2.0)
	#print 'blockSetList', blockSetList

	GraphicManager.printRecWithWords(Tools.flatList(blockSetList))

	sortedIdxList = []
	for blockset in blockSetList:
		for block in blockset:
			sortedIdxList.append(block.originIdx)
	return sortedIdxList