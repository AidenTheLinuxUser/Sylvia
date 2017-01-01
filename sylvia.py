#This code relies on the mechanize, beauitfulsoup, and requests library
#If you do not have these libraries, the code WILL NOT WORK 
import mechanize
import urllib
from bs4 import BeautifulSoup
import time
import requests
import socket

desc = """Welcome to the Sylvia Exploit Detection Program
Written by Aiden The Linux User

Github: https://github.com/AidenTheLinuxUser

Quora:	https://www.quora.com/profile/Aiden-Calvert-2

StackOverflow:
"""

print desc


	
#Opens instance of mechanize browser
url = raw_input("Enter a URL:\n> ")
testBrowser = mechanize.Browser() 


print "\n"

robotsTXT = raw_input("Ignore Robots.txt?(Y/N)\n> ") 

#Sets mechanize robots.txt settings to true or false
if robotsTXT == "Y" or robotsTXT == "y":
	print "Robots.txt will be ignored"
	testBrowser.set_handle_robots(False)
	ignoreRobots = True 
	
elif robotsTXT == "N" or robotsTXT == "n": 
	print "Robots.txt will not be ignored"
	testBrowser.set_handle_robots(True)
	ignoreRobots = false

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


websiteIp = socket.gethostbyname('google.com')

print "Target Sites IP Adress: " + websiteIp 


time.sleep(1)


print "\nChecking for SQL Injection...\n"


#Opens site and adds single-quote to end of URL to check for SQLi
try:
	checkCommaSQL =  urllib.urlopen(url + "'").read()
except: 
	print "SAFE - No Browser SQLi Detected\n"
	checkCommaSQL = " " ;



SQLERROR = "You have an error in your SQL syntax"

#Checks for SQL Error string on page
if SQLERROR in checkCommaSQL: 
	print "\nEXPLOIT - URL SQLi detected using single-quote on URL.\n"

#Terminate if/else statement if SQLi check errored 
elif checkCommaSQL == " ": 
	pass;
	
else:
	print "No Browser SQLi detected."

time.sleep(1)


print "Checking for Directory Indexing...\n" 

#Requests data from www.url.com/img/ 
#If it returns anything, check to see if there is indexing on that page
requestImg = requests.get(url + "/img/")

indexImg = False
if requestImg.status_code == 200:
	readImgIndex = urllib.urlopen(url + "/img/").read()
	if "Index of" in readImgIndex: 
		print "VULNERABILITY - Indexing on /img/\n"
		indexImg = True

if indexImg == False: 
	print "SAFE - No Indexing On /img/\n" 

time.sleep(1)
	




#Requests data from www.url.com/css/ 
#If it returns anything, check to see if there is indexing on that page
requestCss = requests.get(url + "/css/")
cssIndex = False 
if requestCss.status_code == 200:
	readCssIndex = urllib.urlopen(url + "/css/").read()
	if "Index of" in readCssIndex: 
		print "VULNERABILITY - Indexing on /css/\n"
		cssIndex = True

if cssIndex == False: 
	print "SAFE - No Indexing Found On /css/\n" 


time.sleep(1) 

print "Checking for CGI...\n" 

time.sleep(1)

requestCgiBin = requests.get(url + "/cgi-bin/")
requestCgiSys = requests.get(url + "/cgi-sys/")

cgiDetected = False

if requestCgiBin.status_code == 403: 
	print "CGI-BIN Detected. Scanning for vulnerabilities..."
	cgiDetected = True
	
if requestCgiSys.status_code == 403: 
	print "CGI-SYS Detected. Scanning for vulnerabilities..."
	cgiDetected = True 
	
if cgiDetected == False: 
	print "No CGI Detected. Skipping these steps." 






