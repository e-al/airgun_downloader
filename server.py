#!/usr/bin/env python3
__author__ = 'last5bits'

import os
from http.server import CGIHTTPRequestHandler, HTTPServer

handler = CGIHTTPRequestHandler
handler.cgi_directories = ['/cgi-bin']
server = HTTPServer(('localhost', 8000), handler)

os.chdir('http')
server.serve_forever()
