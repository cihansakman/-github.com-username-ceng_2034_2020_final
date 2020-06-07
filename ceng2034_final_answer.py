#!/usr/bin/python3
#Mehmet Cihan Sakman
import os,uuid,requests,hashlib
from multiprocessing import Pool

def download_file(url,file_name = None):
	r = requests.get(url, allow_redirects = True)
	file = file_name if file_name else str(uuid.uuid4())
	open(file, 'wb').write(r.content)

#With os.fork() we create child process. If value of os.fork() equal zero it means it's a child process.
child = os.fork()

url = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg","https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png","https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg","http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg","https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

#I just use child process for downloading pictures and I use my parent process for rest.
if(child==0):
	print("Child process' ID:",os.getpid())
	j=1	# I will use this 'j' for giving name to my png's.
	for i in url:
		download_file(i,"pic{}".format(j))
		j+=1
	os._exit(0)


print("Parent PID:",os.getpid())
	
	
#This array keeps my picture's names which I gave it before.
pics = ["pic1","pic2","pic3","pic4","pic5"]

print(f'{os.getpid()} is waiting')	


'''
To avoid the orphan process we use os.wait() function. The reason to use it here is that in the following 
codes we need our pictures. And for finding pictures we need to wait for the child process to download pictures.
'''
os.wait()
print(f'{os.getpid()} is processing')

def duplicate_test(file_name):
	temp = 0
	temp2 = 0
	#At this point I checked whether files has duplicate or not.
	for i in pics:
		if(file_name != i):
			if(hashlib.md5(open(file_name,'rb').read()).hexdigest()==hashlib.md5(open(i,'rb').read()).hexdigest()):
				temp = 1
				break
	if(temp==1):
		#At this stage I find out which file is duplicate with which file.
		for j in range(pics.index(i)-1):
			if(hashlib.md5(open(file_name,'rb').read()).hexdigest()==hashlib.md5(open(pics[j],'rb').read()).hexdigest()): temp2 = 1
		if (temp2==0): print(f'{file_name} and {i} are duplicate')
			
	else :
		#If it is not duplicate just print 'not duplicate'.
		if(file_name in pics):	
			print(f'{file_name} is not duplicate')
			print("",end="")

'''
While using Pool() it would meaningless to use more than your cpu count. Because your OS can only use how much you have. 
Therefor it's good to use your cpu count as an argument.
'''

with Pool(os.cpu_count()) as p:
	p.map(duplicate_test,pics)



		
			
	
	
