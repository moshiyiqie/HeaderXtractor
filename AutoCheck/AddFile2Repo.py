import os
import shutil
idx=1
year = [str(x) for x in range(2005,2017)]
def addFileTo(fromPath,toPath):
	global idx
	if idx > 300: return
	for one in os.listdir(fromPath):
		if fromPath == 'D:/acm_paper/PROC' and not any([(x in one) for x in year]): 
			continue
		whole = os.path.join(fromPath, one)
		if os.path.isdir(whole):
			addFileTo(whole, toPath)
		if os.path.isfile(whole):
			if idx > 300: return
			if one.startswith('p') and one.endswith('.pdf'):
				print 'IN:',whole
				shutil.copyfile(whole, toPath+'/'+str(idx)+'.pdf')
				idx+=1
				if idx > 300: return

if __name__ == '__main__':
	addFileTo('D:/acm_paper/PROC', 'D:/acm_paper/TAO-TEST')