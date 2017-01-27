#This code relies on the  beauitfulsoup and requests library
#If you do not have these libraries, the code WILL NOT WORK 
#I reccomend pip for installing them

import urllib
from bs4 import BeautifulSoup
import time
import requests
import socket
from contextlib import closing
import subprocess
import sys
from datetime import datetime
import os 


#Will be used to count number of exploits/vulnerabilities.
exploitNum = 0 
vulnNum = 0
dirNum = 0

#Used for chcking whether wordpress is being used 
wordpress = False

#Function to check if website is returning connection code
def checkAccess(request): 
	if request.status_code == 200:
		return True
	else: 
		return False


#Function to check indexing on a directory at the host name
def checkIndexing(host, dirToCheck): 
	indexing = False 
	requestPath = requests.get(host + "/" + dirToCheck + "/")
	readPath = urllib.urlopen(host + "/" + dirToCheck + "/").read().decode('utf-8')
	if requestPath.status_code == 200:
		if "Index of" in readPath: 
			print("- VULNERABILITY - Indexing on /" + dirToCheck + "/")
			indexing = True
	else: 
		print("- /" + dirToCheck + "/" + " returning status code " + str(requestPath.status_code))
	return indexing 
		
			

def checkIndexingRobots(host, dirToCheck): 
	indexing = False 
	requestPath = requests.get(host + "/" + dirToCheck + "/")
	
	try: 
		readPath = urllib.urlopen(host + "/" + dirToCheck + "/").read().decode('utf-8')
	except:
		return False
	if requestPath.status_code == 200:
		if "Index of" in readPath: 
			print("	+ VULNERABILITY - Indexing on /" + dirToCheck + "/")
			indexing = True
	return indexing 
		
				
	

interface = "Select an option:\n" + "1 - Exploit Scanner\n" + "2 - Port Scanner (SLOW)\n"



    
desc = "The Sylvia Pentesting Tool Kit\nWritten by Aiden Calvert"

banner = "---------------------------------------------"

print(desc)
print(banner) 

while(True):
	userSelection = raw_input(interface + "> ")
	try:
		userSelection = int(userSelection)
		break
	except ValueError: 
		print "\nInvalid Option. Try Again.\n"
		continue

