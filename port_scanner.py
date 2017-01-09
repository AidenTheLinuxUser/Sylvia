

import mechanize
import time
import requests
import socket
from contextlib import closing
import subprocess
import sys
from datetime import datetime


desc = "Sylvia Port Scanner BETA 1.0\nWritten By Aiden Calvert"
banner = "---------------------------------------------"
print desc
print banner 

#Selection for port scanning

#Opens instance of mechanize browser
url = raw_input("\nEnter a URL or IP:\n> ")
testBrowser = mechanize.Browser() 


print "\n"



#Connects to site 
try: 
	print "Connecting to " + url + "..."
	testBrowser.open(url)
	print "Connected to URL successfully."
	
except: 
	print "Website refusing connection!\nDid you enter the URL correctly?"
	exit()

testBrowser.close();

if url[:8] == "https://":
	ipURL = url[8:]
elif url[:7] == "http://":
	ipURL = url[7:]

	
	
websiteIp = socket.gethostbyname(ipURL)
print "Target Sites IP Adress: " + websiteIp 


time.sleep(1)
	
	
	
#Port scanning program
#Credit to Python for Begginers 
#Slightly modified for uses of this program
#Link to original code: http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python

#Displays Info on target site/ip
print(banner)
print("IP: " + websiteIp)
print("Hostname: " + url) 
print(banner)


# Ask for input
selections = raw_input("Choose a selection:\n\n1 - Use default port range.\n2 - Enter custom port range.\n> ") 

if selections == "1": 
	useDefault = True 



elif selections == "2": 
	useDefault = False
	startPort = raw_input("Enter a start port:\n> ") 

	try: 
		startPort = int(startPort) 
	except: 
		print "Invalid Start Port. Exiting Program..."
		exit(0)

	endPort = raw_input("\nEnter an end port:\n> ")
	
	try:
		endPort = int(endPort) 
	except:
		print "\nInvalid End Port. Exiting Program..."
		exit(0)


remoteServerIP  = websiteIp
# Print a nice banner with information on which host we are about to scan
print "-" * 60
print "Please wait, scanning target host\nThis may take a while."
print "-" * 60

# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (here it will scans all ports between 1 and 1024)

# We also put in some error handling for catching errors

foundPorts = False
portAmount = 0
try:
	if useDefault == True:
		for port in range(1,1025):  
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((remoteServerIP, port))
			if result == 0:
				print "Port {}: 	 Open".format(port)
				foundPorts = True 
				portAmount = portAmount + 1 
			sock.close()

	elif useDefault == False: 
		for port in range(startPort, endPort):  
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((remoteServerIP, port))
			if result == 0:
				print "Port {}: 	 Open".format(port)
				foundPorts = True 
				portAmount = portAmount + 1 
			sock.close()
	
except KeyboardInterrupt:
	print "You pressed Ctrl+C"
	sys.exit()

except socket.gaierror:
	print 'Hostname could not be resolved.'
	sys.exit()

except socket.error:
	print "Couldn't connect to server."
	sys.exit()

# Checking the time again
t2 = datetime.now()

# Calculates the difference of time, to see how long it took to run the script
total =  t2 - t1

# Printing the information to screen
print "Scanning Completed.\n "

if foundPorts == False:
	print "No ports within port range open"
else:
	print str(portAmount) + " ports found open."
		
