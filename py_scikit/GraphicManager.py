# -*- coding: utf-8 -*- 
from graphics import *  
import Geometry
import BlockManager
def printRecWithWords(blockList, idInDSU, dsu):
	win = GraphWin('CSSA', 700, 700) 
	for i in range(len(blockList)):
		content = blockList[i].header
		rect = Rectangle(Point(blockList[i].l, blockList[i].u), Point(blockList[i].r, blockList[i].d))
		rect.draw(win) 
		midx = (blockList[i].l + blockList[i].r)/2
		midy = (blockList[i].u + blockList[i].d) / 2
		message = Text(Point(midx, midy), content)
		message.setSize(7)
		message.draw(win)
		belongSetId = Text(Point(blockList[i].l-20, blockList[i].u), dsu.find(idInDSU[blockList[i].hash()]))
		belongSetId.setSize(12)
		belongSetId.draw(win)
	win.getMouse()  
	win.close()  
'''
#设置画布窗口名和尺寸  
win = GraphWin('CSSA', 700, 700)   
  
#画点  
pt = Point(100, 100)  
pt.draw(win)  
  
#画圆  
cir = Circle(Point(200, 200), 75)  
cir.draw(win)  
cir.setOutline('red') #外围轮廓颜色  
cir.setFill('yellow')   #填充颜色  
  
#画线  
line = Line(Point(650, 100), Point(250, 100))  
line.draw(win)  
  
#画矩形  
rect = Rectangle(Point(300, 300), Point(400, 400))  
rect.setFill('red') #填充颜色  
rect.draw(win)  
  
#画椭圆  
oval = Oval(Point(450, 450), Point(600, 600))  
oval.setFill('red') #填充颜色  
oval.draw(win)  
  
#显示文字  
message = Text(Point(win.getWidth()/2, 20), 'Click anywhere to quit.')  
message.draw(win)  
  
#关闭画布窗口  
win.getMouse()  
win.close()  
'''