#EXPLOIT SCANNER START
if userSelection == 1:
	print "\nSylvia Exploit Scanner v1.01" 
	print banner
	#Opens instance of mechanize browser
	url = raw_input("\nEnter a URL or IP:\n> ")
	
	#Cuts out http and https to where host is resolvable by ip checker 
	resolved = True 
	if url[:8] == "https://":
		urlIp = url[8:]
	elif url[:7] == "http://":
		urlIp = url[7:]
	else:
		resolved = False 
		urlIp = "Unresolvable"
	
	#Finds websites IP
	if resolved == False: 
		websiteIp = "Unresolvable"  
	else: 
		websiteIp = socket.gethostbyname(urlIp)
		
	print("\n")

	try:
		requestSite = requests.get(url) 
	except:
		print "Website refusing connections, did you enter the URL correctly?"
		sys.exit()
	#Checks if site is running on apache 
	try:
		response = urllib.urlopen('http://www.google.com')
		serverType = response.headers['Server']
	except: 
		serverType = "Unresolvable"
	
	
	


	#Displays Info on target site/ip
	print(banner)
	print("IP: " + websiteIp)
	print("Hostname: " + url) 
	print("Server: " + serverType) 
	print(banner)

	


	time.sleep(1)


	

	#Opens site and adds single-quote to end of URL to check for SQLi
	
	try:
		checkCommaSQL =  urllib.request.urlopen(url + "'").read()
	except: 
		print("- SAFE - No Browser SQLi Detected")
		checkCommaSQL = " " ;



	SQLERROR = "You have an error in your SQL syntax"

	#Checks for SQL Error string on page
	if SQLERROR in checkCommaSQL: 
		print("- EXPLOIT - URL SQLi detected using single-quote on URL.")
		exploitNum = exploitNum + 1 
	#Terminate if/else statement if SQLi check errored 
	elif checkCommaSQL == " ": 
		pass;
	
	else:
		print("- No Browser SQLi detected.")

	time.sleep(1)
	
	print banner 


	#Check indexing on common directories
	
	if checkIndexing(url, "img"):
		vulnNum = vulnNum + 1 
		dirNum = dirNum + 1 
	
	if checkIndexing(url, "css"):
		vulnNum = vulnNum + 1 
		dirNum = dirNum + 1 
	
	#Admin wont check if site is wordpress...weird. [Insert shrug emoticon]
	if checkIndexing(url, "admin"):
		vulnNum = vulnNum + 1 
		dirNum = dirNum + 1
	
	if checkIndexing(url, "wp-content"):
		wordpress = True
		vulnNum = vulnNum + 1
		dirNum = dirNum + 1  
	
	if checkIndexing(url, "wp-includes"):
		wordpress = True
		vulnNum = vulnNum + 1 
		dirNum = dirNum + 1 
		
	if checkIndexing(url, "wp-content/uploads"):
		vulnNum = vulnNum + 1 
		dirNum = dirNum + 1 
	
	
	#Guess I'll just check wordpress login form ^_^
	wordpressLogin = requests.get(url + "/wp-login.php")
	if wordpressLogin.status_code == 200 or wordpress == True: 
		print "- Site running on Wordpress template"
		vulnNum = vulnNum + 1
		if wordpressLogin.status_code == 200: 
			print "- Wordpress login found on " + url +  "/wp-login.php" 
		
	time.sleep(1) 

	print banner 


	#Sets conditional booleans and requests cgi-bin and sys
	requestCgiBin = requests.get(url + "/cgi-bin/")
	requestCgiSys = requests.get(url + "/cgi-sys/")

	cgiDetected = False
	cgiVuln = False



	#Checks if CGI-BIN 
	if requestCgiBin.status_code == 200 or requestCgiBin.status_code == 403: 
	
		print("- CGI-BIN Detected and returning code " + str(requestCgiBin.status_code))
		cgiDetected = True
	
		requestHtmlScript = requests.get(url + "/cgi-bin/htmlscript")
	
		#Check for HTMLSCRIPT vulnerability on CGI
		if checkAccess(requestHtmlScript):
			print("	+ CGI VULNERABILITY - HtmlScript found, this could be used for possible exploitation.")
			vulnNum = vulnNum + 1
			cgiVuln = True
	
		requestDumpEnv = requests.get(url + "/cgi-bin/dumpenv") 
		
		#Check for DumpEnv vulnerability
		if checkAccess(requestDumpEnv):
			print("	+ CGI VULNERABILITY - DumpEnv found, can reveal info on server.")
			vulnNum = vulnNum + 1
			cgiVuln = True
		
		requestScriptDir = requests.get(url + "/cig-bin/scripts")
	
		#Check for /cgi-bin/scripts indexability
		if checkAccess(requestScriptDir):
			print("	+ EXPLOIT - /cgi-bin/scripts/ may be indexable and/or readable!")
			exploitNum = exploitNum + 1
			cgiVuln = True
	
		requestCounter = requests.get(url + "/cgi-bin/counterfiglet/")
	
		if checkAccess(requestCounter): 
			print("	+ CGI VULNERABILITY - CounterFiglet accessible, possible hazard.")
			vulnNum = vulnNum + 1
	
	
	
	
	
	if cgiDetected == True and cgiVuln == False: 
		print("	+ No CGI Vulnerabilities found on CGI-BIN.") 


	time.sleep(1)

	#Check CGI-SYS
	cgiVuln = False
	if requestCgiSys.status_code == 200 or requestCgiSys.status_code == 403: 
		print("- CGI-SYS Detected and returning code " + str(requestCgiSys.status_code))
		cgiDetected = True 
		requestHtmlScript = requests.get(url + "/cgi-sys/htmlscript")
	
		#Check for HTMLSCRIPT vulnerability on CGI
		if checkAccess(requestHtmlScript):
			print("	+ CGI VULNERABILITY - HtmlScript found, this could be used for possible exploitation.")
			vulnNum = vulnNum + 1
			cgiVuln = True
	
		requestDumpEnv = requests.get(url + "/cgi-sys/dumpenv") 
		
		#Check for DumpEnv vulnerability
		if checkAccess(requestDumpEnv):
			print("	+ CGI VULNERABILITY - DumpEnv found, can reveal info on server.")
			vulnNum = vulnNum + 1
			cgiVuln = True
		
		requestScriptDir = requests.get(url + "/cgi-sys/scripts")
	
		#Check for /cgi-bin/scripts indexability
		if checkAccess(requestScriptDir):
			print("	+ EXPLOIT - /cgi-sys/scripts/ may be indexable and/or readable!")
			exploitNum = exploitNum + 1
			cgiVuln = True
	
		requestCounter = requests.get(url + "/cgi-sys/counterfiglet/")
	
		if checkAccess(requestCounter): 
			print("	+ CGI VULNERABILITY - CounterFiglet accessible, possible hazard.")
			vulnNum = vulnNum + 1
			cgiVuln = True
	#Checks if any vulns have been detected 
	if cgiDetected == True and cgiVuln == False: 
		print("	+ No CGI Vulnerabilities found on CGI-SYS.")
	
	#Checks if any CGI was detected, if not, it continues program
	if cgiDetected == False: 
		print("- No CGI Detected. Skipping these steps.") 

	print banner

	requestRobotsTxt = requests.get(url + "/robots.txt") 


