#!/usr/bin/env python2
import socket;
import threading as thread;

bind_ip = "0.0.0.0";
bind_port = 9999;

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.bind((bind_ip, bind_port));
server.listen(5);

print "[*] Listening on %s:%d" % (bind_ip, bind_port);

def clientHandler(client_socket):
    request = client_socket.recv(1024);
    print "[*] Received: %s" % request;
    client_socket.send("ACK!");
    client_socket.close();

while True:
    client, addr = server.accept();
    print "Connection accepted from: %s:%d" % (addr[0], addr[1]);
    client_handler = thread.Thread(target=clientHandler, args=(client,));
    client_handler.start();
