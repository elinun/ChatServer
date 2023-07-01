#import socket module
from socket import *
import sys # In order to terminate the program

HOST = ''
PORT = 80

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
try:
	serverSocket.bind((HOST, PORT))
except socket.error as msg:
	print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()
	 
print('Socket bind complete')
serverSocket.listen()
while True:
  #Establish the connection
  print('Ready to serve...')
  connectionSocket, addr = serverSocket.accept()
  try:
    message = connectionSocket.recv(1024)
    filename = "static/html/websocket.html"
    f = open(filename) 
    outputdata = f.read()
    connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
    #Send the content of the file to the client
    for i in range(0, len(outputdata)): 
      connectionSocket.send(outputdata[i].encode())
    connectionSocket.send("\r\n".encode())
 
    connectionSocket.close()
  except:
    connectionSocket.send("HTTP/1.1 500 INTERNAL SERVER ERROR\r\nContent-Length: 0\r\n\r\n".encode())
    connectionSocket.close()
    serverSocket.close()
  #sys.exit()#Terminate the program after sending the corresponding data


