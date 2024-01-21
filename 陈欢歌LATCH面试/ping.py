#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ping Google Script
"""
import subprocess
import os
import time
import threading
from threading import Timer

def pingGoogle(f):
	kill = lambda process: process.kill()
	cmd = ['ping', 'www.google.com']
	ping = subprocess.Popen(
	cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	my_timer = Timer(1, kill, [ping])
	try:
		my_timer.start()
		stdout, stderr = ping.communicate()
		print(stdout, file = f)
	finally:
		my_timer.cancel()
	p = subprocess.call('ping -c1 127.0.0.1',shell=True)

def saveFile(pingGoogle):
	with open('./data.txt', 'a') as f:
		pingGoogle(f)

if __name__ == '__main__':
	count = 1
	while True:
		if(count <= 300): # run 300 seconds
			saveFile(pingGoogle)
			count+=1
		else:
			break;