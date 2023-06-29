#!/usr/bin/env python2
import socket;
import paramiko as ssh;
import threading as thread;
import sys;

# Key from Paramiko demo files
# https://github.com/paramiko/paramiko/blob/master/demos/test_rsa.key
key = ssh.RSAKey(filename='test_rsa.key');

class Server(ssh.ServerInterface):
    def _init_(self):
        self.event = thread.Event();
    def checkChannelRequest(self, kind, chanid):
        if kind == 'session':
            return ssh.OPEN_SUCCEEDED;
        return ssh.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED;
    def checkAuthPassword(self, username, password):
        # Define your SSH credentials
        if (username == '<USERNAME>') and (password == '<PASSWORD>'):
            return ssh.AUTH_SUCCESSFULL;
        return ssh.AUTH_FAILED;

server = sys.argv[1];
port = int(sys.argv[2]);

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    sock.bind((server, port));
    sock.listen(100);
    print '[+] Listening for connection ...';
    client, addr = sock.accept();
except Exception as e:
    print '[-] Listen failed: ' + str(e);
    sys.exit(1);

print '[+] Connection received!'

try:
    session = ssh.Transport(client);
    session.add_server_key(key);
    server = Server();
    
    try:
        session.start_server(server=server);
    except ssh.SSHException as e:
        print '[-] SSH negotiation failed: ' + str(e);

    chan = session.accept(20);
    print '[+] Authenticated!';
    print chan.recv(1024);
    chan.send('Greetings, personal SSH.');
    while True:
        try:
            command = raw_input("Enter command: ").strip('\n');
            if command != 'exit':
                chan.send(command);
                print chan.recv(1024) + '\n';
            else:
                chan.send('exit');
                print 'Goodbye';
                session.close();
                raise Exception('exit');
        except KeyboardInterrupt:
            session.close();

except Exception as e:
    print '[-] Exception: ' + str(e);
    try:
        session.close();
    except:
        pass;
    sys.exit(1);
