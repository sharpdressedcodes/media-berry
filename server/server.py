#!/usr/bin/python

import struct, subprocess, os, time, logging
from socket import *
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from urllib import unquote

# Server configuration
SERVER_HOST = "127.0.0.1"    
SERVER_PORT = 29876    
SERVER_ADDRESS = (SERVER_HOST,SERVER_PORT)    
BUFFER_SIZE = 4096    
MAX_CONNECTIONS = 10
SCRIPT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
VIDEO_PLAYER_PATH = SCRIPT_DIR_PATH + "/omxplayer.sh"
CONTROL_FILE_PATH = SCRIPT_DIR_PATH + "/server.ctl"
LOG_FILE_PATH = SCRIPT_DIR_PATH + "/server.log"

# Logging configuration
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO)

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

# Function to wait for until a process has started
def waitForProcess(process):
	
	while process != None and process.poll() != None:
		time.sleep(0.1)
		
	return process

# Function to check if a process is running
def isProcessRunning(process):

	if process != None and process.poll() != None:
		return False
	else:
		return True

# Function to get the key code for a key
def getKeyCode(key):
	
	formatString = ">L"		
	keyCode = None

	# Cursor left
	if key == "%":
		keyCode = struct.pack(formatString, 0x5b44);
	# Cursor right
	if key == "'":
		keyCode = struct.pack(formatString, 0x5b43);
	# Cursor up
	if key == "&":
		keyCode = struct.pack(formatString, 0x5b41);
	# Cursor down
	if key == "(":
		keyCode = struct.pack(formatString, 0x5b42);

	if keyCode == None:
		keyCode = key

	return keyCode

# Now we create a new socket object
serv = socket( AF_INET,SOCK_STREAM)      

# Bind our socket to the server address
serv.bind((SERVER_ADDRESS)) 

# Set the maximum number of queued connections
serv.listen(MAX_CONNECTIONS)

# Logging
logging.info("Start listening for video urls on host '" + str(SERVER_HOST) + "' and port '" + str(SERVER_PORT) + "' ...")

# Variable for process instance
process = None

while True:
	
	# Accept the connection	
	conn,SERVER_ADDRESS = serv.accept() 

	# Read the string from the socket
	text = readTextFromSocket(conn)
	
	# Create http request from string
	request = HTTPRequest(text)

	# Send dummy http response
	conn.send("HTTP/1.1 200 OK\nContent-type: text/plain;charset=UTF-8\n\nOK")

	# close the client connection
	conn.close()
	
	# Is a path submitted in the request?
	if hasattr(request, "path"):

		# Parse information from request
		pathArray = request.path.split("/")
		action = pathArray[1]
		
		# Play video 
		if action == "play":

			url = unquote(pathArray[2])							

			# If url is correct -> open with video player
			if url.startswith("http"):
				
				logging.info("Opening url '" + url + "' in omxplayer ...")

				# Create control file for omxplayer
				if os.path.exists(CONTROL_FILE_PATH):
					os.system("rm " + CONTROL_FILE_PATH)
				os.system("mkfifo " + CONTROL_FILE_PATH)

				# Open omxplayer 
				process = subprocess.Popen([VIDEO_PLAYER_PATH, url, CONTROL_FILE_PATH], \
					shell=False, \
					stderr=subprocess.PIPE, \
					stdout=subprocess.PIPE, \
					stdin=subprocess.PIPE)

				# Wait for omxplayer 
				waitForProcess(process)

				# Start video in omxplayer
				os.system("echo . > " + CONTROL_FILE_PATH)

		elif action == "control":

			try:
				if isProcessRunning(process):

					key = pathArray[2].lower()
					keyCode = getKeyCode(key)

					logging.info("Sending key code '" + keyCode + "' to omxplayer ...")

					# Piping key code to control file
					os.system("echo -n " + keyCode + " > " + CONTROL_FILE_PATH)

					# q -> Quit omx player
					if keyCode == "q":
						logging.info("Stopping omxplayer ...")
						waitForProcess(process)
						os.system("rm " + CONTROL_FILE_PATH)
						
			except Exception, e:
				logging.error("An error occured while sending a key code to omxplayer: " + str(e))