# -*- coding: utf-8 -*- 
import os
import Config
import sys
os.chdir(Config.WORKSPACE)
#×÷ÕßÀà
class Author:
	name=''
	address=''
	affliation=''
	email=''
	def __init__(self, name='', address='', affliation='', email=''):
		self.name = name
		self.address = address
		self.affliation = affliation
		self.email = email
	def toString(self):
		outStr = ''
		if len(self.name)>0: outStr += '[Author name]:' + self.name + '\n'
		if len(self.address)>0: outStr += '[Address]:' + self.address + '\n'
		if len(self.affliation)>0: outStr += '[Affliation]:' + self.affliation + '\n'
		if len(self.email)>0: outStr += '[Email]:' + self.email + '\n'
		return outStr
	def toDic(self):
		dic={}
		dic['name'] = self.name
		dic['address'] = self.address
		dic['affliation'] = self.affliation
		dic['email'] = self.email
		return dic