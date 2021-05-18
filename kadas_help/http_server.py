#!/usr/bin/python3

import os
import signal
import sys
import time
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtNetwork import *


class HttpServer(QTcpServer):
    def __init__(self, www_dir, host = "", port = 0):
        QTcpServer.__init__(self)
        self.host = host
        self.port = port
        self.www_dir = www_dir
        self.listen(QHostAddress(host), port)
        self.host = self.serverAddress().toString()
        self.port = self.serverPort()
        self.newConnection.connect(self.handleConnection)

    def _gen_headers(self,  code):
        h = ''
        if (code == 200):
            h = 'HTTP/1.1 200 OK\n'
        elif(code == 404):
            h = 'HTTP/1.1 404 Not Found\n'

        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        h += 'Date: ' + current_date +'\n'
        h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request
        return h

    def handleConnection(self):
        while self.hasPendingConnections():
            socket = self.nextPendingConnection()
            # socket.waitForReadyRead()
            loop = QEventLoop()
            socket.readyRead.connect(loop.quit)
            loop.exec_()
            data = socket.readAll()

            string = bytes(data).decode()
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

                socket.write(server_response)
                socket.flush()
                socket.close()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    www_dir = os.path.join(os.path.dirname(__file__), "html")
    s = HttpServer(www_dir, "127.0.0.1", 42159)
    print("Running on http://%s:%d" % (s.host, s.port))
    app.exec_()
