import subprocess 

def speakOut(msg):
	s = subprocess.call(["/usr/bin/espeak", msg])
	
	
speakOut("The temperature is 10 degress")
