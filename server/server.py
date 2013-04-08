#!/usr/bin/python

import struct, subprocess, os, time, logging
from socket import *
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from urllib import unquote

# Server configuration
import urllib
import urllib2
from urlparse import urlparse

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 29876    
SERVER_ADDRESS = (SERVER_HOST,SERVER_PORT)    
BUFFER_SIZE = 4096    
MAX_CONNECTIONS = 10
SCRIPT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_FILE_PATH = SCRIPT_DIR_PATH + "/server.log"

# Logging configuration
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

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
serv.listen(MAX_CONNECTIONS)

# Logging
logging.info("Start listening for video urls on host '" + str(SERVER_HOST) + "' and port '" + str(SERVER_PORT) + "' ...")

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

        logging.info(request.path)

        # Parse information from request
        pathArray = request.path.split("/")
        action = pathArray[1]

        # Play video
        if action == "play":
            part = urlparse(request.path)

            url = unquote(part.path.split("/")[2])
            hdmi = ""
            screen = "--windows"

            # we take all param out of the url
            params = part.query.split("&")
            for param in params:
                if param.split("=")[0] == "hdmi":
                    if param.split("=")[1]=="true":
                        hdmi = "-o hdmi"
                if param.split("=")[0] == "screen":
                    if param.split("=")[1]=="fullscreen":
                        screen = ""
                if param.split("=")[0] == "youtube":
                    if param.split("=")[1]=="true":
                        url = "$(youtube-dl -g "+ url +")"


            logging.info("url = "+url+" hdmi="+ hdmi+" screen= "+screen)


            # If url is correct -> open with video player
            # if url.startswith("http"):
                # subprocess.Popen(["/usr/bin/omxgtk","--windows", url])