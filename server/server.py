#!/usr/bin/python

import subprocess, os, time, logging
from socket import *
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from urllib import unquote
from urlparse import urlparse


SCRIPT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_FILE_PATH = SCRIPT_DIR_PATH + "/server.log"

# Logging configuration
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO)

# Logger to console TODO disable it in stable
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
    BUFFER_SIZE = 4096
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


class Serverhttp:
    def __init__(self):
        SERVER_HOST = "127.0.0.1"
        SERVER_PORT = 29876
        SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)
        MAX_CONNECTIONS = 10
        try:

            # Now we create a new socket object
            serv = socket(AF_INET, SOCK_STREAM)

            serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

            # Bind our socket to the server address
            serv.bind((SERVER_ADDRESS))

            # Set the maximum number of queued connections
            serv.listen(MAX_CONNECTIONS)

            # Logging
            logging.info("Start listening for video urls on host '" + str(SERVER_HOST) + "' and port '" + str(
                SERVER_PORT) + "' ...")
        except Exception as e:
            time.sleep(2)
            logging.info(e)
            self.__init__()

        while True:
            conn, SERVER_ADDRESS = serv.accept()
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
                    part = urlparse(request.path)
                    url = unquote(part.path.split("/")[2])
                    processList = ["/usr/bin/omxgtk"]

                    # we get all parameter out of the url
                    params = part.query.split("&")
                    for param in params:
                        if param.split("=")[0] == "hdmi":
                            if param.split("=")[1] == "true":
                                processList.append("-o hdmi")
                        if param.split("=")[0] == "screen":
                            if not param.split("=")[1] == "fullscreen":
                                processList.append("--windows")
                        if param.split("=")[0] == "youtube":
                            if param.split("=")[1] == "true":
                                processList.append("$(youtube-dl -g " + url + ")")
                            else:
                                processList.append(url)

                    logging.info(processList)
                    try:
                        subprocess.Popen(processList)
                    except:
                        processList[0] = "/usr/bin/omxplayer"
                        try:
                            subprocess.Popen(processList)
                        except:
                            logging.info("Cannot start video [" + str(processList) + "]")


server = Serverhttp()
