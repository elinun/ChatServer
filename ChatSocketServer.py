from simple_websocket_server import WebSocketServer, WebSocket
import hashlib

HANDSHAKE_STR = (
   "HTTP/1.1 101 Switching Protocols\r\n"
   "Upgrade: WebSocket\r\n"
   "Connection: Upgrade\r\n"
   "Sec-WebSocket-Accept: %(acceptstr)s\r\n\r\n"
)

FAILED_HANDSHAKE_STR = (
   "HTTP/1.1 426 Upgrade Required\r\n"
   "Upgrade: WebSocket\r\n"
   "Connection: Upgrade\r\n"
   "Sec-WebSocket-Version: 13\r\n"
   "Content-Type: text/plain\r\n\r\n"
   "This service requires use of the WebSocket protocol\r\n"
)

GUID_STR = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

STREAM = 0x0
TEXT = 0x1
BINARY = 0x2
CLOSE = 0x8
PING = 0x9
PONG = 0xA

HEADERB1 = 1
HEADERB2 = 3
LENGTHSHORT = 4
LENGTHLONG = 5
MASK = 6
PAYLOAD = 7

MAXHEADER = 65536
MAXPAYLOAD = 33554432


class SimpleChat(WebSocket):
    def handle(self):
        for client in clients:
            if client != self:
                client.send_message(self.address[0] + u' - ' + self.data)

    def connected(self):
        print("Attempting to connect")
        print(self.address, 'connected')
        for client in clients:
            client.send_message(self.address[0] + u' - connected')
        clients.append(self)

    def handle_close(self):
        clients.remove(self)
        print(self.address, 'closed')
        for client in clients:
            client.send_message(self.address[0] + u' - disconnected')
            
    def _handleData(self):
      # do the HTTP header and handshake
      if self.handshaked is False:

         try:
            data = self.client.recv(self.headertoread)
         except (ssl.SSLWantReadError, ssl.SSLWantWriteError):
            # SSL socket not ready to read yet, wait and try again
            return
         if not data:
            raise Exception('remote socket closed')

         else:
            # accumulate
            self.headerbuffer.extend(data)

            if len(self.headerbuffer) >= self.maxheader:
               raise Exception('header exceeded allowable size')

            # indicates end of HTTP header
            if b'\r\n\r\n' in self.headerbuffer:
               self.request = HTTPRequest(self.headerbuffer)

               # handshake rfc 6455
               try:
                  key = self.request.headers['Sec-WebSocket-Key']
                  k = key.encode('ascii') + GUID_STR.encode('ascii')
                  k_s = base64.b64encode(hashlib.sha1(k).digest()).decode('ascii')
                  hStr = HANDSHAKE_STR % {'acceptstr': k_s}
                  self.sendq.append((BINARY, hStr.encode('ascii')))
                  self.handshaked = True
                  self.handleConnected()
               except Exception as e:
                  hStr = FAILED_HANDSHAKE_STR
                  self._sendBuffer(hStr.encode('ascii'), True)
                  self.client.close()
                  raise Exception('handshake failed: %s', str(e))

      # else do normal data
      else:
         try:
            data = self.client.recv(16384)
         except (ssl.SSLWantReadError, ssl.SSLWantWriteError):
            # SSL socket not ready to read yet, wait and try again
            return
         if not data:
            raise Exception("remote socket closed")

         if VER >= 3:
             for d in data:
                 self._parseMessage(d)
         else:
             for d in data:
                 self._parseMessage(ord(d))


clients = []

server = WebSocketServer('0.0.0.0', 8148, SimpleChat)
server.serve_forever()
