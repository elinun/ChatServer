sudo killall python
cd /home/pi/0fc/ChatServer
sudo nohup python -m http.server 8080 &
sudo nohup python ChatSocketServer.py
