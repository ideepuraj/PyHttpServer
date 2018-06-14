#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import subprocess
import shlex
from subprocess import Popen, PIPE
import thread
from threading import Thread
from time import sleep
import threading


PORT_NUMBER = 8000


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	#capture image
	def capture_img(self):
		print 'saving image...'
		cmd = 'ffmpeg -loglevel quiet -i rtsp://admin:vava@deep143@192.168.2.18/onvif1 -s 1280x960 -vframes 1 -r 1 -y /home/osmc/PyHttpServer/cam.jpg'
		p=subprocess.Popen(shlex.split(cmd), stdout=PIPE)
		p.wait()

	#Handler for the GET requests
	def do_GET(self):
		print 'do_GET: ', self.path
		self.path = self.path.split("?")[0]
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and
			#set the right mime type
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				print 'serve file:', curdir + sep + self.path
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()

			#print 'Create new thread..'
			print threading.active_count()
			thread = None
			#if not thread or not thread.is_alive():
			if threading.active_count() <=1 :
				print 'start new...'
				thread = Thread(target=self.capture_img)
				thread.start()
			else:
				print 'running...'

			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
			thread = None
			if not thread or not thread.is_alive():
				print 'start new...'
				thread = Thread(target=self.capture_img)
				thread.start()
			else:
				print 'running...'

#try:
	#Create a web server and define the handler to manage the
	#incoming request
server = HTTPServer(('', PORT_NUMBER), myHandler)
print 'Started httpserver on port ' , PORT_NUMBER
	
#Wait forever for incoming htto requests
server.serve_forever()

#except KeyboardInterrupt:
#	print 'shutting down the web server'
#	server.socket.close()