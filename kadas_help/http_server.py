#!/usr/bin/python3

import os
import socket
import signal
import sys
import time
from threading import Thread

class HttpServer:
    def __init__(self, www_dir, host = "", port = 0):
        self.host = host
        self.port = port
        self.www_dir = www_dir
        self.thread = None
        self.quitting = False

    def start(self, thread=True):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.bind((self.host, self.port))
            self.host, self.port = self.socket.getsockname()
            print("Running on http://%s:%d" % (self.host, self.port))

        except Exception as e:
            print("Error: failed to start server on %s:%d" % (self.host, self.port))
            self.shutdown()
            return False

        if thread:
            self.thread = Thread(target=self._wait_for_connections)
            self.thread.setDaemon(True)
            self.thread.start()
        else:
            self._wait_for_connections()

    def shutdown(self):
        self.quitting = True
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            pass

        if self.thread:
            self.thread.join()

        self.socket.close()

    def _gen_headers(self,  code):
        h = ''
        if (code == 200):
            h = 'HTTP/1.1 200 OK\n'
        elif(code == 404):
            h = 'HTTP/1.1 404 Not Found\n'

        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        h += 'Date: ' + current_date +'\n'
        h += 'Server: Simple-Python-HTTP-Server\n'
        h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request

        return h

    def _wait_for_connections(self):
        while True:
            self.socket.listen()
            try:
                conn, addr = self.socket.accept()
            except:
                if self.quitting:
                    break

            data = conn.recv(1024)
            string = bytes.decode(data)
            parts = string.split(' ')

            if len(parts) >= 2 and ((parts[0] == 'GET') or (parts[0] == 'HEAD')):
                request_method = parts[0]
                file_requested = parts[1]

                # omit any querystring
                file_requested = file_requested.split('?')[0]

                # load index.html if not file specified
                if (file_requested.endswith('/')):
                    file_requested += 'index.html'

                file_requested = self.www_dir + file_requested

                ## Load file content
                try:
                    file_handler = open(file_requested,'rb')
                    if (request_method == 'GET'):  #only read the file when GET
                        response_content = file_handler.read() # read file content
                    file_handler.close()

                    response_headers = self._gen_headers(200)

                except Exception as e:
                    response_headers = self._gen_headers( 404)

                    if (request_method == 'GET'):
                        response_content = b"<html><body><p>Error 404: File not found</p></body></html>"

                server_response =  response_headers.encode()
                if (request_method == 'GET'):
                    server_response +=  response_content

                conn.send(server_response)
            conn.close()

if __name__ == "__main__":
    lang="en"
    www_dir = os.path.join(os.path.dirname(__file__), "html", lang)
    s = HttpServer(www_dir, "127.0.0.1")
    s.start(False)
    signal.signal(signal.SIGINT, s.shutdown)
