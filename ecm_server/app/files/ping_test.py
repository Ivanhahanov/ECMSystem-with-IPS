#!/usr/bin/python3
import os
import subprocess
import sys
hostnames = ["online-edu.mirea.ru", "google.com"]
print('${color grey}Mirea site check:')
for hostname in hostnames:
	status,result = subprocess.getstatusoutput("ping -c1 -w2 " + hostname)

	if status == 0: 
	       print('${color green}'+ hostname + " is UP!")
	else:
	       print('${color red}' + hostname +" is DOWN!")


