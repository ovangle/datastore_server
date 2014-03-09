#!/usr/bin/env python
import os
import sys
import socket
import logging
import BaseHTTPServer

import httplib2
from oauth2client import client
from oauth2client import gce
from googledatastore import connection

GOOGLE_API_URL = 'https://www.googleapis.com'

TEST_DATASTORE_PORT = 5556
TEST_DATASTORE_URL = 'http://localhost:{}'.format(TEST_DATASTORE_PORT)

def get_credentials_from_env():
  try:
    credentials = gce.AppAssertionCredentials(connection.SCOPE)
    http = httplib2.Http()
    credentials.authorize(http)
    credentials.refresh(http)
    print('connect using compute credentials')
    return credentials
  except (client.AccessTokenRefreshError, httplib2.HttpLib2Error, socket.error):
    if (os.getenv('DATASTORE_SERVICE_ACCOUNT')
      and os.getenv('DATASTORE_PRIVATE_KEY_FILE')):
      with open(os.getenv('DATASTORE_PRIVATE_KEY_FILE'), 'rb') as f:
        key = f.read()
        credentials = client.SignedJwtAssertionCredentials(
          os.getenv('DATASTORE_SERVICE_ACCOUNT'),
          key,
          connection.SCOPE)
        print('connect using signed JWT credentials')
        return credentials
    print('connect using no credentials')
    return None

class Datastore():
  def __init__(self, credentials):
    self._http = httplib2.Http()
    self.host = TEST_DATASTORE_URL
    if credentials:
      credentials.authorize(self._http)
      self.host = GOOGLE_API_URL
    
  def post(self, path, headers, payload):
    print("Forwarding request to {}".format(path))
    print("\tRequest headers: {}".format(headers))
    print("\tRequest body: {}".format(payload))
    print('done')
    print(self.host + path)
    return self._http.request(
      self.host + path, method='POST', 
      body=payload, 
      headers=headers)
      
class RequestForwarder(BaseHTTPServer.BaseHTTPRequestHandler):
  """
  Attaches authorization to all incoming requests and forwards them
  on to the datastore
  """
  def __init__(self, request, client_address, server, datastore):
    self.datastore = datastore
    BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
  
  def do_POST(self):
    """
    Forwards a request onto the datastore server
    """
    if not 'content-length' in self.headers: 
      self.send_invalid_length_response()
      return
    content_length = int(self.headers['content-length'])
    if content_length < 0: 
      self.send_invalid_length_response()
      return
    payload = self.rfile.read(content_length)
    headers = { 'Content-Type' : self.headers.gettype() }
    for k in self.headers.keys():
      headers[k] = self.headers[k]
    response, content = self.datastore.post(self.path, headers, payload)
    if response.status != 200:
        self.send_error(response.status, content)
        return
    self.send_response(response.status)
    for k in response.keys():
        self.send_header(k, response[k])
    self.end_headers()
    self.wfile.write(content)
    self.wfile.close()
    return
  def send_invalid_length_response(self):
    self.send_error(401, 'Content length required')
    
if __name__ == '__main__':
  credentials = get_credentials_from_env()
  datastore = Datastore(credentials)
  def request_handler(request, client_address, server):
    forwarder = RequestForwarder(request, client_address, server, datastore)
    return forwarder
  httpd = BaseHTTPServer.HTTPServer( ('localhost', 5555), request_handler)
  httpd.serve_forever()
      

