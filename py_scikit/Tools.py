# -*- coding: utf-8 -*- 
import os
import Config
import sys
import PdfProcessor
os.chdir(Config.WORKSPACE)

#��Ƕ�׵��б��Ϊһά�б�
def __flatList(nested_list, to):
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            for sub_item in expand_list(item):
                to.append(sub_item)
        else:
            to.append(item)
def flatList(nested_list):
	to = []
	__flatList(nested_list,to)
	return to
