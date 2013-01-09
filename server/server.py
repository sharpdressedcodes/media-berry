#!/usr/bin/python

# Example URL for testing:
# http://localhost:29876/http%3A%2F%2Fwww.kaba.de%2Fbekannter-versender%2Fmedia%2F497816%2Fv9%2FMP4VideoFile%2Ffilm-1-3-final.mp4

from socket import *
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from urllib import unquote

#let's set up some constants
HOST = ''    #we are the host
PORT = 29876    #arbitrary port not currently in use
ADDR = (HOST,PORT)    #we need a tuple for the address
BUFSIZE = 4096    #reasonably sized buffer for data

class HTTPRequest(BaseHTTPRequestHandler):
	def __init__(self, request_text):
		self.rfile = StringIO(request_text)
		self.raw_requestline = self.rfile.readline()
		self.error_code = self.error_message = None
		self.parse_request()

    	def send_error(self, code, message):
		self.error_code = code
		self.error_message = message
 
def getDataFromSocket(sck):

	text = ""

	while 1:
		line = ""
		try:
			line = sck.recv(BUFSIZE)			
		except socket.timeout:
			break

		if line == "":
			break

		text += line
		return text
 
# now we create a new socket object (serv)
# see the python docs for more information on the socket types/flags
serv = socket( AF_INET,SOCK_STREAM)      
 
#bind our socket to the address
serv.bind((ADDR))    #the double parens are to create a tuple with one element
serv.listen(5)    #5 is the maximum number of queued connections we'll allow
 
while 1:
	conn,addr = serv.accept() #accept the connection	
	text = getDataFromSocket(conn)
	request = HTTPRequest(text)
	url = unquote(request.path[1:])
	subprocess.Popen(["/usr/bin/vlc", url])
	conn.close()
