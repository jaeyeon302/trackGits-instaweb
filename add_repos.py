import os,pickle
__CONFIG_NAME = "trackGits.conf"
__INSTAWEB_DIR = "git-insta"
__SRC_DIR = os.path.dirname(os.path.abspath(__file__))

def isDir(directory):
	if os.path.isdir(directory): return True
	elif os.path.exists(directory): print("{} is Not Directory".format(directory))
	else: print("{} does not exist".format(directory))
	return False

def isGit(directory):
	gitdir = os.path.join(directory,'.git')
	if os.path.isdir(gitdir):
		print("Git checked")
		return True
	else:
		print("Git was not initialized")
		return False
	
def isInstalled(confPath):
	if os.path.exists(confPath):
		with open(confPath,'rb') as f:
			confs = pickle.load(f)
			instawebDir = confs['instawebDir']
			
		if isDir(instawebDir) and isGit(instawebDir):
			return True
		else: return False
	else: return False
	
	
def install(instawebDir,conf):
	'''
	install directory to run git-instaweb
	
	instawebDir(str): absolute path of directory
	conf(str): absolute path of conf file of trackGits
	'''
	
	#set the absolute path of conf
	if not isDir(instawebDir): return False
	
	#initialize and check instawebDir 
	instawebDir = os.path.join(instawebDir,__INSTAWEB_DIR)	
	if not os.path.exists(instawebDir):
		os.mkdir(instawebDir)
		print("{} created".format(instawebDir))
	else:
		print("already created\n {{} checked".format(instawebDir))
		
	#git-initialize and check instawebDir
	if isGit(instawebDir): print("{} git-checked")
	else:
		os.system('git init {}'.format(instawebDir))
		print("{} git-initialized".format(instawebDir))
	print("ready for git-instaweb")
	
	#update conf
	if os.path.exists(conf): os.remove(conf)
		
	#SAVE CONFIGURATIONS
	with open(conf,'wb') as f:
		confs = {}
		confs['instawebDir'] = instawebDir
		pickle.dump(confs,f)
		print("generate {}".format(conf))
	return True
	
def addDir(dirPath, conf):
	if not isDir(dirPath): return False
	if not isGit(dirPath): return False
	
	#LOAD CONFIGURATIONS
	with open(conf,'rb') as f:
		confs = pickle.load(f)
		instawebDir = confs['instawebDir']
	dst = os.path.join(instawebDir,os.path.basename(dirPath))
	os.symlink(dirPath,dst)
	
	print("{}->{}".format(dirPath,dst))
	if os.path.islink(dst):
		print("add success")
		return True
	else:
		print("add Fail")
		return False
	
def installView(conf):
	yes = input("Do you want to install 'trackGits'? (y/n): ")
	yes = yes.capitalize()
	if yes == 'Y':
		instawebDir = input('input dir-path to run git-instaweb: ')
		instawebDir = os.path.abspath(os.path.expanduser(instawebDir))
		if install(instawebDir,conf):
			print("Success to Install")
			return True
		else:
			print("Fail to Install")
			return False
	elif yes == 'N':
		print('Canceled installation')
		return False
	else:
		print("Wrong user input. not (y/n)")
		return False
	
def main(*args,**kwargs):
	global __CONFIG_NAME, __SRC_DIR
	conf = os.path.join(__SRC_DIR,__CONFIG_NAME)
	if not isInstalled(conf):
		installed = installView(conf)
		if not installed: return False
		
	
	dirPath = kwargs['dirPath']
	addDir(dirPath,conf)
		
def installTest():
	global __CONFIG_NAME, __SRC_DIR
	conf = os.path.join(__SRC_DIR,__CONFIG_NAME)
	
	if not isInstalled(conf):
		installed = installView(conf)
		if not installed: return False
		else: return True
	else:
		return True

def addTest():
	global __CONFIG_NAME, __SRC_DIR
	conf = os.path.join(__SRC_DIR,__CONFIG_NAME)
	
	src = input("dirpath of git project")
	addDir(src,conf)
	
	
print(installTest())
print(addTest())

	

