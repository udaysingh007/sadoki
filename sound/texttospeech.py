import subprocess 

def speakOut(msg):
	s = subprocess.call(["/usr/bin/espeak", "-a", "200", "-p", "0", msg])
	
	
# speakOut("The temperature is ten degress centigrade")
