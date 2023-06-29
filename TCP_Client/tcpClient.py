#!/usr/bin/env python2
import socket;

target_host = "127.0.0.1";
target_port = 9999;

# AF_INET = IPv4
# SOCK_STREAM = TCP client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
client.connect((target_host, target_port));

client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n");
answer = client.recv(4096);
print answer;