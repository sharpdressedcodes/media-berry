#!/usr/bin/python

# Example URLs for testing:
# http://localhost:29876/http%3A%2F%2Fwww.kaba.de%2Fbekannter-versender%2Fmedia%2F497816%2Fv9%2FMP4VideoFile%2Ffilm-1-3-final.mp4
# http://localhost:29876/http%3A%2F%2Fwww.kaba.ch%2Fmedia%2F474122%2Fv8%2FMP4VideoFile%2Fzeiterfassung-neu-definiert-terminal-b-web-93-00.mp4

from socket import *
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from urllib import unquote

# Server configuration
SERVER_HOST = ""    
SERVER_PORT = 29876    
SERVER_ADDRESS = (SERVER_HOST,SERVER_PORT)    
BUFFER_SIZE = 4096    
VIDEO_PLAYER_PATH = "/usr/bin/vlc"

# Class for parsing an http request
class HTTPRequest(BaseHTTPRequestHandler):

	def __init__(self, request_text):
		self.rfile = StringIO(request_text)
		self.raw_requestline = self.rfile.readline()
		self.error_code = self.error_message = None
		self.parse_request()

    	def send_error(self, code, message):
		self.error_code = code
		self.error_message = message

# Function to read text from a socket
def readTextFromSocket(sck):

	text = ""

	while True:

		line = ""

		try:
			line = sck.recv(BUFFER_SIZE)			
		except socket.timeout:
			break

		if line == "":
			break

		text += line

		return text
 
# Now we create a new socket object
serv = socket( AF_INET,SOCK_STREAM)      
 
# Bind our socket to the server address
serv.bind((SERVER_ADDRESS)) 

# Set the maximum number of queued connections
serv.listen(10)

# Set variable for the current url
currentUrl = ""

while True:
	# Accept the connection	
	conn,SERVER_ADDRESS = serv.accept() 

	# Read the string from the socket
	text = readTextFromSocket(conn)
	
	# Create http request from string
	request = HTTPRequest(text)

	# Send dummy http response
	conn.send("HTTP/1.1 200 OK\nContent-type: text/plain\n\nOK")

	# close the client connection
	conn.close()

	# Is a path submitted in the request?	
	if hasattr(request, 'path'):
		
		# Parse the url from the request
		url = unquote(request.path[1:])

		# If url is correct -> open with video player
		if url.startswith("http"):

			# Is the submitted url different from the current url?
			if url != currentUrl:			
				subprocess.Popen([VIDEO_PLAYER_PATH, url])
				currentUrl = url