#Checks if robots.txt exists, and requests if user would like to see the contents
	if checkAccess(requestRobotsTxt):
		if 1==1: 
			#Downloads robots.txt
			print("- Downloading robots.txt...")
			with open('robots.txt','wb') as f:
				f.write(urllib.urlopen(url + "/robots.txt").read())
				f.close()
			print("- Download Complete.")
	
	
			with open('robots.txt', 'r') as f:
				first_line_robots = f.readline()
			
			#Reads robots.txt and saves it to varaible readRobots
			robots = urllib.urlopen(url + "/robots.txt")
			readRobots = robots.read().decode('utf-8') 
		
			#Formats robots.txt to attempt to only have directory names
			newString = readRobots.replace("Allow:", "")
			newString = readRobots.replace("User-agent: *", "")
			newString = newString.replace("Disallow:", "") 
			newString = newString.replace(first_line_robots, "")
			newString = newString.replace(" ", "") 
		
		
			tempList = [] 
			#Cycles through formatted robots.txt
			for char in newString:
				#Adds characters of directory name to tempList 
				if char != "\n": 
					tempList.append(char)
			
				else: 
					#Joins directory name into string
					tempDir = ''.join(tempList)
					#Clear list and start over if not a valid link 
					try: 
						if tempDir[0] != "/": 
							tempList = []
							continue
					#Error catching if string is nothing
					except IndexError: 
						tempList = []
						continue
					
					#Error catching if string is nothing
					if tempDir == "" or tempDir == " ": 
						tempList = [] 
						break
					#Tries connecting with formatted directory, if it doesnt work, clear list and move on	
					try: 
						dirConnect = requests.get(url + tempDir) 
					except: 
						tempList = [] 
						continue
				
					#Prints out status code and checks if indexing is available on link
					#Will only check indexing if directory exists (i.e not 404ing) 
				
					#Wont display URL if its 404ing
					if dirConnect.status_code == 404: 
						tempList = []		
						continue 
					print("- " + tempDir + " returning status code " + str(dirConnect.status_code))
				
					if dirConnect.status_code != 404: 
						checkIndexingRobots(url, tempDir)
					
					#Adds one to dirNum, clears list and reruns loop
					dirNum = dirNum + 1
					tempList = []
	
		else: 
			print " - Robots.txt not found. Skipping this step..."
		#Removes robots.txt from current directory
		os.remove("robots.txt") 

	print banner			
	print "Scan completed.\n" + str(exploitNum) + " exploits detected.\n" +  str(vulnNum) + " vulnerabilities detected.\n" + str(dirNum) + " directories scanned."  	

#EXPLOIT SCANNER END



#PORT SCANNER START

elif userSelection == 2: 
	desc = "Sylvia Port Scanner BETA 1.0\nWritten By Aiden Calvert"
	banner = "---------------------------------------------"
	print desc
	print banner 

	#Selection for port scanning

	#Opens instance of mechanize browser
	url = raw_input("\nEnter a URL or IP:\n> ")
	#Cuts out http and https to where host is resolvable by ip checker 
	resolved = True 
	if url[:8] == "https://":
		urlIp = url[8:]
	elif url[:7] == "http://":
		urlIp = url[7:]
	else:
		resolved = False 
		urlIp = "Unresolvable"
	
	#Finds websites IP
	if resolved == False: 
		websiteIp = "Unresolvable"  
	else: 
		websiteIp = socket.gethostbyname(urlIp)
		
	print("\n")

	try:
		requestSite = requests.get(url) 
	except:
		print "Website refusing connections, did you enter the URL correctly?"
		sys.exit()
	#Checks if site is running on apache 
	try:
		response = urllib.urlopen('http://www.google.com')
		serverType = response.headers['Server']
	except: 
		serverType = "Unresolvable"
	
	websiteIp = socket.gethostbyname(urlIp)


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
	selections = raw_input("\nChoose a selection:\n\n1 - Use default port range (1-2000)\n2 - Enter custom port range\n> ") 

	if selections == "1": 
		useDefault = True 



	elif selections == "2": 
		useDefault = False
		startPort = raw_input("\nEnter a start port:\n> ") 

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

	# Using the range function to specify ports (here it will scans all ports between 1 and 1024)

	foundPorts = False
	portAmount = 0
	try:
		if useDefault == True:
			for port in range(1,2000):  
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				result = sock.connect_ex((remoteServerIP, port))
				if result == 0:
					print "Port " + str(port) + " Open."
					foundPorts = True 
					portAmount = portAmount + 1 
				sock.close()

		elif useDefault == False: 
			for port in range(startPort, endPort):  
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				result = sock.connect_ex((remoteServerIP, port))
				if result == 0:
					print "Port " + str(port) + " Open."
					foundPorts = True 
					portAmount = portAmount + 1 
				sock.close()
	

	except socket.gaierror:
		print 'Hostname could not be resolved.'
		sys.exit()

	except socket.error:
		print "Couldn't connect to server."
		sys.exit()

	

	# Printing the information to screen
	print "Scanning Completed.\n "

	if foundPorts == False:
		print "No ports within port range open"
	else:
		print str(portAmount) + " ports found open."
			
#PORT SCANNER END


