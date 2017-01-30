import urllib
from bs4 import BeautifulSoup
import time
import requests
import socket
from contextlib import closing
import subprocess
import sys
import os 

#Print description and ask for URL/IP
banner = "---------------------------------------------"
wcDesc = "Sylvia Web Scraper DEVELOPMENT_MODE\n" + banner


print wcDesc

question = "\nEnter a URL or IP\n> "


url = raw_input(question) 


#Check if target is online 
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


try:
	requestSite = requests.get(url) 
except:
	print "Website refusing connections, did you enter the URL correctly?"
	sys.exit()
	

#Checks what server websites running on 
try:
	response = urllib.urlopen(url)
	serverType = response.headers['Server']
except: 
	serverType = "Unresolvable"
	
websiteIp = socket.gethostbyname(urlIp)


time.sleep(1)
print "\n"
#Displays Info on target site/ip
print(banner)
print("IP: " + websiteIp)
print("Hostname: " + url) 
print("Server: " + serverType) 
print(banner)

