# -*- coding: utf-8 -*- 
import os
import Config
import sys
import ner
os.chdir(Config.WORKSPACE)
def getNerResult(s):
	tagger = ner.SocketNER(host = 'localhost', port=10111)
	return tagger.get_entities(s)